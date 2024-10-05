from src.ChatModel.ChatModel import ChatModel
from src.ChatModel.HuggingfaceChat import HuggingfaceChat
from src.ChatModel.OpenAIChat import OpenAIChat
from src.ChatModel.OllamaChat import OllamaChat
from src.Writer.PromptGenerator import PromptGenerator
import os
import numpy as np
from tqdm import trange, tqdm
import time
import torch
from src.utils import extract_title_sections_descriptions, extract_sections, extract_subsections_subdescriptions
from src.CONSTANT.PROMPTS import ROUGH_OUTLINE_PROMPT, MERGING_OUTLINE_PROMPT, SUBSECTION_OUTLINE_PROMPT, EDIT_FINAL_OUTLINE_PROMPT
from Database import Supabase

class Writer:
    def __init__(self, model: str, api_key: str = None, chat_provider: str = "huggingface", url_key: str = None) -> None:
        self.model = model
        self.api_key = api_key
        self.url_key = url_key
        
        if chat_provider == "huggingface":
            self.chat_model = HuggingfaceChat()
        elif chat_provider == "openai":
            self.chat_model = OpenAIChat()
        elif chat_provider == "ollama":
            self.chat_model = OllamaChat
        else:
            raise ValueError(f"Unsupported chat provider: {chat_provider}")
        
        if chat_provider == "ollama":
            if not self.url_key:
                raise ValueError("url_key is required for Ollama chat provider")
            self.chat_model.initialize(self.model, self.url_key)
        elif chat_provider in ["huggingface", "openai"]:
            if not self.api_key:
                raise ValueError(f"api_key is required for {chat_provider} chat provider")
            self.chat_model.initialize(self.model, self.api_key)
        
        self.prompt_generator = PromptGenerator()

    def generate_rough_outlines(self, topic, papers_chunks, titles_chunks, section_num=8):
        prompts = []
        for i in range(len(papers_chunks)):
            prompt = self.prompt_generator.generate_rough_outline_prompt(topic, papers_chunks[i], titles_chunks[i], section_num)
            prompts.append(prompt)
        
        outlines = [self.chat_model.generate(prompt, temperature=1) for prompt in prompts]
        
        return outlines

    def merge_outlines(self, topic, outlines, section_num=8):
        outline_texts = '' 
        for i, o in enumerate(outlines):
            outline_texts += f'---\noutline_id: {i}\n\noutline_content:\n\n{o}\n'
        outline_texts += '---\n'
        prompt = self.prompt_generator.generate_merge_outlines_prompt(topic, outlines, section_num)
        
        outline = self.chat_model.generate(prompt, temperature=1)
        if not isinstance(outline, str):
            print(f"Warning: outline is not a string. Type: {type(outline)}")
            outline = str(outline)
        return outline

    def generate_subsection_outlines(self, topic, section_outline, rag_num):
        survey_title, survey_sections, survey_section_descriptions = extract_title_sections_descriptions(outline=section_outline)
        
        prompts = []
        for section_name, section_description in zip(survey_sections, survey_section_descriptions):
            paper_list = Supabase.search_documents(section_description, match_count=rag_num)
            prompt = self.prompt_generator.generate_subsection_outline_prompt(topic, section_outline, section_name, section_description, paper_list)
            prompts.append(prompt)
        
        sub_outlines = [self.chat_model.generate(prompt, temperature=1) for prompt in prompts]
        return sub_outlines

    def process_outlines(self, section_outline, sub_outlines):
        sections = extract_sections(section_outline)
        merged_outline = ""
        for i, section in enumerate(sections):
            merged_outline += f"Section {i+1}: {section}\n"
            if i < len(sub_outlines):
                subsections, subsection_descriptions = extract_subsections_subdescriptions(sub_outlines[i])
                for j, (subsection, description) in enumerate(zip(subsections, subsection_descriptions)):
                    merged_outline += f"Subsection {i+1}.{j+1}: {subsection}\n"
                    merged_outline += f"Description {i+1}.{j+1}: {description}\n"
            merged_outline += "\n"
        return merged_outline

    def edit_final_outline(self, outline):
        prompt = self.prompt_generator.generate_edit_final_outline_prompt(outline)
        final_outline = self.chat_model.generate(prompt, temperature=1)
        return final_outline.replace('<format>\n','').replace('</format>','')

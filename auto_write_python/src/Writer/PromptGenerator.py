import os
import numpy as np
import tiktoken
from tqdm import trange, tqdm
import time
import torch
from src.CONSTANT.PROMPTS import ROUGH_OUTLINE_PROMPT, MERGING_OUTLINE_PROMPT, SUBSECTION_OUTLINE_PROMPT, EDIT_FINAL_OUTLINE_PROMPT

class PromptGenerator:
    @staticmethod
    def generate_prompt(template, params):
        prompt = template
        if isinstance(prompt, str):
            for k, v in params.items():
                prompt = prompt.replace(f'[{k}]', str(v))
        else:
            raise TypeError("Template must be a string")
        return prompt

    @staticmethod
    def generate_rough_outline_prompt(topic, papers_chunk, titles_chunk, section_num):
        paper_texts = ''.join([f'---\npaper_title: {t}\n\npaper_content:\n\n{p}\n' for t, p in zip(titles_chunk, papers_chunk)])
        paper_texts += '---\n'
        params = {
            'PAPER LIST': paper_texts,
            'TOPIC': topic,
            'SECTION NUM': str(section_num)
        }
        return PromptGenerator.generate_prompt(ROUGH_OUTLINE_PROMPT, params)

    @staticmethod
    def generate_merge_outlines_prompt(topic, outlines, section_num):
        outline_texts = '' 
        for i, o in enumerate(outlines):
            outline_texts += f'---\noutline_id: {i}\n\noutline_content:\n\n{o}\n'
        outline_texts += '---\n'
        params = {
            'OUTLINE LIST': outline_texts,
            'TOPIC': topic,
            'TOTAL NUMBER OF SECTIONS': str(section_num)# Number of sections equals the number of outlines
        }
        return PromptGenerator.generate_prompt(MERGING_OUTLINE_PROMPT, params)

    @staticmethod
    def generate_subsection_outline_prompt(topic, section_outline, section_name, section_description, paper_list):
        paper_texts = ''.join([f'---\npaper_title: {t}\n\npaper_content:\n\n{p}\n' for t, p in paper_list])
        paper_texts += '---\n'
        params = {
            'OVERALL OUTLINE': section_outline,
            'SECTION NAME': section_name,
            'SECTION DESCRIPTION': section_description,
            'TOPIC': topic,
            'PAPER LIST': paper_texts
        }
        return PromptGenerator.generate_prompt(SUBSECTION_OUTLINE_PROMPT, params)

    @staticmethod
    def generate_edit_final_outline_prompt(outline):
        params = {
            'OVERALL OUTLINE': outline
        }
        return PromptGenerator.generate_prompt(EDIT_FINAL_OUTLINE_PROMPT, params)

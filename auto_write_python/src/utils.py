import os
from typing import List
import threading
import tiktoken
from tqdm import trange
import time
import requests
import random
import json
import logging

class tokenCounter():

    def __init__(self) -> None:
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.model_price = {}
        
    def num_tokens_from_string(self, string:str) -> int:
        return len(self.encoding.encode(string))

    def num_tokens_from_list_string(self, list_string):
        num = 0
        for i, s in enumerate(list_string):
            try:
                # Convert to string if not already a string
                s = str(s) if not isinstance(s, str) else s
                num += len(self.encoding.encode(s))
            except Exception as e:
                logging.error(f"Error processing item {i} in list_string: {e}")
                logging.error(f"Problematic item: {s}")
                raise  # Re-raise the exception after logging
        return num
    
    def compute_price(self, input_tokens, output_tokens, model):
        return (input_tokens/1000) * self.model_price[model][0] + (output_tokens/1000) * self.model_price[model][1]

    def text_truncation(self,text, max_len = 1000):
        encoded_id = self.encoding.encode(text, disallowed_special=())
        return self.encoding.decode(encoded_id[:min(max_len,len(encoded_id))])
 
def extract_title_sections_descriptions(outline):
    title = outline.split('Title: ')[1].split('\n')[0]
    sections, descriptions = [], []
    for i in range(100):
        if f'Section {i+1}' in outline:
            sections.append(outline.split(f'Section {i+1}: ')[1].split('\n')[0])
            descriptions.append(outline.split(f'Description {i+1}: ')[1].split('\n')[0])
    return title, sections, descriptions


def extract_sections(outline):
    sections = []
    lines = outline.split('\n')
    for line in lines:
        if line.startswith('Section'):
            sections.append(line.split(': ', 1)[-1].strip())
    return sections

def extract_subsections_subdescriptions(outline):
    subsections, subdescriptions = [], []
    lines = outline.split('\n')
    current_subsection = None
    current_description = None

    for line in lines:
        if line.startswith('Subsection'):
            if current_subsection:
                subsections.append(current_subsection)
                subdescriptions.append(current_description or '')
            current_subsection = line.split(': ', 1)[-1].strip()
            current_description = None
        elif line.startswith('Description'):
            current_description = line.split(': ', 1)[-1].strip()

    if current_subsection:
        subsections.append(current_subsection)
        subdescriptions.append(current_description or '')

    return subsections, subdescriptions

def chunking(papers, titles, chunk_size=14000, encoding=None):
    if encoding is None:
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    
    paper_chunks, title_chunks = [], []
    total_length = sum(len(encoding.encode(paper)) for paper in papers)
    num_of_chunks = max(1, int(total_length / chunk_size))
    avg_len = int(total_length / num_of_chunks) + 1
    
    current_chunk_papers, current_chunk_titles = [], []
    current_length = 0
    
    for paper, title in zip(papers, titles):
        paper_length = len(encoding.encode(paper))
        if current_length + paper_length > avg_len and current_chunk_papers:
            paper_chunks.append(current_chunk_papers)
            title_chunks.append(current_chunk_titles)
            current_chunk_papers, current_chunk_titles = [], []
            current_length = 0
        
        current_chunk_papers.append(paper)
        current_chunk_titles.append(title)
        current_length += paper_length
    
    if current_chunk_papers:
        paper_chunks.append(current_chunk_papers)
        title_chunks.append(current_chunk_titles)
    
    return paper_chunks, title_chunks

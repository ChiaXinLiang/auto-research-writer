import json
from collections import Counter
import os
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv('.env.local')

# Get the dataset path from the environment variable
dataset_path = os.getenv('DATASET_PATH')

def get_cs_stats_papers():
    cs_stats_papers = 0
    with open(dataset_path, 'r') as file:
        for line in file:
            paper = json.loads(line)
            categories = paper.get('categories', '').split()
            if any(cat.startswith(('stat.')) for cat in categories):
                cs_stats_papers += 1
    return cs_stats_papers

def show_cs_stats_papers():
    print("Number of papers in Statistics:")
    paper_count = get_cs_stats_papers()
    print(f"Total: {paper_count}")

if __name__ == "__main__":
    show_cs_stats_papers()

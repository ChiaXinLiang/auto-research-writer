from sentence_transformers import SentenceTransformer
import torch
import json

# model_choose = "sentence-transformers/all-distilroberta-v1"
model_choose = "nomic-ai/nomic-embed-text-v1.5"


embedding_model = SentenceTransformer(model_choose, trust_remote_code=True)
embedding_model.to(torch.device('mps'))

def get_encode_vector():
    encode_vector = []
    with open('./dataset/arxiv-metadata-oai-snapshot.json', 'r') as file:
        for index, line in enumerate(file):
            paper = json.loads(line)
            abstract = paper.get('abstract', '')
            title = paper.get('title', '')
            if abstract:
                encoded = embedding_model.encode(abstract)
                encode_vector.append(encoded)
                print(f"Index: {index}, Title: {title}, Vector Count: {len(encoded)}")
    return encode_vector

encode_vector = get_encode_vector()

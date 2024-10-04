import os
from dotenv import load_dotenv
from supabase import create_client, Client
import json
from sentence_transformers import SentenceTransformer
import torch

def initialize_supabase():
    load_dotenv('.env.local')
    model_choose = "nomic-ai/nomic-embed-text-v1.5"
    embedding_model = SentenceTransformer(model_choose, trust_remote_code=True)
    embedding_model.to(torch.device('mps'))
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase, embedding_model

def insert_document(supabase, content: str, metadata: dict, embedding: list):
    data = supabase.table("documents").insert({
        "content": content,
        "metadata": metadata,
        "embedding": embedding
    }).execute()
    return data

def search_documents(supabase, query_embedding: list, match_threshold: float = 0.8, match_count: int = 10):
    data = supabase.rpc(
        'match_documents',
        {
            'query_embedding': query_embedding,
            'match_threshold': match_threshold,
            'match_count': match_count
        }
    ).execute()
    return data

def get_dataset():
    load_dotenv('.env.local')
    dataset_path = os.environ.get("DATASET_PATH")
    if dataset_path:
        with open(dataset_path, 'r') as file:
            dataset = [json.loads(line) for line in file]
        return dataset
    else:
        print("Error: DATASET_PATH not found in environment variables.")
        return None



def filter_dataset(dataset, category):
    filtered_data = []
    for paper in dataset:
        # Check if all required fields are present
        required_fields = ['id', 'submitter', 'authors', 'title', 'comments', 'journal-ref', 'doi', 'abstract', 'categories', 'versions']
        if all(field in paper for field in required_fields):
            categories = paper['categories'].split()
            if category in ['cs', 'math', 'physics', 'q-bio', 'q-fin', 'stat', 'eess', 'econ']:
                # If category is a main category, include all papers with any subcategory
                if any(cat.startswith(f'{category}.') for cat in categories):
                    filtered_data.append(paper)
            elif '.' in category:
                # For specific subcategories (e.g., 'cs.AI'), only include exact matches
                if category in categories:
                    filtered_data.append(paper)
            else:
                # For other categories without subcategories, include exact matches
                if category in categories:
                    filtered_data.append(paper)
    return filtered_data

def get_filtered_dataset(category='cs'):
    dataset = get_dataset()
    if dataset:
        return filter_dataset(dataset, category)
    else:
        return None
    
def get_document(embedding_model, paper):
    # Prepare content
    content = f"Topic: {paper['title'].replace('\n', '')} \n Abstract: {paper['abstract'].replace('\n', '')}"
    # Prepare metadata
    metadata = {
        'title': paper['title'].replace('\n', ''),
        'authors': paper['authors'],
        'categories': paper['categories'],
        'id': paper['id'],
        'doi': paper['doi'],
        'journal_ref': paper['journal-ref'],
        'update_date': paper['versions'][-1]['created']
    }
    
    # Generate embedding
    embedding = embedding_model.encode(content)
    
    return embedding, metadata, content

def insert_document_by_index(supabase, embedding, metadata, content):
    insert_document(supabase, embedding, metadata, content)
    print(f"Inserted document: {metadata['title']}")

def delete_all_documents(supabase):
    try:
        # Delete all rows from the 'documents' table
        response = supabase.table('documents').delete().neq('id', 0).execute()

        
        # Check if the deletion was successful
        if response.data is not None:
            print(f"Deleted {len(response.data)} documents from Supabase.")
        else:
            print("No documents were deleted or an error occurred.")
        
        return response
    except Exception as e:
        print(f"An error occurred while deleting documents: {str(e)}")
        return None

def initialize():
    supabase, embedding_model = initialize_supabase()
    dataset = get_dataset()
    return supabase, embedding_model, dataset

def filter_papers(dataset, categories):
    combined_papers = []
    for category in categories:
        filtered_papers = filter_dataset(dataset, category)
        combined_papers.extend(filtered_papers)
        print(f"Total {category} papers: {len(filtered_papers)}")
    print(f"Total combined papers: {len(combined_papers)}")
    return combined_papers

def insert_papers(supabase, embedding_model, papers):
    total_papers = len(papers)
    inserted_papers = 0
    for index, paper in enumerate(papers, 1):
        paper_id = paper['id']
        existing_paper = supabase.table('documents').select('id').eq('metadata->>id', paper_id).execute()
        
        if not existing_paper.data:
            embedding, metadata, content = get_document(embedding_model, paper)
            insert_document(supabase, content, metadata, embedding.tolist())
            print(f"Inserted paper {index}: {paper['title']}")
            inserted_papers += 1
        else:
            print(f"Skipped paper {index}: {paper['title']} (already exists)")
    
    print(f"Inserted {inserted_papers} out of {total_papers} papers into Supabase")

def get_papers_and_insert(categories):
    supabase, embedding_model, dataset = initialize()
    if dataset:
        combined_papers = filter_papers(dataset, categories)
        insert_papers(supabase, embedding_model, combined_papers)
        return combined_papers
    else:
        print("Error: Unable to load dataset")
        return None
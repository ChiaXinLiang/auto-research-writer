import os
from dotenv import load_dotenv
from supabase import create_client, Client
import json
from sentence_transformers import SentenceTransformer
import torch
from tqdm import tqdm
from datetime import datetime

def initialize_supabase():
    load_dotenv('.env.local')
    model_choose = "nomic-ai/nomic-embed-text-v1.5"
    embedding_model = SentenceTransformer(model_choose, trust_remote_code=True)
    embedding_model.to(torch.device('mps'))
    #
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    print(f"Supabase URL: {url}")
    print(f"Supabase Key: {key}")
    supabase: Client = create_client(url, key)
    return supabase, embedding_model

def insert_documents_batch(supabase, documents):
    try:
        documents_table_name = os.environ.get("DOCUMENTS_TABLE_NAME")
        # Convert datetime objects to ISO format strings
        for doc in documents:
            if 'update_date' in doc and isinstance(doc['update_date'], datetime):
                doc['update_date'] = doc['update_date'].isoformat()
        data = supabase.table(documents_table_name).insert(documents).execute()
        return data
    except Exception as e:
        print(f"Error inserting batch: {str(e)}")
        return None

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
    # Prepare content for embedding
    content = f"{paper['abstract'].replace('\n', '')}"
    
    # Generate embedding
    embedding = embedding_model.encode(content)
    # print(paper)
    # Prepare document data according to the schema
    document = {
        "paper_id": paper['id'],
        "title": paper['title'].replace('\n', ''),
        "authors": paper['authors'].split(', '),  # Convert string to array
        "categories": paper['categories'].split(),  # Convert string to array
        "abstract": paper['abstract'].replace('\n', ''),
        "update_date": datetime.strptime(paper['update_date'], "%Y-%m-%d"),  # Keep as datetime object
        "journal_ref": paper.get('journal-ref'),
        "doi": paper.get('doi'),
        "metadata": json.dumps({
            "submitter": paper['submitter'],
            "comments": paper.get('comments'),
            "versions": paper['versions'],
            "report_no": paper.get('report-no'),
            "license": paper.get('license'),
            "authors_parsed": paper.get('authors_parsed', [])
        }),
        "embedding": embedding.tolist()
    }
    
    # Remove None values from the document
    document = {k: v for k, v in document.items() if v is not None}
    document['metadata'] = json.dumps({k: v for k, v in json.loads(document['metadata']).items() if v is not None})
    return document

def delete_all_documents(supabase):
    try:
        # Delete all rows from the table
        documents_table_name = os.environ.get("DOCUMENTS_TABLE_NAME")
        response = supabase.table(documents_table_name).delete().neq('id', 0).execute()
        
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
    batch_size = 100  # Adjust this value based on your needs
    documents_table_name = os.environ.get("DOCUMENTS_TABLE_NAME")
    
    for i in tqdm(range(0, total_papers, batch_size), desc="Inserting papers"):
        # if i % (5 * batch_size) == 0:
        #     # Reinitialize Supabase every 5 batches
        #     supabase, _ = initialize_supabase()
        
        batch = papers[i:i+batch_size]
        documents_to_insert = []
        
        # Get all existing paper IDs in this batch
        paper_ids = [paper['id'] for paper in batch]
        existing_papers = supabase.table(documents_table_name).select('paper_id').in_('paper_id', paper_ids).execute()
        existing_ids = set(paper['paper_id'] for paper in existing_papers.data)
        
        print(f"Number of existing papers in this batch: {len(existing_ids)}")
        
        for paper in batch:
            paper_id = paper['id']
            if paper_id not in existing_ids:
                document = get_document(embedding_model, paper)
                documents_to_insert.append(document)
                inserted_papers += 1
        
        if documents_to_insert:
            result = insert_documents_batch(supabase, documents_to_insert)
            if result is None:
                print(f"Failed to insert batch starting at index {i}")
    
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
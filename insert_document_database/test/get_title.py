from supabase import create_client
import time
from sentence_transformers import SentenceTransformer
import torch

url = "http://45.76.222.23:8000"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ewogICJyb2xlIjogImFub24iLAogICJpc3MiOiAic3VwYWJhc2UiLAogICJpYXQiOiAxNzI4MDU3NjAwLAogICJleHAiOiAxODg1ODI0MDAwCn0.Xf52RhaQ7n0CEDPhW12rGnPFN2qceYolZDyQ21Mk-y8"
supabase = create_client(url, key)

# Initialize the SentenceTransformer model
model_choose = "nomic-ai/nomic-embed-text-v1.5"
embedding_model = SentenceTransformer(model_choose, trust_remote_code=True)
embedding_model.to(torch.device('mps'))

# Query to search with
query = "Calculating Valid Domains for BDD-Based Interactive Configuration"

# Generate query embedding using SentenceTransformer
query_embedding = embedding_model.encode(query).tolist()

# Start timing
start_time = time.time()

# Execute the query
response = supabase.rpc(
    'match_arxiv_documents',
    {
        'query_embedding': query_embedding,
        'match_threshold': 0.7,
        'match_count': 1,
        'filters':{
            'start_date': '2009-03-03T00:00:00Z'
        }
    }
).execute()

# End timing
end_time = time.time()

data = response.data

print("query:", query)
print("Number of retrieved documents:", len(data))
if data:
    print(data)
else:
    print("No documents retrieved.")

# Calculate and print the time taken
time_taken = end_time - start_time
print(f"Time taken to retrieve data: {time_taken:.4f} seconds")
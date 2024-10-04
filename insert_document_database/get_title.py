from utils import initialize_supabase

supabase, embedding_model = initialize_supabase()
# Assuming we have a query embedding to search with
query_embedding = embedding_model.encode("what is AI?")

response = supabase.rpc(
    'match_documents',
    {
        'query_embedding': query_embedding.tolist(),
        'match_count': 10,
        'filter': {}  # Add an empty filter as default
    }
).execute()

data = response.data
print(data[0])

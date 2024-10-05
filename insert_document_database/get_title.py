from utils import initialize_supabase
import time

supabase, embedding_model = initialize_supabase()

# Assuming we have a query embedding to search with
query = "Minimax rates for cost-sensitive learning on manifolds with approximate  nearest neighbours"
query_embedding = embedding_model.encode(query)
# print(f"Query embedding for '{query}':")
# print(query_embedding)

# Start timing
start_time = time.time()

response = supabase.rpc(
    'match_documents',
    {
        'query_embedding': query_embedding.tolist(),
        'match_threshold': 0.7, 
        'match_count': 1,
    }
).execute()

# End timing
end_time = time.time()

data = response.data
print("Retrieved data:")
print(data)

# Calculate and print the time taken
time_taken = end_time - start_time
print(f"Time taken to retrieve data: {time_taken:.4f} seconds")

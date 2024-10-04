from utils import get_papers_and_insert

# Define the categories you want to filter
categories_to_filter = ['cs.AI', 'cs.CL', 'cs.CV', 'cs.LG', 'stat.ML']  # Categories related to multimodal large language models

# Get papers, filter them, and insert into Supabase
filtered_papers = get_papers_and_insert(categories_to_filter)

if filtered_papers:
    print(f"Total papers inserted: {len(filtered_papers)}")
    print(f"First paper title: {filtered_papers[0]['title']}")
else:
    print("No papers were processed or an error occurred.")

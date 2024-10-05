from nomic import atlas


# Access the arXiv dataset
arxiv_dataset = atlas.map_data(data="arxiv")
# Perform a semantic search
results = arxiv_dataset.search("quantum computing", k=10)

# Explore topics
topics = arxiv_dataset.get_topics()
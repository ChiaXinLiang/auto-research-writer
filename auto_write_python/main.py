from src.ChatModel.OllamaChat import OllamaChat
from src.Writer.Writer import Writer
import os
from dotenv import load_dotenv
from Database import Supabase
from src.utils import chunking

def main():
    load_dotenv('.env.local')
    model = "llama3.1:8b"  # or any other Ollama model
    api_key = ""  # Ollama typically doesn't require an API key for local usage
    ollama_url = os.getenv('OLLAMA_URL')  # Get the Ollama URL from the environment variable

    # Initialize the Supabase database
    Supabase.initialize()

    writer = Writer(model, api_key=api_key, chat_provider="ollama", url_key=ollama_url)

    # Example usage
    topic = "The Impact of Artificial Intelligence on Modern Society"
    
    # Use Supabase to get abstract chunks and title chunks
    search_results = Supabase.search_documents(topic, match_count=1500)  # Adjust match_count as needed
    
    references_papers = [result['abstract'] for result in search_results]
    references_titles = [result['title'] for result in search_results]
    papers_chunks, titles_chunks = chunking(references_papers, references_titles, chunk_size=14000)
    # print(titles_chunks)

    print(f"Retrieved {len(papers_chunks)} papers related to the topic.")

    # Generate rough outlines
    outlines = writer.generate_rough_outlines(topic, papers_chunks, titles_chunks)
    print("Generated Rough Outlines:")
    for i, outline in enumerate(outlines):
        # print(outline)
        print()

    # Merge outlines
    merged_outline = writer.merge_outlines(topic, outlines)
    print(merged_outline)
    print()

    # Generate subsection outlines
    rag_num = 100  # Number of papers to retrieve for each section
    sub_outlines = writer.generate_subsection_outlines(topic, merged_outline, rag_num)
    print("Subsection Outlines:")
    for i, sub_outline in enumerate(sub_outlines):
        print(f"Subsection Outline {i + 1}:")
        print(sub_outline)
        print()

    # Process outlines
    processed_outline = writer.process_outlines(merged_outline, sub_outlines)
    print("Processed Outline:")
    print(processed_outline)
    print()

    # Edit final outline
    final_outline = writer.edit_final_outline(processed_outline)
    print("Final Outline:")
    print(final_outline)

if __name__ == "__main__":
    main()

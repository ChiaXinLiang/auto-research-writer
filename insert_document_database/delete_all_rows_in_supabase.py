from utils import initialize_supabase, delete_all_documents

def main():
    # Initialize Supabase client
    supabase, _ = initialize_supabase()

    # Delete all documents
    result = delete_all_documents(supabase)

    if result:
        print("All documents have been deleted from Supabase.")
    else:
        print("An error occurred while deleting documents.")

if __name__ == "__main__":
    main()

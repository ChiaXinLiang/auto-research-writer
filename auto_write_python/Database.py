import os
from dotenv import load_dotenv
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
import logging
from sentence_transformers import SentenceTransformer

class Supabase:
    client: Client = None
    embedding_model = None

    @staticmethod
    def initialize():
        if Supabase.client is None:
            load_dotenv('.env.local')
            url: str = os.environ.get("SUPABASE_URL")
            key: str = os.environ.get("SUPABASE_KEY")
            if not url or not key:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env.local")
            opts = ClientOptions().replace(postgrest_client_timeout=60)
            Supabase.client = create_client(url, key, options=opts)
        if Supabase.embedding_model is None:
            Supabase.embedding_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)

    @staticmethod
    def execute_query(query_func):
        try:
            Supabase.initialize()
            return query_func()
        except Exception as e:
            logging.error(f"Error executing query: {str(e)}")
            return None

    @staticmethod
    def insert(table: str, data: dict):
        return Supabase.execute_query(lambda: Supabase.client.table(table).insert(data).execute().data)

    @staticmethod
    def select(table: str, columns: str = "*"):
        return Supabase.execute_query(lambda: Supabase.client.table(table).select(columns).execute().data)

    @staticmethod
    def update(table: str, data: dict, match_column: str, match_value: str):
        return Supabase.execute_query(lambda: Supabase.client.table(table).update(data).eq(match_column, match_value).execute().data)

    @staticmethod
    def delete(table: str, match_column: str, match_value: str):
        return Supabase.execute_query(lambda: Supabase.client.table(table).delete().eq(match_column, match_value).execute().data)

    @staticmethod
    def rpc(function_name: str, params: dict):
        return Supabase.execute_query(lambda: Supabase.client.rpc(function_name, params).execute().data)

    @staticmethod
    def search_documents(query: str, match_count: int = 100, match_threshold: float = 0.5):
        query_embedding = Supabase.embedding_model.encode(query).tolist()
        response = Supabase.client.rpc('match_documents', {
            'query_embedding': query_embedding,
            'match_count': match_count,
            'match_threshold': match_threshold,
            'filter': {}  # Add an empty filter as default
        }).execute()
        
        results = []
        for item in response.data:
            results.append({
                'abstract': item['content'],
                'title': item['metadata']['title']
            })
        return results

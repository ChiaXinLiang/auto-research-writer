from .ChatModel import ChatModel
import requests
import json

class OllamaChat(ChatModel):
    base_url = None
    model = None

    @classmethod
    def initialize(cls, model: str, base_url: str = "http://localhost:11434") -> None:
        cls.base_url = base_url
        cls.model = model

    @classmethod
    def generate(cls, text: str, temperature: float = 1, max_tokens: int = 250) -> str:
        if not cls.model:
            raise ValueError("OllamaChat not initialized. Call initialize() first.")
        
        url = f"{cls.base_url}/api/generate"
        payload = {
            "model": cls.model,
            "prompt": text,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        # Ollama returns streaming responses, so we need to accumulate them
        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                response_data = json.loads(decoded_line)
                full_response += response_data.get('response', '')
        
        return full_response.strip()

    @classmethod
    def batch_generate(cls, text_batch: list[str], temperature: float = 0, max_tokens: int = 250) -> list[str]:
        return [cls.generate(text, temperature, max_tokens) for text in text_batch]

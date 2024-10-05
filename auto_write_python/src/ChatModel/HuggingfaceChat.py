from .ChatModel import ChatModel
from huggingface_hub import InferenceClient

class HuggingfaceChat(ChatModel):
    def __init__(self):
        self.client = None
        self.model = None

    def initialize(self, model: str, api_key: str) -> None:
        self.client = InferenceClient(api_key=api_key)
        self.model = model

    def generate(self, text: str, temperature: float = 5, max_tokens: int = 5000) -> str:
        if not self.client:
            raise ValueError("HuggingfaceChat not initialized. Call initialize() first.")
        messages = [{"role": "user", "content": text}]
        response = self.client.chat_completion(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        result = response.choices[0].message.content
        return result

    def batch_generate(self, text_batch: list[str], temperature: float = 0, max_tokens: int = 250) -> list[str]:
        results = []
        for text in text_batch:
            result = self.generate(text, temperature, max_tokens)
            results.append(result)
        return results
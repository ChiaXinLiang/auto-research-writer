from .ChatModel import ChatModel
import openai

class OpenAIChat(ChatModel):
    model = None

    @classmethod
    def initialize(cls, model: str, api_key: str) -> None:
        openai.api_key = api_key
        cls.model = model

    @classmethod
    def generate(cls, text: str, temperature: float = 1, max_tokens: int = 250) -> str:
        if not cls.model:
            raise ValueError("OpenAIChat not initialized. Call initialize() first.")
        response = openai.ChatCompletion.create(
            model=cls.model,
            messages=[{"role": "user", "content": text}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    @classmethod
    def batch_generate(cls, text_batch: list[str], temperature: float = 0, max_tokens: int = 250) -> list[str]:
        return [cls.generate(text, temperature, max_tokens) for text in text_batch]
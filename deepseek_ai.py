from ai_interface import AIInterface
from openai import OpenAI

class DeepSeekAI(AIInterface):
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://api.deepseek.com",
            api_key=api_key,
        )
        self.model_name = "deepseek-chat"

    def get_answer(self, question: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": question},
            ],
        )
        return completion.choices[0].message.content

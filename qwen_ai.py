from ai_interface import AIInterface
from openai import OpenAI

class QwenAI(AIInterface):
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=api_key,
        )
        self.model_name = "qwen-long"

    def get_answer(self, question: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "你是一个有用的助手。"},
                {"role": "user", "content": question},
            ],
        )
        return completion.choices[0].message.content

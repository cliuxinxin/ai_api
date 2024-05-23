from ai_interface import AIInterface
from zhipuai import ZhipuAI as ZhipuAPI

class ZhipuClient(AIInterface):
    def __init__(self, api_key):
        self.client = ZhipuAPI(api_key=api_key)

    def get_answer(self, question):
        messages = [
            {"role": "user", "content": question}
        ]
        response = self.client.chat.completions.create(
            model="glm-3-turbo",
            messages=messages
        )
        return response.choices[0].message.content

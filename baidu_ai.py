import requests
import json

class BaiduAI:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = self.get_access_token()
        self.base_url = f'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token={self.access_token}'
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.messages = []

    def get_access_token(self):
        auth_url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}'
        response = requests.get(auth_url)
        response_data = response.json()
        access_token = response_data.get('access_token')
        if not access_token:
            raise Exception("Unable to retrieve access token")
        return access_token

    def get_answer(self, question):
        self.messages.append({"role": "user", "content": question})
        data = {
            "messages": self.messages
        }
        response = requests.post(self.base_url, headers=self.headers, data=json.dumps(data))
        result = response.json()
        answer = result.get('result', '')
        # 将助手的回答加入消息列表中
        self.messages.append({"role": "assistant", "content": answer})
        return answer
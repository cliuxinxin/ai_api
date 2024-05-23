from ai_interface import AIInterface
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models
import json

class TencentAI(AIInterface):
    def __init__(self, secret_id, secret_key, region='ap-guangzhou', model='hunyuan-lite'):
        self.cred = credential.Credential(secret_id, secret_key)
        http_profile = HttpProfile()
        http_profile.endpoint = "hunyuan.tencentcloudapi.com"

        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile

        self.client = hunyuan_client.HunyuanClient(self.cred, region, client_profile)
        self.model = model
        self.messages = []

    def get_answer(self, question):
        self.messages.append({"Role": "system", "Content": "你是一个有用的助手。"})
        self.messages.append({"Role": "user", "Content": question})

        req = models.ChatCompletionsRequest()
        params = {
            "Action": "ChatCompletions",
            "Version": "2023-09-01",
            "Model": self.model,
            "Messages": self.messages,
            "TopP": 1.0,
            "Temperature": 1.0,
            "Stream": False
        }
        req.from_json_string(json.dumps(params))

        try:
            resp = self.client.ChatCompletions(req)
            result = json.loads(resp.to_json_string())
            answer = result['Choices'][0]['Message']['Content']
            self.messages.append({"Role": "assistant", "Content": answer})
            return answer
        except Exception as e:
            print(e)
            return None

from ai_interface import AIInterface
import _thread as thread
import time
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse, urlencode
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import ssl
import websocket

class Ws_Param:
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    def create_url(self):
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        signature_origin = "host: " + self.host + "\n" + "date: " + date + "\n" + "GET " + self.path + " HTTP/1.1"
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'), digestmod=hashlib.sha256).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        v = {"authorization": authorization, "date": date, "host": self.host}
        url = self.gpt_url + '?' + urlencode(v)
        return url

class SparkAI(AIInterface):
    def __init__(self, appid, api_key, api_secret, gpt_url):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        self.gpt_url = gpt_url
        self.answer = ""

    def create_url(self):
        ws_param = Ws_Param(self.appid, self.api_key, self.api_secret, self.gpt_url)
        return ws_param.create_url()

    def get_answer(self, question):
        ws_url = self.create_url()

        def on_error(ws, error):
            print("### error:", error)

        def on_close(ws, close_status_code, close_msg):
            pass

        def on_open(ws):
            def run(*args):
                data = {
                    "header": {"app_id": ws.appid},
                    "parameter": {"chat": {"domain": ws.domain, "temperature": 0.5, "max_tokens": 4096}},
                    "payload": {"message": {"text": [{"role": "user", "content": ws.query}]}}
                }
                ws.send(json.dumps(data))
            thread.start_new_thread(run, ())

        def on_message(ws, message):
            data = json.loads(message)
            code = data['header']['code']
            if code != 0:
                print(f'请求错误: {code}, {data}')
                ws.close()
            else:
                choices = data["payload"]["choices"]
                status = choices["status"]
                content = choices["text"][0]["content"]
                self.answer += content
                if status == 2:
                    ws.close()

        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
        ws.appid = self.appid
        ws.query = question
        ws.domain = "general"
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

        # 等待响应
        while not self.answer:
            time.sleep(0.1)

        return self.answer

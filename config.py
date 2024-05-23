from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

api_key_qwen = os.getenv("API_KEY_QWEN")
api_key_deepseek = os.getenv("API_KEY_DEEPSEEK")
api_key_baidu = os.getenv("API_KEY_BAIDU")
secret_key_baidu = os.getenv("SECRET_KEY_BAIDU")
secret_id_hunyuan = os.getenv("SECRET_ID_HUNYUAN")
secret_key_hunyuan = os.getenv("SECRET_KEY_HUNYUAN")
api_key_zhipu = os.getenv("API_KEY_ZHIPU")
APPID_spark = os.getenv("APPID_SPARK")
APIKey_spark = os.getenv("APIKey_SPARK")
APISecret_spark = os.getenv("APISecret_SPARK")


from qwen_ai import QwenAI
from deepseek_ai import DeepSeekAI
from baidu_ai import BaiduAI
from tencent_ai import TencentAI
from zhipu_ai import ZhipuClient
from spark_ai import SparkAI
import config

def main():
    # 初始化各个AI接口
    qwen_ai = QwenAI(config.api_key_qwen)
    deepseek_ai = DeepSeekAI(config.api_key_deepseek)
    baidu_ai = BaiduAI(config.api_key_baidu, config.secret_key_baidu)
    tencent_ai = TencentAI(config.secret_id_hunyuan, config.secret_key_hunyuan)
    zhipu_ai = ZhipuClient(config.api_key_zhipu)
    spark_ai = SparkAI(config.APPID_spark, config.APIKey_spark, config.APISecret_spark, "wss://spark-api.xf-yun.com/v1.1/chat")

    # 测试各个接口
    question = "你是谁？"
    print("QwenAI:", qwen_ai.get_answer(question))
    print("DeepSeekAI:", deepseek_ai.get_answer(question))
    print("BaiduAI:", baidu_ai.get_answer(question))
    print("TencentAI:", tencent_ai.get_answer(question))
    print("ZhipuAI:", zhipu_ai.get_answer(question))
    print("SparkAI:", spark_ai.get_answer(question))

if __name__ == "__main__":
    main()

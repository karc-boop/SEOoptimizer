from typing import List
from google.cloud import aiplatform
from config.config import settings

class NameGenerator:
    def __init__(self):
        # 初始化 Vertex AI
        aiplatform.init(
            project=settings.PROJECT_ID,
            location=settings.LOCATION,
        )
        
    def generate(self, keywords: List[str]) -> str:
        """使用 Google Vertex AI 生成产品名称"""
        # 构建提示
        prompt = self._build_prompt(keywords)
        
        # 获取预测客户端
        model = aiplatform.TextGenerationModel.from_pretrained(settings.MODEL_NAME)
        
        # 生成响应
        response = model.predict(
            prompt,
            temperature=settings.TEMPERATURE,
            max_output_tokens=settings.MAX_OUTPUT_TOKENS,
        )
        
        # 处理并返回生成的名称
        return self._process_response(response)
    
    def _build_prompt(self, keywords: List[str]) -> str:
        """构建提示模板"""
        keywords_str = ", ".join(keywords)
        return (
            f"Generate a catchy and marketable product name based on these keywords: {keywords_str}.\n"
            "The name should be concise, memorable, and appealing to customers.\n"
            "Product name:"
        )
    
    def _process_response(self, response) -> str:
        """处理模型响应"""
        # 清理和格式化响应
        generated_name = response.text.strip()
        # 可以添加额外的处理逻辑
        return generated_name 
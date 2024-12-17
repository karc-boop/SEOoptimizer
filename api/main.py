from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.text_processing.text_preprocessor import TextPreprocessor
from src.keyword_matching.keyword_matcher import KeywordMatcher
from src.product_naming.name_generator import NameGenerator
from database.database import get_db
from typing import List

app = FastAPI()

class ProductRequest(BaseModel):
    description: str

class ProductResponse(BaseModel):
    product_name: str
    keywords: List[str]
    score: float

@app.post("/generate-product-name", response_model=ProductResponse)
async def generate_product_name(request: ProductRequest):
    try:
        # 1. 预处理文本
        preprocessor = TextPreprocessor()
        processed_text = preprocessor.process(request.description)
        
        # 2. 匹配关键词
        matcher = KeywordMatcher()
        keywords, score = matcher.match(processed_text)
        
        # 3. 生成产品名称
        generator = NameGenerator()
        product_name = generator.generate(keywords)
        
        return ProductResponse(
            product_name=product_name,
            keywords=keywords,
            score=score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 
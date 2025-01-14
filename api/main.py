from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.text_processing.text_preprocessor import TextPreprocessor
from src.keyword_matching.keyword_matcher import KeywordMatcher
from src.keyword_matching.keyword_repository import KeywordRepository
from src.product_naming.name_generator import NameGenerator
from database.database import get_db
from typing import List
import logging
import time
from config.logging_config import logger

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
        logger.info("Starting product name generation", extra={
            "description": request.description,
            "timestamp": time.time()
        })
        
        with get_db() as db:
            # Create repository and matcher
            repository = KeywordRepository(db)
            matcher = KeywordMatcher(repository)
            
            # Add request logging
            logging.info(f"Processing request: {request.description}")
            
            # Add timing metrics
            start_time = time.time()
            
            # 1. Preprocess text
            preprocessor = TextPreprocessor()
            processed_text = preprocessor.process(request.description)
            
            # 2. Match keywords
            keywords, score = matcher.match(processed_text['cleaned_text'])
            
            # 3. Generate product name
            generator = NameGenerator()
            product_name = generator.generate(keywords)
            
            if not product_name:
                raise HTTPException(status_code=500, detail="Failed to generate product name")
            
            logger.info("Request processed successfully", extra={
                "processing_time": f"{time.time() - start_time:.2f}s",
                "keywords": keywords,
                "score": score
            })
            return ProductResponse(
                product_name=product_name,
                keywords=keywords,
                score=score
            )
    except Exception as e:
        logger.error("Error in product name generation", extra={
            "error": str(e),
            "description": request.description
        })
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 
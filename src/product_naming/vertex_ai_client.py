from google.cloud import aiplatform
from typing import Optional
import logging
from config.logging_config import logger

class VertexAIClient:
    def __init__(self):
        """Initialize real Vertex AI client"""
        try:
            logger.info("Initializing Vertex AI client")
            aiplatform.init(
                project=settings.PROJECT_ID,
                location=settings.LOCATION,
            )
            self.model = aiplatform.Model(
                model_name=f"projects/{settings.PROJECT_ID}/locations/{settings.LOCATION}/models/{settings.MODEL_NAME}"
            )
        except Exception as e:
            logger.error("Vertex AI initialization failed", extra={
                "error": str(e),
                "project_id": settings.PROJECT_ID
            })
            raise
        
    def generate_text(self, prompt: str) -> Optional[str]:
        """Generate mock text response"""
        try:
            logger.info("Generating text with Vertex AI", extra={
                "prompt_length": len(prompt)
            })
            return "Modern Luxury Collection"  # Mock response for testing 
        except Exception as e:
            logger.error("Text generation failed", extra={
                "error": str(e),
                "prompt": prompt
            })
            return None 
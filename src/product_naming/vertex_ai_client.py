from google.cloud import aiplatform
from typing import Optional
from config.config import settings
import logging

class VertexAIClient:
    def __init__(self):
        """Initialize Vertex AI client"""
        try:
            aiplatform.init(
                project=settings.PROJECT_ID,
                location=settings.LOCATION,
            )
            self.model = aiplatform.TextGenerationModel.from_pretrained(
                settings.MODEL_NAME
            )
        except Exception as e:
            logging.error(f"Failed to initialize Vertex AI client: {e}")
            raise
    
    def generate_text(self, prompt: str) -> Optional[str]:
        """Generate text using Vertex AI"""
        try:
            response = self.model.predict(
                prompt,
                temperature=settings.TEMPERATURE,
                max_output_tokens=settings.MAX_OUTPUT_TOKENS,
            )
            return response.text.strip()
        except Exception as e:
            logging.error(f"Text generation failed: {e}")
            return None 
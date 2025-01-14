from typing import List, Optional
from .vertex_ai_client import VertexAIClient
import logging

class NameGenerator:
    def __init__(self):
        """Initialize name generator with Vertex AI client"""
        self.ai_client = VertexAIClient()
        
    def generate(self, keywords: List[str]) -> Optional[str]:
        """Generate product name based on keywords"""
        prompt = self._build_prompt(keywords)
        
        # Generate name using Vertex AI
        generated_name = self.ai_client.generate_text(prompt)
        
        if generated_name:
            return self._process_response(generated_name)
        return None
    
    def _build_prompt(self, keywords: List[str]) -> str:
        """Build prompt for the AI model"""
        keywords_str = ", ".join(keywords)
        return (
            "Generate a catchy and marketable product name based on these keywords:\n"
            f"Keywords: {keywords_str}\n\n"
            "Requirements:\n"
            "1. Name should be concise (1-3 words)\n"
            "2. Easy to remember and pronounce\n"
            "3. Reflect the product's key features\n"
            "4. Suitable for marketing\n\n"
            "Product name:"
        )
    
    def _process_response(self, response: str) -> str:
        """Process and clean the generated response"""
        # Remove any quotes or extra whitespace
        name = response.strip().strip('"\'')
        
        # Take only the first line if multiple lines are returned
        name = name.split('\n')[0]
        
        # Ensure proper capitalization
        return name.title() 
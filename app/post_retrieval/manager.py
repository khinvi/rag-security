# app/post_retrieval/manager.py
from typing import Dict, Any, List
from openai import OpenAI
from .content_assembly import ContentAssembler
from .validation import ResponseValidator
from ..monitoring.logger import SecurityLogger
from ..config import settings

class PostRetrievalManager:
    """Manages post-retrieval security for the RAG system"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.LLM_MODEL
        self.content_assembler = ContentAssembler()
        self.validator = ResponseValidator()
        self.logger = SecurityLogger()
        
    async def generate_secure_response(self, 
                                      user_query: str, 
                                      query_results: List[Dict],
                                      user_id: str = "anonymous") -> Dict:
        """Generate a secure response using retrieved context"""
        # Assemble context from retrieved documents
        context = self.content_assembler.assemble_context(query_results)
        
        # Create prompt with context
        prompt = self.content_assembler.create_prompt_with_context(user_query, context)
        
        # Generate response from LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a secure RAG system assistant. Only provide information from the given context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent responses
            max_tokens=500
        )
        
        response_text = response.choices[0].message.content
        
        # Validate response
        validation_result = self.validator.validate_response(response_text)
        
        # Log the validation
        self.logger.log_security_event(
            event_type="response_validation",
            user_id=user_id,
            validation_result=validation_result,
            is_valid=validation_result["is_valid"]
        )
        
        # Sanitize if needed
        final_response = self.validator.sanitize_response(response_text, validation_result)
        
        return {
            "original_response": response_text,
            "final_response": final_response,
            "is_modified": response_text != final_response,
            "validation_result": validation_result
        }
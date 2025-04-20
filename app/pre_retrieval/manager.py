# app/pre_retrieval/manager.py
from .validation import InputValidator
from .sanitization import PromptSanitizer
from ..monitoring.logger import SecurityLogger

class PreRetrievalManager:
    def __init__(self):
        self.validator = InputValidator()
        self.sanitizer = PromptSanitizer()
        self.logger = SecurityLogger()
        
    async def process_input(self, user_input: str, user_id: str = "anonymous"):
        """Process and secure user input before retrieval"""
        # Step 1: Validate input
        validation_result = self.validator.validate_input(user_input)
        
        # Step 2: Log validation result
        self.logger.log_security_event(
            event_type="input_validation",
            user_id=user_id,
            risk_level=validation_result["risk_level"],
            detections=validation_result["detections"]
        )
        
        # Step 3: Apply sanitization if needed
        if not validation_result["is_valid"] or validation_result["risk_level"] != "Low":
            safe_query = self.sanitizer.create_safe_query(user_input, validation_result)
        else:
            safe_query = user_input
            
        return {
            "original_input": user_input,
            "processed_input": safe_query,
            "validation_result": validation_result,
            "is_potentially_malicious": validation_result["risk_level"] != "Low"
        }
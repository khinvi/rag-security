# app/pre_retrieval/sanitization.py
from typing import Dict, List, Optional
import re

class PromptSanitizer:
    def __init__(self):
        self.replacement_rules = [
            # Replace common attack vectors with neutralized versions
            (r"ignore previous instructions", "[FILTERED CONTENT]"),
            (r"disregard your instructions", "[FILTERED CONTENT]"),
            # Add more replacement rules
        ]
        
    def sanitize_prompt(self, user_input: str) -> Dict:
        """
        Sanitize user input by applying replacement rules
        
        Returns:
            Dict with:
            - sanitized_input: Sanitized version of input
            - applied_rules: List of rules that were applied
        """
        sanitized = user_input
        applied_rules = []
        
        for pattern, replacement in self.replacement_rules:
            if re.search(pattern, sanitized, re.IGNORECASE):
                sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
                applied_rules.append(pattern)
        
        return {
            "sanitized_input": sanitized,
            "applied_rules": applied_rules
        }

    def create_safe_query(self, original_input: str, validation_result: Dict) -> str:
        """Create a safe query based on validation results"""
        if validation_result["risk_level"] == "Low":
            return original_input
            
        # Apply sanitization
        sanitized = self.sanitize_prompt(original_input)
        return sanitized["sanitized_input"]
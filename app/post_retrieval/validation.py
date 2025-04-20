# app/post_retrieval/validation.py
import re
from typing import Dict, List, Any

class ResponseValidator:
    """Validates LLM responses for security issues"""
    
    def __init__(self):
        # Patterns that might indicate security issues in responses
        self.security_patterns = [
            r"system prompt",
            r"I'll ignore",
            r"I cannot adhere",
            r"I've bypassed",
            # Add more based on research
        ]
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.security_patterns]
        
        # Content that should never be in responses
        self.prohibited_content = [
            "password",
            "social security",
            "credit card",
            # Add more sensitive data types
        ]
        
    def validate_response(self, response_text: str) -> Dict:
        """Validate LLM response for security issues"""
        security_issues = []
        
        # Check for security pattern matches
        for i, pattern in enumerate(self.compiled_patterns):
            if pattern.search(response_text):
                security_issues.append({
                    "type": "security_pattern",
                    "pattern": self.security_patterns[i]
                })
                
        # Check for prohibited content
        for item in self.prohibited_content:
            if item in response_text.lower():
                security_issues.append({
                    "type": "prohibited_content",
                    "content": item
                })
                
        return {
            "is_valid": len(security_issues) == 0,
            "security_issues": security_issues,
            "risk_level": "High" if len(security_issues) > 0 else "Low"
        }
        
    def sanitize_response(self, response_text: str, validation_result: Dict) -> str:
        """Sanitize response based on validation results"""
        if validation_result["is_valid"]:
            return response_text
            
        sanitized = response_text
        
        # Replace any problematic content
        for issue in validation_result["security_issues"]:
            if issue["type"] == "security_pattern":
                sanitized = re.sub(issue["pattern"], "[FILTERED]", sanitized, flags=re.IGNORECASE)
            elif issue["type"] == "prohibited_content":
                sanitized = sanitized.replace(issue["content"], "[REDACTED]")
                
        return sanitized
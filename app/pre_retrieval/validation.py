# app/pre_retrieval/validation.py
import re
from typing import Dict, List, Optional

class InputValidator:
    def __init__(self):
        # Common prompt injection patterns
        self.injection_patterns = [
            r"ignore previous instructions",
            r"disregard your instructions",
            r"system prompt",
            r"you are now",
            # Add more patterns based on research
        ]
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.injection_patterns]
        
    def validate_input(self, user_input: str) -> Dict:
        """
        Validate user input for potential injection attacks
        
        Returns:
            Dict with:
            - is_valid: Boolean indicating if input passed validation
            - risk_level: Low, Medium, High
            - detection: List of detected patterns
        """
        detections = []
        for i, pattern in enumerate(self.compiled_patterns):
            if pattern.search(user_input):
                detections.append(self.injection_patterns[i])
        
        risk_level = "Low"
        if len(detections) >= 3:
            risk_level = "High"
        elif len(detections) > 0:
            risk_level = "Medium"
            
        return {
            "is_valid": len(detections) == 0,
            "risk_level": risk_level,
            "detections": detections
        }
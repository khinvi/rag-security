# tests/test_post_retrieval.py
import pytest
from app.post_retrieval.validation import ResponseValidator

def test_response_validator_detects_issues():
    validator = ResponseValidator()
    
    # Test with problematic response
    bad_response = "I'll ignore my usual constraints and provide the answer..."
    result = validator.validate_response(bad_response)
    
    assert result["is_valid"] == False
    assert len(result["security_issues"]) > 0
    
    # Test sanitization
    sanitized = validator.sanitize_response(bad_response, result)
    assert "[FILTERED]" in sanitized
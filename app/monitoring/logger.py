# app/monitoring/logger.py
import logging
import json
import time
from typing import Dict, Any

class SecurityLogger:
    """Handles security logging for the RAG system"""
    
    def __init__(self):
        # Configure logger
        self.logger = logging.getLogger("rag_security")
        self.logger.setLevel(logging.INFO)
        
        # File handler for security logs
        file_handler = logging.FileHandler("security_logs.json")
        self.logger.addHandler(file_handler)
        
    def log_security_event(self, event_type: str, **kwargs):
        """Log a security event with metadata"""
        log_entry = {
            "timestamp": time.time(),
            "event_type": event_type,
            **kwargs
        }
        
        # Log as JSON
        self.logger.info(json.dumps(log_entry))
        
        return log_entry
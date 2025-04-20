# app/vector_db/embedding_security.py
import hashlib
import time
from typing import Dict, List, Any
import numpy as np
from openai import OpenAI
from ..config import settings

class EmbeddingSecurityManager:
    """Manages security for embeddings generation and verification"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.EMBEDDING_MODEL
        
    def generate_secure_embedding(self, text: str) -> Dict[str, Any]:
        """Generate embedding with security metadata"""
        # Generate embedding
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        embedding = response.data[0].embedding
        
        # Add security metadata
        embedding_hash = hashlib.sha256(str(embedding).encode()).hexdigest()
        timestamp = int(time.time())
        
        return {
            "embedding": embedding,
            "security_metadata": {
                "hash": embedding_hash,
                "timestamp": timestamp,
                "model": self.model
            }
        }
        
    def verify_embedding_integrity(self, embedding: List[float], security_metadata: Dict) -> bool:
        """Verify the integrity of an embedding using its security metadata"""
        if not security_metadata or "hash" not in security_metadata:
            return False
            
        # Regenerate hash
        current_hash = hashlib.sha256(str(embedding).encode()).hexdigest()
        
        # Verify hash
        return current_hash == security_metadata["hash"]
        
    def detect_anomalous_embedding(self, embedding: List[float]) -> bool:
        """Detect potentially anomalous or poisoned embeddings"""
        # Check for statistical anomalies
        embedding_array = np.array(embedding)
        
        # Check for unusual statistical properties
        mean = np.mean(embedding_array)
        std = np.std(embedding_array)
        
        # Embeddings typically have mean close to 0
        if abs(mean) > 0.1:
            return True
            
        # Unusually low variance might indicate poisoning
        if std < 0.01:
            return True
            
        return False
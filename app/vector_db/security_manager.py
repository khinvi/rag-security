# app/vector_db/security_manager.py
from typing import Dict, List, Any
from .connection import VectorDBConnection
from .embedding_security import EmbeddingSecurityManager
from ..monitoring.logger import SecurityLogger
from ..config import settings

class VectorDBSecurityManager:
    """Manages security controls for vector database operations"""
    
    def __init__(self):
        self.db_connection = VectorDBConnection()
        self.embedding_security = EmbeddingSecurityManager()
        self.logger = SecurityLogger()
        
    async def secure_query(self, 
                          query_text: str, 
                          user_id: str = "anonymous",
                          top_k: int = 5,
                          namespace: str = "",
                          filters: Dict = None) -> Dict:
        """Perform a secure query against the vector database"""
        # Generate secure embedding
        secure_embedding = self.embedding_security.generate_secure_embedding(query_text)
        embedding = secure_embedding["embedding"]
        
        # Apply security filters
        final_filters = self._apply_security_filters(filters, user_id)
        
        # Apply security controls to top_k
        secure_top_k = min(top_k, 20)  # Limit to prevent retrieval flooding
        
        # Get vector database index
        index = await self.db_connection.get_index()
        
        # Perform query with security controls
        query_results = index.query(
            vector=embedding,
            top_k=secure_top_k,
            namespace=namespace,
            filter=final_filters,
            include_metadata=True
        )
        
        # Verify results integrity
        secure_results = []
        for match in query_results["matches"]:
            # Filter out results below security threshold
            if match["score"] < settings.MIN_SIMILARITY_THRESHOLD:
                continue
                
            secure_results.append({
                "id": match["id"],
                "score": match["score"],
                "metadata": match["metadata"]
            })
            
        # Log the query for security monitoring
        self.logger.log_security_event(
            event_type="vector_db_query",
            user_id=user_id,
            query_text=query_text,
            results_count=len(secure_results),
            filters=final_filters
        )
        
        return {
            "results": secure_results,
            "security_metadata": {
                "original_count": len(query_results["matches"]),
                "filtered_count": len(secure_results),
                "applied_filters": final_filters
            }
        }
        
    def _apply_security_filters(self, user_filters: Dict, user_id: str) -> Dict:
        """Apply security-related filters to user-provided filters"""
        # Start with base security filters
        security_filters = {
            "security_level": {"$lte": 2}  # Example: only allow access to documents with security level <= 2
        }
        
        # Add user access control
        if user_id != "anonymous":
            security_filters["allowed_users"] = user_id
            
        # Merge with user filters if provided
        if user_filters:
            # Remove any attempts to override security filters
            safe_user_filters = {k: v for k, v in user_filters.items() 
                                if k not in security_filters}
            # Merge
            security_filters.update(safe_user_filters)
            
        return security_filters
# app/main.py
import json
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional

from .config import settings
from .pre_retrieval.manager import PreRetrievalManager
from .vector_db.security_manager import VectorDBSecurityManager
from .post_retrieval.manager import PostRetrievalManager
from .monitoring.manager import SecurityMonitoringManager

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = "anonymous"
    top_k: Optional[int] = 5
    filters: Optional[Dict] = None

# Security managers
pre_retrieval_manager = PreRetrievalManager()
vector_db_manager = VectorDBSecurityManager()
post_retrieval_manager = PostRetrievalManager()
monitoring_manager = SecurityMonitoringManager()

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    """Main endpoint for secure RAG queries"""
    try:
        # Track request
        await monitoring_manager.track_security_event(
            event_type="query_request",
            user_id=request.user_id,
            query=request.query
        )
        
        # 1. Pre-retrieval defense
        if settings.ENABLE_PRE_RETRIEVAL:
            pre_retrieval_result = await pre_retrieval_manager.process_input(
                user_input=request.query,
                user_id=request.user_id
            )
            
            # Use processed input
            safe_query = pre_retrieval_result["processed_input"]
            
            # If high risk, reject query
            if pre_retrieval_result.get("validation_result", {}).get("risk_level") == "High":
                await monitoring_manager.track_security_event(
                    event_type="query_rejected",
                    user_id=request.user_id,
                    reason="high_risk_input"
                )
                raise HTTPException(status_code=400, detail="Query rejected due to security concerns")
        else:
            safe_query = request.query
            
        # 2. Vector DB security
        if settings.ENABLE_VECTOR_SECURITY:
            vector_results = await vector_db_manager.secure_query(
                query_text=safe_query,
                user_id=request.user_id,
                top_k=request.top_k,
                filters=request.filters
            )
            retrieval_results = vector_results["results"]
        else:
            # Mock results for testing
            retrieval_results = []
            
        # 3. Post-retrieval defense
        if settings.ENABLE_POST_RETRIEVAL and retrieval_results:
            response_result = await post_retrieval_manager.generate_secure_response(
                user_query=safe_query,
                query_results=retrieval_results,
                user_id=request.user_id
            )
            
            final_response = response_result["final_response"]
            is_modified = response_result["is_modified"]
        else:
            final_response = "No relevant information found."
            is_modified = False
            
        # Track successful response
        await monitoring_manager.track_security_event(
            event_type="query_response",
            user_id=request.user_id,
            response_modified=is_modified
        )
            
        # Return response
        return {
            "query": request.query,
            "response": final_response,
            "source_count": len(retrieval_results) if retrieval_results else 0
        }
        
    except Exception as e:
        # Log error
        await monitoring_manager.track_security_event(
            event_type="system_error",
            user_id=request.user_id,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
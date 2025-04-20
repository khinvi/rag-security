# app/post_retrieval/content_assembly.py
from typing import Dict, List, Any

class ContentAssembler:
    """Securely assembles retrieved content for LLM context"""
    
    def __init__(self):
        # Maximum number of documents to include
        self.max_docs = 5
        # Maximum characters per document
        self.max_chars_per_doc = 1000
        
    def assemble_context(self, query_results: List[Dict]) -> Dict:
        """Assemble retrieved documents into a secure context"""
        # Limit number of documents
        limited_results = query_results[:min(len(query_results), self.max_docs)]
        
        assembled_docs = []
        
        for result in limited_results:
            # Extract content safely
            content = result.get("metadata", {}).get("text", "")
            
            # Truncate if too long
            if len(content) > self.max_chars_per_doc:
                content = content[:self.max_chars_per_doc] + "..."
                
            # Add document with source information
            assembled_docs.append({
                "content": content,
                "source": result.get("id", "unknown"),
                "relevance": result.get("score", 0)
            })
            
        return {
            "documents": assembled_docs,
            "document_count": len(assembled_docs)
        }
        
    def create_prompt_with_context(self, user_query: str, context: Dict) -> str:
        """Create a secure prompt with assembled context"""
        documents = context.get("documents", [])
        
        prompt = "Answer the question based on the provided context only. If the answer is not in the context, say 'I don't have information about that.'\n\n"
        
        prompt += "Context:\n"
        
        for i, doc in enumerate(documents):
            prompt += f"[Document {i+1}] {doc['content']}\n\n"
            
        prompt += f"Question: {user_query}\n"
        prompt += "Answer: "
        
        return prompt
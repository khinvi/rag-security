# app/vector_db/connection.py
import pinecone
from ..config import settings

class VectorDBConnection:
    """Manages secure connections to vector databases"""
    
    def __init__(self):
        self.db_type = settings.VECTOR_DB_TYPE
        self.index_name = settings.PINECONE_INDEX
        self.connection = None
        self.index = None
        
    async def connect(self):
        """Establish connection to vector database"""
        if self.db_type == "pinecone":
            pinecone.init(
                api_key=settings.PINECONE_API_KEY,
                environment=settings.PINECONE_ENVIRONMENT
            )
            
            # Create index if it doesn't exist
            if self.index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name=self.index_name,
                    dimension=1536,  # For OpenAI embedding models
                    metric="cosine"
                )
                
            self.index = pinecone.Index(self.index_name)
            self.connection = pinecone
            return self.index
        else:
            raise ValueError(f"Unsupported vector database type: {self.db_type}")
            
    async def get_index(self):
        """Get the vector database index"""
        if self.index is None:
            await self.connect()
        return self.index
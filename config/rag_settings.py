"""
RAG関連の設定
"""
import os
from typing import Dict, Any

class RAGSettings:
    """RAG設定クラス"""
    
    def __init__(self):
        self.vector_store_type = os.getenv("VECTOR_STORE_TYPE", "chroma")
        self.chroma_persist_directory = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
        self.faiss_index_path = os.getenv("FAISS_INDEX_PATH", "./faiss_index")
        
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "openai")  # openai or huggingface
        self.huggingface_model_name = os.getenv("HF_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
        
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "1000"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "200"))
        
        self.default_k = int(os.getenv("DEFAULT_K", "4"))
        self.similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
        
        self.rag_model = os.getenv("RAG_MODEL", "gpt-3.5-turbo")
        self.rag_temperature = float(os.getenv("RAG_TEMPERATURE", "0.7"))
        self.max_iterations = int(os.getenv("RAG_MAX_ITERATIONS", "10"))
        
        self.documents_directory = os.getenv("DOCUMENTS_DIR", "./documents")
    
    def get_vector_store_config(self) -> Dict[str, Any]:
        """ベクトルストア設定を取得"""
        config = {
            "store_type": self.vector_store_type
        }
        
        if self.vector_store_type == "chroma":
            config["persist_directory"] = self.chroma_persist_directory
        elif self.vector_store_type == "faiss":
            config["index_path"] = self.faiss_index_path
        
        return config
    
    def get_document_processor_config(self) -> Dict[str, Any]:
        """ドキュメントプロセッサー設定を取得"""
        return {
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        }
    
    def get_rag_agent_config(self) -> Dict[str, Any]:
        """RAGエージェント設定を取得"""
        return {
            "model": self.rag_model,
            "temperature": self.rag_temperature,
            "include_web_search": True,
            "include_custom_tools": True
        }
    
    def get_search_config(self) -> Dict[str, Any]:
        """検索設定を取得"""
        return {
            "k": self.default_k,
            "similarity_threshold": self.similarity_threshold
        }
    
    def validate(self) -> bool:
        """設定の妥当性をチェック"""
        if not os.getenv("OPENAI_API_KEY") and self.embedding_model == "openai":
            print("警告: OpenAIエンベディングを使用するにはOPENAI_API_KEYが必要です")
            return False
        
        if self.chunk_size <= 0:
            print("エラー: CHUNK_SIZEは正の値である必要があります")
            return False
        
        if self.chunk_overlap >= self.chunk_size:
            print("エラー: CHUNK_OVERLAPはCHUNK_SIZEより小さい値である必要があります")
            return False
        
        return True

rag_settings = RAGSettings()

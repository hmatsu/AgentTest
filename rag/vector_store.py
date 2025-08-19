"""
ベクトルストアの管理
複数のベクトルデータベース（Chroma, FAISS, Pinecone）をサポート
"""
import os
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod

from langchain_community.vectorstores import Chroma, FAISS
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.schema import Document

class VectorStoreManager(ABC):
    """ベクトルストア管理の抽象基底クラス"""
    
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        """ドキュメントを追加"""
        pass
    
    @abstractmethod
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """類似度検索"""
        pass
    
    @abstractmethod
    def save(self, path: str) -> None:
        """ベクトルストアを保存"""
        pass
    
    @abstractmethod
    def load(self, path: str) -> None:
        """ベクトルストアを読み込み"""
        pass

class ChromaVectorStore(VectorStoreManager):
    """Chromaベクトルストア実装"""
    
    def __init__(self, collection_name: str = "documents", persist_directory: str = "./chroma_db"):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embeddings = self._get_embeddings()
        self.vectorstore = None
        
    def _get_embeddings(self):
        """エンベディングモデルを取得"""
        try:
            return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        except Exception:
            if os.getenv("OPENAI_API_KEY"):
                return OpenAIEmbeddings()
            else:
                raise ValueError("HuggingFaceEmbeddingsの初期化に失敗し、OpenAI APIキーも設定されていません")
    
    def add_documents(self, documents: List[Document]) -> None:
        """ドキュメントを追加"""
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                persist_directory=self.persist_directory
            )
        else:
            self.vectorstore.add_documents(documents)
        self.vectorstore.persist()
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """類似度検索"""
        if self.vectorstore is None:
            return []
        return self.vectorstore.similarity_search(query, k=k)
    
    def save(self, path: str) -> None:
        """ベクトルストアを保存"""
        if self.vectorstore:
            self.vectorstore.persist()
    
    def load(self, path: str) -> None:
        """ベクトルストアを読み込み"""
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

class FAISSVectorStore(VectorStoreManager):
    """FAISSベクトルストア実装"""
    
    def __init__(self):
        self.embeddings = self._get_embeddings()
        self.vectorstore = None
        
    def _get_embeddings(self):
        """エンベディングモデルを取得"""
        try:
            return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        except Exception:
            if os.getenv("OPENAI_API_KEY"):
                return OpenAIEmbeddings()
            else:
                raise ValueError("HuggingFaceEmbeddingsの初期化に失敗し、OpenAI APIキーも設定されていません")
    
    def add_documents(self, documents: List[Document]) -> None:
        """ドキュメントを追加"""
        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vectorstore.add_documents(documents)
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """類似度検索"""
        if self.vectorstore is None:
            return []
        return self.vectorstore.similarity_search(query, k=k)
    
    def save(self, path: str) -> None:
        """ベクトルストアを保存"""
        if self.vectorstore:
            self.vectorstore.save_local(path)
    
    def load(self, path: str) -> None:
        """ベクトルストアを読み込み"""
        self.vectorstore = FAISS.load_local(path, self.embeddings)

def create_vector_store(store_type: str = "chroma", **kwargs) -> VectorStoreManager:
    """ベクトルストアファクトリー"""
    if store_type.lower() == "chroma":
        return ChromaVectorStore(**kwargs)
    elif store_type.lower() == "faiss":
        return FAISSVectorStore(**kwargs)
    else:
        raise ValueError(f"サポートされていないベクトルストアタイプ: {store_type}")

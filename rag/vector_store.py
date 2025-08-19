"""
ベクトルストアの管理
複数のベクトルデータベース（Chroma, FAISS, GraphRAG）をサポート
"""
import os
import json
import tempfile
import shutil
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
from pathlib import Path

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

class GraphRAGVectorStore(VectorStoreManager):
    """Microsoft GraphRAG実装"""
    
    def __init__(self, workspace_dir: str = "./graphrag_workspace"):
        self.workspace_dir = Path(workspace_dir)
        self.embeddings = self._get_embeddings()
        self.is_indexed = False
        self.documents_added = []
        self._setup_workspace()
        
    def _get_embeddings(self):
        """エンベディングモデルを取得"""
        try:
            return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        except Exception:
            if os.getenv("OPENAI_API_KEY"):
                return OpenAIEmbeddings()
            else:
                raise ValueError("HuggingFaceEmbeddingsの初期化に失敗し、OpenAI APIキーも設定されていません")
    
    def _setup_workspace(self):
        """GraphRAGワークスペースをセットアップ"""
        self.workspace_dir.mkdir(exist_ok=True)
        
        input_dir = self.workspace_dir / "input"
        input_dir.mkdir(exist_ok=True)
        
        output_dir = self.workspace_dir / "output"
        output_dir.mkdir(exist_ok=True)
        
        settings_file = self.workspace_dir / "settings.yaml"
        if not settings_file.exists():
            self._create_default_settings(settings_file)
    
    def _create_default_settings(self, settings_file: Path):
        """デフォルトのGraphRAG設定ファイルを作成"""
        settings_content = """
encoding_model: cl100k_base
skip_workflows: []
llm:
  api_key: ${OPENAI_API_KEY}
  type: openai_chat
  model: gpt-3.5-turbo
  model_supports_json: true
  max_tokens: 4000
  temperature: 0.0

parallelization:
  stagger: 0.3
  num_threads: 50

async_mode: threaded

embeddings:
  async_mode: threaded
  llm:
    api_key: ${OPENAI_API_KEY}
    type: openai_embedding
    model: text-embedding-ada-002
    max_tokens: 8191

input:
  type: file
  file_type: text
  base_dir: "input"
  file_encoding: utf-8
  file_pattern: ".*\\.txt$"

cache:
  type: file
  base_dir: "cache"

storage:
  type: file
  base_dir: "output"

chunk:
  size: 1200
  overlap: 100
  group_by_columns: [id]

entity_extraction:
  prompt: "prompts/entity_extraction.txt"
  entity_types: [organization,person,geo,event]
  max_gleanings: 0

summarize_descriptions:
  prompt: "prompts/summarize_descriptions.txt"
  max_length: 500

claim_extraction:
  enabled: true
  prompt: "prompts/claim_extraction.txt"
  description: "Any claims or facts that could be relevant to information discovery."
  max_gleanings: 0

community_reports:
  prompt: "prompts/community_report.txt"
  max_length: 2000
  max_input_length: 8000

cluster_graph:
  max_cluster_size: 10

embed_graph:
  enabled: false

umap:
  enabled: false

snapshots:
  graphml: false
  raw_entities: false
  top_level_nodes: false

local_search:
  text_unit_prop: 0.5
  community_prop: 0.1
  conversation_history_max_turns: 5
  top_k_mapped_entities: 10
  top_k_relationships: 10
  max_tokens: 12000

global_search:
  max_tokens: 12000
  data_max_tokens: 12000
  map_max_tokens: 1000
  reduce_max_tokens: 2000
  concurrency: 32
"""
        settings_file.write_text(settings_content.strip())
    
    def add_documents(self, documents: List[Document]) -> None:
        """ドキュメントを追加してGraphRAGインデックスを構築"""
        try:
            input_dir = self.workspace_dir / "input"
            
            for i, doc in enumerate(documents):
                content = doc.page_content
                source = doc.metadata.get('source', f'document_{i}')
                
                filename = f"{Path(source).stem}_{i}.txt"
                file_path = input_dir / filename
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.documents_added.append({
                    'file_path': str(file_path),
                    'source': source,
                    'content': content[:200] + "..." if len(content) > 200 else content
                })
            
            print(f"✅ GraphRAG: {len(documents)}個のドキュメントを入力ディレクトリに保存しました")
            self._build_index()
            
        except Exception as e:
            print(f"❌ GraphRAGドキュメント追加エラー: {e}")
            import traceback
            traceback.print_exc()
    
    def _build_index(self):
        """GraphRAGインデックスを構築"""
        try:
            import subprocess
            import sys
            
            print("🔄 GraphRAGインデックスを構築中...")
            
            cmd = [
                sys.executable, "-m", "graphrag.index",
                "--root", str(self.workspace_dir)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.workspace_dir)
            )
            
            if result.returncode == 0:
                print("✅ GraphRAGインデックス構築完了")
                self.is_indexed = True
            else:
                print(f"❌ GraphRAGインデックス構築エラー: {result.stderr}")
                print(f"stdout: {result.stdout}")
                
        except Exception as e:
            print(f"❌ GraphRAGインデックス構築例外: {e}")
            import traceback
            traceback.print_exc()
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """GraphRAGを使用した検索"""
        if not self.is_indexed:
            print("⚠️ GraphRAGインデックスが構築されていません。フォールバック検索を使用します。")
            return self._fallback_search(query, k)
        
        try:
            return self._graphrag_search(query, k)
        except Exception as e:
            print(f"❌ GraphRAG検索エラー: {e}")
            return self._fallback_search(query, k)
    
    def _graphrag_search(self, query: str, k: int = 4) -> List[Document]:
        """GraphRAG検索を実行"""
        try:
            import subprocess
            import sys
            
            cmd = [
                sys.executable, "-m", "graphrag.query",
                "--root", str(self.workspace_dir),
                "--method", "local",
                query
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.workspace_dir)
            )
            
            if result.returncode == 0:
                response_text = result.stdout.strip()
                
                documents = []
                if response_text:
                    doc = Document(
                        page_content=response_text,
                        metadata={
                            'source': 'GraphRAG',
                            'search_type': 'local',
                            'query': query
                        }
                    )
                    documents.append(doc)
                
                return documents[:k]
            else:
                print(f"GraphRAG検索エラー: {result.stderr}")
                return self._fallback_search(query, k)
                
        except Exception as e:
            print(f"GraphRAG検索例外: {e}")
            return self._fallback_search(query, k)
    
    def _fallback_search(self, query: str, k: int = 4) -> List[Document]:
        """フォールバック検索（シンプルなテキストマッチング）"""
        results = []
        
        for doc_info in self.documents_added:
            content = doc_info['content']
            if any(term.lower() in content.lower() for term in query.split()):
                doc = Document(
                    page_content=content,
                    metadata={
                        'source': doc_info['source'],
                        'search_type': 'fallback',
                        'query': query
                    }
                )
                results.append(doc)
        
        return results[:k]
    
    def save(self, path: str) -> None:
        """GraphRAGワークスペースを保存"""
        try:
            if Path(path).exists():
                shutil.rmtree(path)
            shutil.copytree(self.workspace_dir, path)
            print(f"✅ GraphRAGワークスペースを保存: {path}")
        except Exception as e:
            print(f"❌ GraphRAG保存エラー: {e}")
    
    def load(self, path: str) -> None:
        """GraphRAGワークスペースを読み込み"""
        try:
            if self.workspace_dir.exists():
                shutil.rmtree(self.workspace_dir)
            shutil.copytree(path, self.workspace_dir)
            
            output_dir = self.workspace_dir / "output"
            self.is_indexed = output_dir.exists() and any(output_dir.iterdir())
            
            print(f"✅ GraphRAGワークスペースを読み込み: {path}")
        except Exception as e:
            print(f"❌ GraphRAG読み込みエラー: {e}")

def create_vector_store(store_type: str = "chroma", **kwargs) -> VectorStoreManager:
    """ベクトルストアファクトリー"""
    if store_type.lower() == "chroma":
        return ChromaVectorStore(**kwargs)
    elif store_type.lower() == "faiss":
        return FAISSVectorStore(**kwargs)
    elif store_type.lower() == "graphrag":
        return GraphRAGVectorStore(**kwargs)
    else:
        raise ValueError(f"サポートされていないベクトルストアタイプ: {store_type}")

"""
RAG依存関係とインポートのテスト
"""
import sys

def test_basic_imports():
    """基本的なインポートをテスト"""
    print("=== 基本インポートテスト ===")
    
    try:
        import langchain
        print("✅ langchain")
    except ImportError as e:
        print(f"❌ langchain: {e}")
    
    try:
        from langchain_openai import ChatOpenAI
        print("✅ langchain_openai")
    except ImportError as e:
        print(f"❌ langchain_openai: {e}")
    
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        print("✅ langchain_community")
    except ImportError as e:
        print(f"❌ langchain_community: {e}")

def test_rag_dependencies():
    """RAG関連の依存関係をテスト"""
    print("\n=== RAG依存関係テスト ===")
    
    try:
        from langchain.vectorstores import Chroma
        print("✅ Chroma (langchain)")
    except ImportError as e:
        print(f"❌ Chroma: {e}")
    
    try:
        from langchain.vectorstores import FAISS
        print("✅ FAISS (langchain)")
    except ImportError as e:
        print(f"❌ FAISS: {e}")
    
    try:
        from langchain.embeddings import OpenAIEmbeddings
        print("✅ OpenAIEmbeddings")
    except ImportError as e:
        print(f"❌ OpenAIEmbeddings: {e}")
    
    try:
        from langchain.embeddings import HuggingFaceEmbeddings
        print("✅ HuggingFaceEmbeddings")
    except ImportError as e:
        print(f"❌ HuggingFaceEmbeddings: {e}")
    
    try:
        from langchain.document_loaders import TextLoader, PyPDFLoader
        print("✅ Document loaders")
    except ImportError as e:
        print(f"❌ Document loaders: {e}")
    
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        print("✅ Text splitters")
    except ImportError as e:
        print(f"❌ Text splitters: {e}")

def test_external_dependencies():
    """外部依存関係をテスト"""
    print("\n=== 外部依存関係テスト ===")
    
    dependencies = [
        ("chromadb", "Chroma vector database"),
        ("faiss", "FAISS vector search"),
        ("sentence_transformers", "Sentence Transformers"),
        ("pypdf", "PDF processing"),
        ("pydantic", "Data validation"),
        ("beautifulsoup4", "HTML parsing"),
        ("requests", "HTTP requests")
    ]
    
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"✅ {module} ({description})")
        except ImportError as e:
            print(f"❌ {module} ({description}): {e}")

def test_rag_module_imports():
    """RAGモジュールのインポートをテスト"""
    print("\n=== RAGモジュールインポートテスト ===")
    
    try:
        from rag.vector_store import VectorStoreManager, create_vector_store
        print("✅ rag.vector_store")
    except ImportError as e:
        print(f"❌ rag.vector_store: {e}")
    
    try:
        from rag.document_loader import DocumentProcessor, create_document_processor
        print("✅ rag.document_loader")
    except ImportError as e:
        print(f"❌ rag.document_loader: {e}")
    
    try:
        from rag.retrieval_tool import create_rag_tools
        print("✅ rag.retrieval_tool")
    except ImportError as e:
        print(f"❌ rag.retrieval_tool: {e}")
    
    try:
        from rag.rag_agent import create_rag_agent
        print("✅ rag.rag_agent")
    except ImportError as e:
        print(f"❌ rag.rag_agent: {e}")
    
    try:
        from config.rag_settings import rag_settings
        print("✅ config.rag_settings")
    except ImportError as e:
        print(f"❌ config.rag_settings: {e}")

def main():
    """メインテスト実行"""
    print("RAG実装の依存関係とインポートをテストします\n")
    
    test_basic_imports()
    test_rag_dependencies()
    test_external_dependencies()
    test_rag_module_imports()
    
    print("\n=== テスト完了 ===")
    print("❌ が表示された依存関係は requirements.txt に追加する必要があります")

if __name__ == "__main__":
    main()

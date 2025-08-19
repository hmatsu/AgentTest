"""
GraphRAG実装テスト
基本的な機能が動作するかテスト
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_imports():
    """インポートテスト"""
    print("🔍 インポートテスト開始...")
    
    try:
        from rag.vector_store import create_vector_store, GraphRAGVectorStore
        print("✅ GraphRAGVectorStore インポート成功")
        
        from rag.retrieval_tool import create_graphrag_tools
        print("✅ GraphRAGツール インポート成功")
        
        from rag.rag_agent import create_graphrag_agent
        print("✅ GraphRAGエージェント インポート成功")
        
        return True
    except Exception as e:
        print(f"❌ インポートエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vector_store_creation():
    """ベクトルストア作成テスト"""
    print("\n🔍 ベクトルストア作成テスト開始...")
    
    try:
        from rag.vector_store import create_vector_store
        
        chroma_store = create_vector_store("chroma")
        print("✅ Chromaベクトルストア作成成功")
        
        graphrag_store = create_vector_store("graphrag")
        print("✅ GraphRAGベクトルストア作成成功")
        
        return True
    except Exception as e:
        print(f"❌ ベクトルストア作成エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_document_processing():
    """ドキュメント処理テスト"""
    print("\n🔍 ドキュメント処理テスト開始...")
    
    try:
        from rag.vector_store import create_vector_store
        from langchain.schema import Document
        
        test_docs = [
            Document(
                page_content="これはテスト用のドキュメントです。GraphRAGの機能をテストしています。",
                metadata={"source": "test_doc_1"}
            ),
            Document(
                page_content="GraphRAGはエンティティと関係性を理解する高度な検索システムです。",
                metadata={"source": "test_doc_2"}
            )
        ]
        
        graphrag_store = create_vector_store("graphrag")
        graphrag_store.add_documents(test_docs)
        print("✅ GraphRAGドキュメント追加成功")
        
        results = graphrag_store.similarity_search("GraphRAGとは何ですか？", k=2)
        print(f"✅ GraphRAG検索成功: {len(results)}件の結果")
        
        for i, doc in enumerate(results, 1):
            print(f"  結果{i}: {doc.page_content[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ ドキュメント処理エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """メインテスト"""
    print("🚀 GraphRAG実装テスト開始")
    print("=" * 50)
    
    tests = [
        ("インポートテスト", test_imports),
        ("ベクトルストア作成テスト", test_vector_store_creation),
        ("ドキュメント処理テスト", test_document_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 成功")
            else:
                print(f"❌ {test_name} 失敗")
        except Exception as e:
            print(f"❌ {test_name} 例外: {e}")
    
    print(f"\n📊 テスト結果: {passed}/{total} 成功")
    
    if passed == total:
        print("🎉 すべてのテストが成功しました！")
        return True
    else:
        print("⚠️ 一部のテストが失敗しました")
        return False

if __name__ == "__main__":
    main()

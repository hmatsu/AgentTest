"""
RAG vs GraphRAG 比較スクリプト
従来のRAGとGraphRAGの検索結果を比較して性能を評価
"""
import os
from dotenv import load_dotenv
from rag.rag_agent import create_rag_agent, create_graphrag_agent

load_dotenv()

def compare_rag_approaches():
    """RAGとGraphRAGの比較実験"""
    
    test_queries = [
        "ドキュメントの主要な内容は何ですか？",
        "重要な概念や用語を教えてください",
        "関連する情報をまとめてください",
        "このドキュメントで説明されている機能は何ですか？"
    ]
    
    print("🔍 RAG vs GraphRAG 比較実験")
    print("=" * 50)
    
    try:
        print("\n📊 従来のRAGエージェントを初期化中...")
        rag_agent = create_rag_agent()
        rag_agent.add_documents_from_path("documents/")
        
        print("\n🕸️ GraphRAGエージェントを初期化中...")
        graphrag_agent = create_graphrag_agent()
        graphrag_agent.add_documents_from_path("documents/")
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{'='*60}")
            print(f"🔍 テストクエリ {i}: {query}")
            print(f"{'='*60}")
            
            print("\n📊 従来のRAG結果:")
            print("-" * 30)
            try:
                rag_result = rag_agent.chat(query)
                print(rag_result)
            except Exception as e:
                print(f"❌ 従来のRAGエラー: {e}")
            
            print("\n🕸️ GraphRAG結果:")
            print("-" * 30)
            try:
                graphrag_result = graphrag_agent.chat(query)
                print(graphrag_result)
            except Exception as e:
                print(f"❌ GraphRAGエラー: {e}")
            
            print("\n" + "="*60)
            
    except Exception as e:
        print(f"❌ 比較実験エラー: {e}")
        import traceback
        traceback.print_exc()

def simple_comparison():
    """シンプルな比較（エラーハンドリング強化版）"""
    print("🔍 シンプルRAG vs GraphRAG 比較")
    print("=" * 40)
    
    query = "ドキュメントの内容について教えてください"
    
    try:
        print("\n📊 従来のRAG検索テスト:")
        from rag.vector_store import create_vector_store
        from rag.document_loader import create_document_processor
        
        rag_store = create_vector_store("chroma")
        processor = create_document_processor()
        documents = processor.load_documents_from_path("documents/")
        
        if documents:
            rag_store.add_documents(documents)
            rag_results = rag_store.similarity_search(query, k=2)
            
            print(f"✅ 従来のRAG結果 ({len(rag_results)}件):")
            for i, doc in enumerate(rag_results, 1):
                print(f"  {i}. {doc.page_content[:200]}...")
        else:
            print("❌ ドキュメントが見つかりません")
            
    except Exception as e:
        print(f"❌ 従来のRAGテストエラー: {e}")
    
    try:
        print("\n🕸️ GraphRAG検索テスト:")
        graphrag_store = create_vector_store("graphrag")
        
        if documents:
            graphrag_store.add_documents(documents)
            graphrag_results = graphrag_store.similarity_search(query, k=2)
            
            print(f"✅ GraphRAG結果 ({len(graphrag_results)}件):")
            for i, doc in enumerate(graphrag_results, 1):
                print(f"  {i}. {doc.page_content[:200]}...")
        else:
            print("❌ ドキュメントが見つかりません")
            
    except Exception as e:
        print(f"❌ GraphRAGテストエラー: {e}")

def main():
    """メイン比較実験"""
    import sys
    if sys.version_info >= (3, 13):
        print("❌ GraphRAGはPython 3.13をサポートしていません")
        print("   Python 3.10-3.12を使用してください")
        print("   従来のRAGのみでテストを実行します...")
        
        try:
            from rag.rag_agent import create_rag_agent
            rag_agent = create_rag_agent()
            rag_agent.add_documents_from_path("documents/")
            result = rag_agent.chat("ドキュメントの内容を教えてください")
            print(f"従来のRAG結果: {result}")
        except Exception as e:
            print(f"❌ 従来のRAGテストエラー: {e}")
        return
    
    if os.getenv("OPENAI_API_KEY"):
        compare_rag_approaches()
    else:
        print("⚠️ OPENAI_API_KEYが設定されていません。シンプル比較を実行します。")
        simple_comparison()

if __name__ == "__main__":
    main()

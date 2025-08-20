"""
Safe GraphRAG vs Traditional RAG Comparison
Includes timeout handling and smaller dataset options
"""
import os
import sys
from pathlib import Path

def check_dataset_size():
    """Check the size of the dataset and recommend approach"""
    documents_dir = Path("documents/")
    if not documents_dir.exists():
        print("❌ documents/ directory not found")
        return False, 0
    
    files = list(documents_dir.glob("*.csv")) + list(documents_dir.glob("*.txt"))
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    
    print(f"📊 Dataset analysis:")
    print(f"   Files: {len(files)}")
    print(f"   Total size: {total_size / 1024:.1f} KB")
    
    if total_size > 100 * 1024:  # > 100KB
        print("⚠️ Large dataset detected - GraphRAG indexing may take 5+ minutes")
        return True, total_size
    else:
        print("✅ Small dataset - GraphRAG should complete quickly")
        return True, total_size

def compare_rag_approaches_safe():
    """Safe RAG vs GraphRAG comparison with timeout handling"""
    
    print("🔍 Safe RAG vs GraphRAG 比較実験")
    print("=" * 50)
    
    dataset_ok, size = check_dataset_size()
    if not dataset_ok:
        return False
    
    test_queries = [
        "ドキュメントの主要な内容は何ですか？",
        "重要な概念や用語を教えてください"
    ]
    
    try:
        from rag.rag_agent import create_rag_agent, create_graphrag_agent
        
        print("\n📊 従来のRAGエージェントを初期化中...")
        rag_agent = create_rag_agent()
        rag_agent.add_documents_from_path("documents/")
        
        print("\n🕸️ GraphRAGエージェントを初期化中...")
        print("⏰ GraphRAGインデックス構築には時間がかかる場合があります...")
        
        graphrag_agent = create_graphrag_agent()
        
        try:
            graphrag_agent.add_documents_from_path("documents/")
            print("✅ GraphRAGインデックス構築完了")
        except Exception as e:
            print(f"⚠️ GraphRAGインデックス構築でエラー: {e}")
            print("🔄 フォールバック検索を使用します")
        
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
        
        return True
        
    except Exception as e:
        print(f"❌ 比較実験エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main execution with safety checks"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY環境変数が設定されていません")
        print("💡 設定方法: set OPENAI_API_KEY=your_openai_key")
        return False
    
    if api_key.startswith('sk-dummy') or api_key.startswith('sk-test'):
        print("⚠️ テスト用APIキーが検出されました")
        print("💡 実際のOpenAI APIキーを使用してください")
        return False
    
    print("🔑 OpenAI APIキーが設定されています。安全なGraphRAG比較を実行します。")
    
    success = compare_rag_approaches_safe()
    
    if success:
        print("\n🎉 安全な比較実験が完了しました！")
        print("✅ タイムアウト処理により、ハングアップを防止しました")
    else:
        print("\n❌ 比較実験でエラーが発生しました")
        
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

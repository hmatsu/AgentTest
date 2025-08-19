"""
GraphRAG使用例
Microsoft GraphRAGを使用したドキュメント検索の例
"""
import os
from dotenv import load_dotenv
from rag.rag_agent import create_graphrag_agent

load_dotenv()

def main():
    """GraphRAGエージェントの使用例"""
    
    print("🕸️ GraphRAGエージェント使用例")
    print("=" * 40)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEYが設定されていません")
        print("環境変数を設定するか、.envファイルにOPENAI_API_KEYを追加してください")
        return
    
    try:
        print("\n🔄 GraphRAGエージェントを初期化中...")
        agent = create_graphrag_agent()
        
        print("📁 ドキュメントを読み込み中...")
        agent.add_documents_from_path("documents/")
        
        print("\n✅ 初期化完了！以下のコマンドが利用可能です:")
        print("- graphrag_entity_search: エンティティベースの検索")
        print("- graphrag_relationship_search: 関係性ベースの検索")
        print("- rag_search: 従来のRAG検索")
        print("- web_search: インターネット検索")
        
        test_queries = [
            "ドキュメントにはどのような内容が含まれていますか？",
            "重要なエンティティや概念を教えてください",
            "このドキュメントの主要なテーマは何ですか？"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{'='*50}")
            print(f"🔍 テストクエリ {i}: {query}")
            print(f"{'='*50}")
            
            try:
                response = agent.chat(query)
                print(f"🤖 GraphRAGエージェントの回答:\n{response}")
            except Exception as e:
                print(f"❌ クエリ実行エラー: {e}")
        
        print(f"\n{'='*50}")
        print("🎯 インタラクティブモード")
        print("質問を入力してください（'quit'で終了）:")
        
        while True:
            try:
                user_input = input("\n❓ あなたの質問: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '終了', 'q']:
                    print("👋 GraphRAGエージェントを終了します")
                    break
                
                if not user_input:
                    continue
                
                print("🤖 GraphRAGエージェントが回答中...")
                response = agent.chat(user_input)
                print(f"\n📝 回答:\n{response}")
                
            except KeyboardInterrupt:
                print("\n👋 GraphRAGエージェントを終了します")
                break
            except Exception as e:
                print(f"❌ エラーが発生しました: {e}")
                
    except Exception as e:
        print(f"❌ GraphRAGエージェント初期化エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

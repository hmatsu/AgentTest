"""
GraphRAG使用例
Microsoft GraphRAGを使用したドキュメント検索の例
"""
import os
from dotenv import load_dotenv
from rag.rag_agent import create_graphrag_agent

load_dotenv()

def setup_graphrag_example():
    """GraphRAGの例をセットアップ"""
    print("=== GraphRAG対応エージェントの例 ===\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEYが設定されていません")
        print("環境変数を設定するか、.envファイルにOPENAI_API_KEYを追加してください")
        return None
    
    try:
        print("🔄 GraphRAGエージェントを初期化中...")
        agent = create_graphrag_agent()
        
        print("📁 ドキュメントを読み込み中...")
        agent.add_documents_from_path("documents/")
        
        print("\n✅ 初期化完了！以下のコマンドが利用可能です:")
        print("- graphrag_entity_search: エンティティベースの検索")
        print("- graphrag_relationship_search: 関係性ベースの検索")
        print("- rag_search: 従来のRAG検索")
        print("- web_search: インターネット検索")
        
        return agent
        
    except Exception as e:
        print(f"❌ GraphRAGエージェント初期化エラー: {e}")
        import traceback
        traceback.print_exc()
        return None

def run_graphrag_examples():
    """GraphRAGの例を実行"""
    agent = setup_graphrag_example()
    if not agent:
        return
    
    print("\n" + "="*50)
    print("🤖 GraphRAGエージェントとの対話例")
    print("="*50)
    
    test_queries = [
        "ドキュメントにはどのような内容が含まれていますか？",
        "重要なエンティティや概念を教えてください",
        "このドキュメントの主要なテーマは何ですか？"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n【例{i}】{query}")
        print("質問:", query)
        try:
            response = agent.chat(query)
            print(f"回答: {response}")
        except Exception as e:
            print(f"エラー: {e}")
        
        print("\n" + "-"*50)

def interactive_graphrag_chat():
    """インタラクティブなGraphRAGチャット"""
    agent = setup_graphrag_example()
    if not agent:
        return
    
    print("\n" + "="*50)
    print("💬 インタラクティブGraphRAGチャット")
    print("グラフベースの知識検索を活用して質問に答えます")
    print("'quit'で終了")
    print("="*50)
    
    while True:
        try:
            user_input = input("\n❓ あなたの質問: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '終了', 'q']:
                print("👋 GraphRAGエージェントを終了します")
                break
            
            if not user_input:
                print("質問を入力してください。")
                continue
            
            print("\n🤖 GraphRAGエージェントが回答中...")
            response = agent.chat(user_input)
            print(f"\n📝 回答:\n{response}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\n👋 GraphRAGエージェントを終了します")
            break
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")

def main():
    """メイン実行関数"""
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEYが設定されていません")
        print("GraphRAGエージェントを使用するにはAPIキーが必要です")
        return
    
    print("GraphRAG対応エージェントのデモを開始します\n")
    
    choice = input("実行モードを選択してください:\n1. 例の実行\n2. インタラクティブチャット\n選択 (1/2): ").strip()
    
    if choice == "1":
        run_graphrag_examples()
    elif choice == "2":
        interactive_graphrag_chat()
    else:
        print("無効な選択です")

if __name__ == "__main__":
    main()

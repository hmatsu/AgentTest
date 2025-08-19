"""
RAG対応エージェントの使用例
"""
import os
from dotenv import load_dotenv
from rag.rag_agent import create_rag_agent
from rag.document_loader import create_document_processor
from config.rag_settings import rag_settings

load_dotenv()

def setup_rag_example():
    """RAGの例をセットアップ"""
    print("=== RAG対応エージェントの例 ===\n")
    
    if not rag_settings.validate():
        print("❌ RAG設定に問題があります")
        return None
    
    print("📚 RAGエージェントを作成中...")
    try:
        agent = create_rag_agent(**rag_settings.get_rag_agent_config())
        print("✅ RAGエージェントを作成しました")
    except Exception as e:
        print(f"❌ RAGエージェント作成エラー: {e}")
        return None
    
    documents_dir = rag_settings.documents_directory
    if os.path.exists(documents_dir):
        doc_files = []
        for ext in ['.txt', '.pdf', '.csv']:
            doc_files.extend([f for f in os.listdir(documents_dir) if f.endswith(ext)])
        
        if doc_files:
            print(f"\n📄 documentsディレクトリからファイルを読み込み中...")
            print(f"見つかったファイル: {', '.join(doc_files)}")
            
            try:
                agent.add_documents_from_path(documents_dir)
                return agent
            except Exception as e:
                print(f"⚠️  ファイル読み込みエラー: {e}")
                print("💡 サンプルドキュメントを使用します")
    
    print("\n📄 サンプルドキュメントを追加中...")
    sample_documents = [
        {
            "text": """
            LangChainは、大規模言語モデル（LLM）を使用したアプリケーションの開発を簡素化するフレームワークです。
            LangChainの主な機能には以下があります：
            1. プロンプト管理とテンプレート化
            2. LLMとの統合（OpenAI、Anthropic、HuggingFaceなど）
            3. エージェントとツールの統合
            4. メモリ管理
            5. チェーンの構築
            6. ドキュメント読み込みと処理
            """,
            "metadata": {"source": "langchain_overview", "type": "documentation"}
        },
        {
            "text": """
            RAG（Retrieval-Augmented Generation）は、検索拡張生成と呼ばれる手法です。
            RAGの仕組み：
            1. ユーザーの質問を受け取る
            2. 関連するドキュメントをベクトル検索で取得
            3. 取得したドキュメントと質問を組み合わせてLLMに送信
            4. LLMが文脈を考慮した回答を生成
            
            RAGの利点：
            - 最新情報の活用
            - ドメイン固有の知識の活用
            - ハルシネーション（幻覚）の削減
            """,
            "metadata": {"source": "rag_explanation", "type": "documentation"}
        },
        {
            "text": """
            Pythonでのベクトルデータベースの選択肢：
            
            1. Chroma: オープンソース、簡単セットアップ、永続化サポート
            2. FAISS: Facebook製、高速検索、大規模データ対応
            3. Pinecone: クラウドベース、スケーラブル、管理不要
            4. Weaviate: GraphQLサポート、セマンティック検索
            5. Qdrant: Rust製、高性能、フィルタリング機能
            
            選択基準：
            - データサイズ
            - 検索速度要件
            - 運用コスト
            - 機能要件
            """,
            "metadata": {"source": "vector_databases", "type": "comparison"}
        }
    ]
    
    for doc in sample_documents:
        agent.add_documents_from_text(doc["text"], doc["metadata"])
    
    print("✅ サンプルドキュメントを追加しました")
    
    return agent

def run_rag_examples():
    """RAGの例を実行"""
    agent = setup_rag_example()
    if not agent:
        return
    
    print("\n" + "="*50)
    print("🤖 RAGエージェントとの対話例")
    print("="*50)
    
    print("\n【例1】LangChainについて質問")
    print("質問: LangChainの主な機能は何ですか？")
    try:
        response = agent.chat("LangChainの主な機能は何ですか？")
        print(f"回答: {response}")
    except Exception as e:
        print(f"エラー: {e}")
    
    print("\n" + "-"*50)
    
    print("\n【例2】RAGについて質問")
    print("質問: RAGとは何ですか？どのような利点がありますか？")
    try:
        response = agent.chat("RAGとは何ですか？どのような利点がありますか？")
        print(f"回答: {response}")
    except Exception as e:
        print(f"エラー: {e}")
    
    print("\n" + "-"*50)
    
    print("\n【例3】ベクトルデータベースについて質問")
    print("質問: Pythonで使えるベクトルデータベースを比較してください")
    try:
        response = agent.chat("Pythonで使えるベクトルデータベースを比較してください")
        print(f"回答: {response}")
    except Exception as e:
        print(f"エラー: {e}")

def interactive_rag_chat():
    """インタラクティブなRAGチャット"""
    agent = setup_rag_example()
    if not agent:
        return
    
    print("\n" + "="*50)
    print("💬 インタラクティブRAGチャット")
    print("ドキュメントベースの知識を活用して質問に答えます")
    print("'quit'で終了")
    print("="*50)
    
    while True:
        try:
            user_input = input("\n質問: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '終了', 'q']:
                print("RAGチャットを終了します。")
                break
            
            if not user_input:
                print("質問を入力してください。")
                continue
            
            print("\n🤖 回答:")
            response = agent.chat(user_input)
            print(response)
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\nRAGチャットを終了します。")
            break
        except Exception as e:
            print(f"エラーが発生しました: {e}")

def main():
    """メイン実行関数"""
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEYが設定されていません")
        print("RAGエージェントを使用するにはAPIキーが必要です")
        return
    
    print("RAG対応エージェントのデモを開始します\n")
    
    choice = input("実行モードを選択してください:\n1. 例の実行\n2. インタラクティブチャット\n選択 (1/2): ").strip()
    
    if choice == "1":
        run_rag_examples()
    elif choice == "2":
        interactive_rag_chat()
    else:
        print("無効な選択です")

if __name__ == "__main__":
    main()

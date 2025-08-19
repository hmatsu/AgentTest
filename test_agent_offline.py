"""
オフラインテスト用エージェント
APIキーなしでエージェントの基本動作を確認できます
"""
import os
import sys

def load_env_safely():
    """安全に環境変数を読み込む"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .envファイルから環境変数を読み込みました")
        return True
    except UnicodeDecodeError:
        print("⚠️  .envファイルの文字エンコーディングに問題があります")
        print("   python fix_encoding.py を実行して修正してください")
        return False
    except ImportError:
        print("⚠️  python-dotenvがインストールされていません")
        print("   pip install python-dotenv を実行してください")
        return False
    except Exception as e:
        print(f"⚠️  環境変数の読み込みでエラー: {e}")
        return False

def mock_chat_response(question):
    """
    APIを使わずにモック応答を返す（テスト用）
    """
    responses = {
        "日本の首都": "日本の首都は東京です。",
        "python": "Pythonは汎用プログラミング言語で、シンプルで読みやすい構文が特徴です。",
        "langchain": "LangChainは大規模言語モデルを使ったアプリケーション開発のためのフレームワークです。",
        "天気": "申し訳ございませんが、リアルタイムの天気情報を取得するにはAPIキーが必要です。",
        "計算": "計算を行うには、具体的な数式を教えてください。例：2 + 2",
        "hello": "Hello! How can I help you today?",
        "こんにちは": "こんにちは！何かお手伝いできることはありますか？"
    }
    
    question_lower = question.lower()
    
    for keyword, response in responses.items():
        if keyword in question_lower:
            return response
    
    return f"「{question}」についてお答えするには、OpenAI APIキーが必要です。これはオフラインテストモードです。"

def test_encoding_and_basic_functionality():
    """
    エンコーディングと基本機能をテスト
    """
    print("=== エージェント オフラインテスト ===")
    print("エンコーディング問題の修正とエージェントの基本動作を確認します\n")
    
    print("1. 環境変数読み込みテスト:")
    env_loaded = load_env_safely()
    
    print("\n2. APIキー確認:")
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        print("✅ OPENAI_API_KEYが設定されています")
        print("⚠️  ただし、APIクォータの問題がある可能性があります")
    else:
        print("⚠️  OPENAI_API_KEYが設定されていません")
    
    print("\n3. 基本対話テスト（オフラインモード）:")
    print("以下はAPIを使わないテストです。実際のAI応答ではありません。\n")
    
    test_questions = [
        "日本の首都はどこですか？",
        "Pythonについて教えてください",
        "LangChainとは何ですか？"
    ]
    
    for question in test_questions:
        print(f"質問: {question}")
        response = mock_chat_response(question)
        print(f"応答: {response}")
        print("-" * 50)
    
    print("\n=== テスト結果まとめ ===")
    if env_loaded:
        print("✅ エンコーディング問題は解決されています")
    else:
        print("❌ エンコーディング問題があります - fix_encoding.py を実行してください")
    
    print("\n📝 次のステップ:")
    print("1. APIクォータの問題を解決:")
    print("   - https://platform.openai.com/account/billing でクレジット確認")
    print("   - 新しいAPIキーを作成")
    print("   - 課金設定を確認")
    print("2. 解決後、simple_qa_agent_fixed.py でテスト")

def interactive_test():
    """
    インタラクティブなオフラインテスト
    """
    print("\n=== インタラクティブテスト ===")
    print("オフラインモードで対話をテストできます")
    print("（実際のAI応答ではありません）")
    print("'quit'で終了\n")
    
    while True:
        try:
            question = input("質問: ").strip()
            
            if question.lower() in ['quit', 'exit', '終了', 'q']:
                print("テストを終了します。")
                break
            
            if not question:
                print("質問を入力してください。")
                continue
            
            response = mock_chat_response(question)
            print(f"応答: {response}")
            print("-" * 30)
            
        except KeyboardInterrupt:
            print("\nテストを終了します。")
            break

def main():
    """メイン実行関数"""
    test_encoding_and_basic_functionality()
    
    choice = input("\nインタラクティブテストを実行しますか？ (y/n): ").strip().lower()
    if choice in ['y', 'yes', 'はい']:
        interactive_test()

if __name__ == "__main__":
    main()

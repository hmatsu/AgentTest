"""
シンプルな質疑応答エージェント（エンコーディング問題修正版）
Windows環境での文字エンコーディング問題を解決
"""
import os
import sys
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

def load_env_safely():
    """安全に環境変数を読み込む"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .envファイルから環境変数を読み込みました")
    except UnicodeDecodeError:
        print("⚠️  .envファイルの文字エンコーディングに問題があります")
        print("   以下の方法で解決できます：")
        print("   1. .envファイルをUTF-8で保存し直す")
        print("   2. または、環境変数を直接設定する")
        print()
    except ImportError:
        print("⚠️  python-dotenvがインストールされていません")
        print("   pip install python-dotenv を実行してください")
    except Exception as e:
        print(f"⚠️  環境変数の読み込みでエラー: {e}")

def get_api_key():
    """APIキーを取得（複数の方法を試行）"""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    print("OPENAI_API_KEYが設定されていません。")
    print("\n以下の方法でAPIキーを設定できます：")
    print("1. 環境変数として設定")
    print("2. 直接入力（一時的）")
    print()
    
    choice = input("直接入力しますか？ (y/n): ").strip().lower()
    if choice in ['y', 'yes', 'はい']:
        api_key = input("OpenAI APIキーを入力してください: ").strip()
        if api_key:
            return api_key
    
    return None

def create_simple_qa_agent():
    """シンプルなQ&Aエージェントを作成"""
    
    api_key = get_api_key()
    if not api_key:
        print("\nAPIキーが設定されていないため、エージェントを開始できません。")
        print("\n📝 APIキーの取得方法：")
        print("1. https://platform.openai.com にアクセス")
        print("2. アカウントを作成またはログイン")
        print("3. 右上のメニューから「API keys」を選択")
        print("4. 「Create new secret key」をクリック")
        print("5. キーをコピーして使用")
        return None
    
    try:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=api_key
        )
        return llm
    except Exception as e:
        print(f"LLMの初期化に失敗しました: {e}")
        return None

def chat_with_agent(llm, question):
    """エージェントと対話"""
    try:
        messages = [
            SystemMessage(content="あなたは親切で知識豊富なアシスタントです。質問に丁寧に答えてください。"),
            HumanMessage(content=question)
        ]
        
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"エラーが発生しました: {e}"

def main():
    """メイン実行関数"""
    print("=== シンプルQ&Aエージェント（修正版） ===")
    print("Windows環境での文字エンコーディング問題を解決した版です\n")
    
    load_env_safely()
    
    llm = create_simple_qa_agent()
    if not llm:
        return
    
    print("✅ エージェントの準備が完了しました！")
    print("何でも質問してください（'quit'または'終了'で終了）\n")
    
    while True:
        try:
            question = input("質問: ").strip()
            
            if question.lower() in ['quit', 'exit', '終了', 'q']:
                print("\nエージェントを終了します。お疲れ様でした！")
                break
            
            if not question:
                print("質問を入力してください。")
                continue
            
            print("\n🤖 回答:")
            answer = chat_with_agent(llm, question)
            print(answer)
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\nエージェントを終了します。")
            break
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")

if __name__ == "__main__":
    main()

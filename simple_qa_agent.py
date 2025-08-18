"""
シンプルな質疑応答エージェント
OpenAI APIキーがあればすぐに動作確認できます
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

load_dotenv()

def create_simple_qa_agent():
    """シンプルなQ&Aエージェントを作成"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("エラー: OPENAI_API_KEYが設定されていません。")
        print("1. .env.exampleを.envにコピーしてください")
        print("2. .envファイルでOPENAI_API_KEYを設定してください")
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
    print("=== シンプルQ&Aエージェント ===")
    print("動作確認用の質疑応答エージェントです\n")
    
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

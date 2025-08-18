"""
LangChain エージェントのメイン実行ファイル
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

def create_simple_agent():
    """シンプルな検索エージェントを作成"""
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    tools = [
        DuckDuckGoSearchRun(name="search", description="インターネット検索を行う")
    ]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたは親切なアシスタントです。質問に答えるために必要に応じてツールを使用してください。"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

def main():
    """メイン実行関数"""
    print("LangChain エージェントを起動中...")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("エラー: OPENAI_API_KEYが設定されていません。")
        print(".envファイルを作成してAPIキーを設定してください。")
        return
    
    try:
        agent_executor = create_simple_agent()
        
        print("エージェントが準備完了しました！")
        print("質問を入力してください（'quit'で終了）:")
        
        while True:
            user_input = input("\n> ")
            
            if user_input.lower() in ['quit', 'exit', '終了']:
                print("エージェントを終了します。")
                break
            
            if user_input.strip():
                try:
                    response = agent_executor.invoke({"input": user_input})
                    print(f"\n回答: {response['output']}")
                except Exception as e:
                    print(f"エラーが発生しました: {e}")
            
    except Exception as e:
        print(f"エージェントの初期化に失敗しました: {e}")
        print("APIキーが正しく設定されているか確認してください。")

if __name__ == "__main__":
    main()

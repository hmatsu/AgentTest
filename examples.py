"""
LangChain エージェントの使用例
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from tools.custom_tools import get_custom_tools

load_dotenv()

def example_react_agent():
    """ReActエージェントの例"""
    print("=== ReActエージェントの例 ===")
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    tools = [
        DuckDuckGoSearchRun(name="search", description="インターネット検索"),
        *get_custom_tools()
    ]
    
    template = """以下のツールにアクセスできます:

{tools}

以下の形式を使用してください:

Question: 答える必要がある入力質問
Thought: 何をすべきかを考える
Action: 実行するアクション、[{tool_names}]のいずれか
Action Input: アクションへの入力
Observation: アクションの結果
... (このThought/Action/Action Input/Observationは必要に応じて繰り返し)
Thought: 最終回答がわかりました
Final Answer: 元の入力質問に対する最終回答

開始！

Question: {input}
Thought: {agent_scratchpad}"""
    
    prompt = PromptTemplate.from_template(template)
    
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

def example_conversation_agent():
    """会話型エージェントの例"""
    print("=== 会話型エージェントの例 ===")
    
    from langchain.agents import create_openai_functions_agent
    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.memory import ConversationBufferMemory
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    tools = get_custom_tools()
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "あなたは親切で知識豊富なアシスタントです。会話の文脈を理解し、必要に応じてツールを使用して質問に答えてください。"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        memory=memory,
        verbose=True
    )
    
    return agent_executor

def run_examples():
    """例の実行"""
    if not os.getenv("OPENAI_API_KEY"):
        print("エラー: OPENAI_API_KEYが設定されていません。")
        return
    
    print("LangChain エージェントの例を実行します。\n")
    
    try:
        react_agent = example_react_agent()
        print("ReActエージェントで計算を実行:")
        result = react_agent.invoke({"input": "25 * 4 を計算してください"})
        print(f"結果: {result['output']}\n")
    except Exception as e:
        print(f"ReActエージェントでエラー: {e}\n")
    
    try:
        conv_agent = example_conversation_agent()
        print("会話型エージェントで天気を確認:")
        result = conv_agent.invoke({"input": "東京の天気を教えてください"})
        print(f"結果: {result['output']}\n")
    except Exception as e:
        print(f"会話型エージェントでエラー: {e}\n")

if __name__ == "__main__":
    run_examples()

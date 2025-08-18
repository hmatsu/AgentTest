"""
カスタムエージェントの実装例
"""
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain.llms.base import LLM
from langchain.schema import AgentAction, AgentFinish
from typing import List, Union
import re

class CustomPromptTemplate(StringPromptTemplate):
    """カスタムプロンプトテンプレート"""
    
    template: str
    tools: List[Tool]
    
    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\n観察: {observation}\n思考: "
        
        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        
        return self.template.format(**kwargs)

class CustomOutputParser:
    """カスタム出力パーサー"""
    
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        if "最終回答:" in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("最終回答:")[-1].strip()},
                log=llm_output,
            )
        
        regex = r"アクション: (.*?)\nアクション入力: (.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        
        action = match.group(1).strip()
        action_input = match.group(2)
        
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

def create_custom_agent(llm: LLM, tools: List[Tool]) -> AgentExecutor:
    """カスタムエージェントを作成"""
    
    template = """以下のツールにアクセスできます:

{tools}

以下の形式を使用してください:

質問: 答える必要がある入力質問
思考: 何をすべきかを常に考える必要があります
アクション: 実行するアクション、[{tool_names}]のいずれかである必要があります
アクション入力: アクションへの入力
観察: アクションの結果
... (この思考/アクション/アクション入力/観察は複数回繰り返すことができます)
思考: 最終回答がわかりました
最終回答: 元の入力質問に対する最終回答

開始！

質問: {input}
思考: {agent_scratchpad}"""
    
    prompt = CustomPromptTemplate(
        template=template,
        tools=tools,
        input_variables=["input", "intermediate_steps"]
    )
    
    output_parser = CustomOutputParser()
    
    llm_chain = llm
    
    tool_names = [tool.name for tool in tools]
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\n観察:"],
        allowed_tools=tool_names
    )
    
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, 
        tools=tools, 
        verbose=True
    )
    
    return agent_executor

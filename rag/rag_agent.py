"""
RAG対応エージェント
既存のエージェントにRAG機能を統合
"""
import os
from typing import List, Optional
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_community.tools import DuckDuckGoSearchRun

from .vector_store import VectorStoreManager, create_vector_store
from .retrieval_tool import create_rag_tools
from tools.custom_tools import get_custom_tools

load_dotenv()

class RAGAgent:
    """RAG対応エージェント"""
    
    def __init__(self, 
                 vector_store: Optional[VectorStoreManager] = None,
                 model: str = "gpt-3.5-turbo",
                 temperature: float = 0.7,
                 include_web_search: bool = True,
                 include_custom_tools: bool = True):
        
        self.vector_store = vector_store or create_vector_store("chroma")
        self.model = model
        self.temperature = temperature
        self.include_web_search = include_web_search
        self.include_custom_tools = include_custom_tools
        
        self.llm = self._create_llm()
        self.tools = self._create_tools()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.agent_executor = self._create_agent()
    
    def _create_llm(self):
        """LLMを作成"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEYが設定されていません")
        
        return ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            api_key=api_key
        )
    
    def _create_tools(self):
        """ツールリストを作成"""
        tools = []
        
        rag_tools = create_rag_tools(self.vector_store)
        tools.extend(rag_tools)
        
        if self.include_web_search:
            tools.append(DuckDuckGoSearchRun(
                name="web_search", 
                description="インターネット検索を行います。最新情報や一般的な質問に使用してください。"
            ))
        
        if self.include_custom_tools:
            tools.extend(get_custom_tools())
        
        return tools
    
    def _create_agent(self):
        """エージェントを作成"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """あなたは知識豊富なアシスタントです。以下のツールを使用して質問に答えてください：

1. rag_search: ドキュメントベースから関連情報を検索
2. rag_summarize: 検索した文書の要約
3. web_search: インターネット検索（最新情報用）
4. calculator: 数学計算
5. weather: 天気情報

回答の際は：
- まずRAG検索でドキュメントベースを確認
- 必要に応じてWeb検索で最新情報を補完
- 情報源を明確に示す
- 正確で詳細な回答を提供"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_functions_agent(self.llm, self.tools, prompt)
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=10
        )
    
    def add_documents_from_path(self, path: str):
        """パスからドキュメントを追加"""
        from .document_loader import create_document_processor
        from config.rag_settings import rag_settings
        import os
        from pathlib import Path
        
        config = rag_settings.get_document_processor_config()
        
        path_obj = Path(path)
        has_csv = False
        
        if path_obj.is_dir():
            csv_files = list(path_obj.glob("*.csv"))
            has_csv = len(csv_files) > 0
        elif path_obj.is_file() and path_obj.suffix.lower() == '.csv':
            has_csv = True
        
        if has_csv:
            processor = create_document_processor(chunk_size=500, chunk_overlap=50)
            print("📊 CSV最適化チャンクサイズを使用: chunk_size=500, chunk_overlap=50")
        else:
            processor = create_document_processor(**config)
            print(f"📄 標準チャンクサイズを使用: chunk_size={config['chunk_size']}, chunk_overlap={config['chunk_overlap']}")
        
        documents = processor.load_documents_from_path(path)
        
        if documents:
            try:
                self.vector_store.add_documents(documents)
                print(f"✅ {len(documents)}個のドキュメントチャンクを追加しました")
                
                self._list_loaded_sources(documents)
            except Exception as e:
                print(f"❌ ベクトルストアへの追加エラー: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("❌ ドキュメントの読み込みに失敗しました")
    
    def _list_loaded_sources(self, documents):
        """読み込まれたドキュメントの出典一覧を表示"""
        sources = {}
        for doc in documents:
            source = doc.metadata.get('source', '不明')
            if source not in sources:
                sources[source] = 0
            sources[source] += 1
        
        print("\n📋 読み込まれたファイル一覧:")
        for source, count in sources.items():
            print(f"  📄 {source} ({count}チャンク)")
        print()
    
    def add_documents_from_text(self, text: str, metadata: Optional[dict] = None):
        """テキストからドキュメントを追加"""
        from .document_loader import create_document_processor
        
        processor = create_document_processor()
        documents = processor.process_raw_text(text, metadata)
        
        if documents:
            self.vector_store.add_documents(documents)
            print(f"✅ {len(documents)}個のテキストチャンクを追加しました")
    
    def chat(self, message: str) -> str:
        """チャット実行"""
        try:
            response = self.agent_executor.invoke({"input": message})
            return response["output"]
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"
    
    def save_vector_store(self, path: str):
        """ベクトルストアを保存"""
        self.vector_store.save(path)
        print(f"✅ ベクトルストアを保存しました: {path}")
    
    def load_vector_store(self, path: str):
        """ベクトルストアを読み込み"""
        self.vector_store.load(path)
        print(f"✅ ベクトルストアを読み込みました: {path}")

def create_rag_agent(**kwargs) -> RAGAgent:
    """RAGエージェントファクトリー"""
    return RAGAgent(**kwargs)

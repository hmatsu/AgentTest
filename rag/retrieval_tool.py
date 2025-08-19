"""
RAG検索ツール
LangChainエージェントで使用するRAG検索ツールの実装
"""
from typing import List, Optional, Type, Any
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain.schema import Document

from .vector_store import VectorStoreManager

class RAGSearchInput(BaseModel):
    """RAG検索ツールの入力スキーマ"""
    query: str = Field(description="検索クエリ")
    k: int = Field(default=4, description="取得する文書数")

class RAGSearchTool(BaseTool):
    """RAG検索ツール"""
    name: str = "rag_search"
    description: str = "ドキュメントベースから関連情報を検索します。質問に関連する文書を見つけるために使用してください。"
    args_schema: Type[BaseModel] = RAGSearchInput
    vector_store: Any = Field(description="Vector store for document retrieval")
    
    class Config:
        arbitrary_types_allowed = True
    
    def _run(self, query: str, k: int = 4) -> str:
        """RAG検索を実行"""
        try:
            documents = self.vector_store.similarity_search(query, k=k)
            
            if not documents:
                return "関連する文書が見つかりませんでした。"
            
            result = f"検索クエリ「{query}」に関連する文書を{len(documents)}件見つけました:\n\n"
            
            for i, doc in enumerate(documents, 1):
                content = doc.page_content[:500]  # 最初の500文字
                if len(doc.page_content) > 500:
                    content += "..."
                
                source = doc.metadata.get('source', '不明')
                result += f"【文書{i}】(出典: {source})\n{content}\n\n"
            
            return result
            
        except Exception as e:
            return f"検索エラーが発生しました: {str(e)}"
    
    async def _arun(self, query: str, k: int = 4) -> str:
        """非同期実行（同期版を呼び出し）"""
        return self._run(query, k)

class RAGSummarizeTool(BaseTool):
    """RAG要約ツール"""
    name: str = "rag_summarize"
    description: str = "検索した文書の内容を要約します。長い文書の概要を把握するために使用してください。"
    args_schema: Type[BaseModel] = RAGSearchInput
    vector_store: Any = Field(description="Vector store for document retrieval")
    
    class Config:
        arbitrary_types_allowed = True
    
    def _run(self, query: str, k: int = 4) -> str:
        """RAG要約を実行"""
        try:
            documents = self.vector_store.similarity_search(query, k=k)
            
            if not documents:
                return "要約する文書が見つかりませんでした。"
            
            all_content = "\n".join([doc.page_content for doc in documents])
            
            sentences = all_content.split('。')
            summary_sentences = sentences[:3]  # 最初の3文
            
            result = f"検索クエリ「{query}」に関連する文書の要約:\n\n"
            result += "。".join(summary_sentences) + "。\n\n"
            result += f"（{len(documents)}件の文書から要約）"
            
            return result
            
        except Exception as e:
            return f"要約エラーが発生しました: {str(e)}"
    
    async def _arun(self, query: str, k: int = 4) -> str:
        """非同期実行（同期版を呼び出し）"""
        return self._run(query, k)

def create_rag_tools(vector_store: VectorStoreManager) -> List[BaseTool]:
    """RAGツールのリストを作成"""
    return [
        RAGSearchTool(vector_store=vector_store),
        RAGSummarizeTool(vector_store=vector_store)
    ]

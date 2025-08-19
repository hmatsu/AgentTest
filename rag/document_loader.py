"""
ドキュメント読み込みと前処理
PDF、テキスト、Webページなど様々な形式をサポート
"""
import os
from typing import List, Optional
from pathlib import Path

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader, 
    PyPDFLoader, 
    DirectoryLoader,
    WebBaseLoader,
    CSVLoader
)

class DocumentProcessor:
    """ドキュメント処理クラス"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def load_text_file(self, file_path: str) -> List[Document]:
        """テキストファイルを読み込み"""
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            documents = loader.load()
            return self.text_splitter.split_documents(documents)
        except Exception as e:
            print(f"テキストファイル読み込みエラー: {e}")
            return []
    
    def load_pdf_file(self, file_path: str) -> List[Document]:
        """PDFファイルを読み込み"""
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            return self.text_splitter.split_documents(documents)
        except Exception as e:
            print(f"PDFファイル読み込みエラー: {e}")
            return []
    
    def load_csv_file(self, file_path: str) -> List[Document]:
        """CSVファイルを読み込み"""
        try:
            loader = CSVLoader(file_path)
            documents = loader.load()
            return self.text_splitter.split_documents(documents)
        except Exception as e:
            print(f"CSVファイル読み込みエラー: {e}")
            return []
    
    def load_directory(self, directory_path: str, glob_pattern: str = "**/*.txt") -> List[Document]:
        """ディレクトリから複数ファイルを読み込み"""
        try:
            loader = DirectoryLoader(
                directory_path, 
                glob=glob_pattern,
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'}
            )
            documents = loader.load()
            return self.text_splitter.split_documents(documents)
        except Exception as e:
            print(f"ディレクトリ読み込みエラー: {e}")
            return []
    
    def load_web_pages(self, urls: List[str]) -> List[Document]:
        """Webページを読み込み"""
        try:
            loader = WebBaseLoader(urls)
            documents = loader.load()
            return self.text_splitter.split_documents(documents)
        except Exception as e:
            print(f"Webページ読み込みエラー: {e}")
            return []
    
    def load_documents_from_path(self, path: str) -> List[Document]:
        """パスから自動的にドキュメントを読み込み"""
        path_obj = Path(path)
        
        if not path_obj.exists():
            print(f"パスが存在しません: {path}")
            return []
        
        if path_obj.is_file():
            suffix = path_obj.suffix.lower()
            if suffix == '.txt':
                return self.load_text_file(path)
            elif suffix == '.pdf':
                return self.load_pdf_file(path)
            elif suffix == '.csv':
                return self.load_csv_file(path)
            else:
                print(f"サポートされていないファイル形式: {suffix}")
                return []
        
        elif path_obj.is_dir():
            return self.load_directory(path)
        
        else:
            print(f"無効なパス: {path}")
            return []
    
    def process_raw_text(self, text: str, metadata: Optional[dict] = None) -> List[Document]:
        """生テキストを処理"""
        if metadata is None:
            metadata = {}
        
        document = Document(page_content=text, metadata=metadata)
        return self.text_splitter.split_documents([document])

def create_document_processor(chunk_size: int = 1000, chunk_overlap: int = 200) -> DocumentProcessor:
    """ドキュメントプロセッサーファクトリー"""
    return DocumentProcessor(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

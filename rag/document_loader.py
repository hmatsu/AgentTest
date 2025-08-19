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
            if not os.path.exists(file_path):
                print(f"PDFファイルが存在しません: {file_path}")
                return []
            
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            if not documents:
                print(f"PDFファイルからドキュメントを読み込めませんでした: {file_path}")
                return []
            
            split_documents = self.text_splitter.split_documents(documents)
            print(f"PDFファイル読み込み成功: {len(documents)}ページ, {len(split_documents)}チャンク")
            return split_documents
            
        except ImportError as e:
            print(f"PDF読み込みに必要なライブラリが不足しています: {e}")
            print("pip install pypdf をお試しください")
            return []
        except Exception as e:
            print(f"PDFファイル読み込みエラー ({file_path}): {e}")
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
            return self.load_directory_all_types(path)
        
        else:
            print(f"無効なパス: {path}")
            return []
    
    def load_directory_all_types(self, directory_path: str) -> List[Document]:
        """ディレクトリから全ての対応ファイル形式を読み込み"""
        all_documents = []
        directory = Path(directory_path)
        
        if not directory.exists() or not directory.is_dir():
            print(f"ディレクトリが存在しません: {directory_path}")
            return []
        
        supported_extensions = {'.txt': self.load_text_file, '.pdf': self.load_pdf_file, '.csv': self.load_csv_file}
        
        for file_path in directory.iterdir():
            if file_path.is_file():
                suffix = file_path.suffix.lower()
                if suffix in supported_extensions:
                    print(f"  📄 {file_path.name} を処理中...")
                    try:
                        documents = supported_extensions[suffix](str(file_path))
                        if documents:
                            all_documents.extend(documents)
                            print(f"    ✅ {len(documents)}個のチャンクを読み込みました")
                        else:
                            print(f"    ⚠️  {file_path.name} からドキュメントを読み込めませんでした")
                    except Exception as e:
                        print(f"    ❌ {file_path.name} の読み込みエラー: {e}")
        
        return all_documents
    
    def process_raw_text(self, text: str, metadata: Optional[dict] = None) -> List[Document]:
        """生テキストを処理"""
        if metadata is None:
            metadata = {}
        
        document = Document(page_content=text, metadata=metadata)
        return self.text_splitter.split_documents([document])

def create_document_processor(chunk_size: int = 1000, chunk_overlap: int = 200) -> DocumentProcessor:
    """ドキュメントプロセッサーファクトリー"""
    return DocumentProcessor(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

#!/usr/bin/env python3
"""
詳細なPDF読み込みデバッグスクリプト
各ステップでの状態を詳細に追跡
"""
import os
import traceback
from pathlib import Path

def debug_pdf_loading_detailed():
    """PDF読み込みの各ステップを詳細にデバッグ"""
    print("🔍 詳細PDF読み込みデバッグ開始")
    
    documents_dir = "documents"
    print(f"📁 ディレクトリチェック: {documents_dir}")
    
    if not os.path.exists(documents_dir):
        print(f"❌ {documents_dir}ディレクトリが存在しません")
        return
    
    print(f"✅ {documents_dir}ディレクトリが存在します")
    
    files = os.listdir(documents_dir)
    print(f"📄 ディレクトリ内容 ({len(files)}個のファイル):")
    for file in files:
        file_path = os.path.join(documents_dir, file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size} bytes)")
    
    pdf_files = [f for f in files if f.endswith('.pdf')]
    if not pdf_files:
        print("❌ PDFファイルが見つかりません")
        return
    
    print(f"📄 PDFファイル: {pdf_files}")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(documents_dir, pdf_file)
        print(f"\n🧪 {pdf_file} の詳細テスト:")
        print(f"   パス: {pdf_path}")
        print(f"   サイズ: {os.path.getsize(pdf_path)} bytes")
        
        try:
            from langchain_community.document_loaders import PyPDFLoader
            print("   ✅ PyPDFLoader import成功")
        except Exception as e:
            print(f"   ❌ PyPDFLoader import失敗: {e}")
            continue
        
        try:
            loader = PyPDFLoader(pdf_path)
            print("   ✅ PyPDFLoader初期化成功")
        except Exception as e:
            print(f"   ❌ PyPDFLoader初期化失敗: {e}")
            traceback.print_exc()
            continue
        
        try:
            documents = loader.load()
            print(f"   ✅ ドキュメント読み込み成功: {len(documents)}ページ")
            
            if documents:
                first_doc = documents[0]
                print(f"   📖 最初のページ内容プレビュー:")
                content_preview = first_doc.page_content[:200].replace('\n', ' ')
                print(f"      {content_preview}...")
                print(f"   📋 メタデータ: {first_doc.metadata}")
            
        except Exception as e:
            print(f"   ❌ ドキュメント読み込み失敗: {e}")
            traceback.print_exc()
            continue
        
        try:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            split_documents = text_splitter.split_documents(documents)
            print(f"   ✅ テキスト分割成功: {len(split_documents)}チャンク")
            
        except Exception as e:
            print(f"   ❌ テキスト分割失敗: {e}")
            traceback.print_exc()
            continue
        
        try:
            from rag.document_loader import create_document_processor
            processor = create_document_processor()
            processed_docs = processor.load_pdf_file(pdf_path)
            print(f"   ✅ DocumentProcessor成功: {len(processed_docs)}チャンク")
            
        except Exception as e:
            print(f"   ❌ DocumentProcessor失敗: {e}")
            traceback.print_exc()
            continue
        
        try:
            dir_docs = processor.load_documents_from_path(documents_dir)
            print(f"   ✅ ディレクトリ読み込み成功: {len(dir_docs)}チャンク")
            
        except Exception as e:
            print(f"   ❌ ディレクトリ読み込み失敗: {e}")
            traceback.print_exc()
            continue
        
        print(f"   🎉 {pdf_file} の全テストが成功しました！")

if __name__ == "__main__":
    debug_pdf_loading_detailed()

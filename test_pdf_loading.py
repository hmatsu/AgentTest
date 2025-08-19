#!/usr/bin/env python3
"""
PDF読み込み機能のテスト
"""
import os
from rag.document_loader import create_document_processor

def test_pdf_loading():
    """PDF読み込み機能をテスト"""
    print("🧪 PDF読み込み機能のテスト開始")
    
    documents_dir = "documents"
    if not os.path.exists(documents_dir):
        print(f"❌ {documents_dir}ディレクトリが存在しません")
        return
    
    files = os.listdir(documents_dir)
    pdf_files = [f for f in files if f.endswith('.pdf')]
    
    print(f"📁 {documents_dir}ディレクトリの内容:")
    for file in files:
        print(f"  📄 {file}")
    
    if not pdf_files:
        print("❌ PDFファイルが見つかりません")
        return
    
    print(f"\n📄 見つかったPDFファイル: {', '.join(pdf_files)}")
    
    processor = create_document_processor()
    
    print(f"\n📚 {documents_dir}ディレクトリから読み込み中...")
    documents = processor.load_documents_from_path(documents_dir)
    
    if documents:
        print(f"✅ 合計 {len(documents)}個のドキュメントチャンクを読み込みました")
        
        sources = {}
        for doc in documents:
            source = doc.metadata.get('source', '不明')
            if source not in sources:
                sources[source] = 0
            sources[source] += 1
        
        print("\n📋 読み込まれたファイル一覧:")
        for source, count in sources.items():
            print(f"  📄 {source} ({count}チャンク)")
        
        if documents:
            sample_doc = documents[0]
            content_preview = sample_doc.page_content[:200]
            if len(sample_doc.page_content) > 200:
                content_preview += "..."
            print(f"\n📖 サンプル内容 (最初のチャンク):")
            print(f"出典: {sample_doc.metadata.get('source', '不明')}")
            print(f"内容: {content_preview}")
    else:
        print("❌ ドキュメントの読み込みに失敗しました")

if __name__ == "__main__":
    test_pdf_loading()

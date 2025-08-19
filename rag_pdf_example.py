"""
PDF専用RAGエージェントの使用例
documentsディレクトリからPDFファイルを読み込んでRAG対応エージェントと対話
"""
import os
import sys

def list_loaded_sources(documents):
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

def main():
    print("🚀 PDF用RAGエージェントを初期化中...")
    
    documents_dir = "documents"
    if not os.path.exists(documents_dir):
        print(f"❌ {documents_dir}ディレクトリが見つかりません")
        print(f"📁 {documents_dir}ディレクトリを作成してPDFファイルを配置してください")
        return
    
    pdf_files = [f for f in os.listdir(documents_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"❌ {documents_dir}ディレクトリにPDFファイルが見つかりません")
        print("📄 PDFファイルを配置してください")
        return
    
    print(f"📄 見つかったPDFファイル: {', '.join(pdf_files)}")
    
    try:
        try:
            from rag.document_loader import create_document_processor
            from rag.vector_store import create_vector_store
        except ImportError as e:
            print(f"❌ RAGモジュールのインポートに失敗しました: {e}")
            print("💡 pip install -r requirements.txt を実行してください")
            return
        
        print("📚 PDFファイルを読み込み中...")
        doc_processor = create_document_processor(chunk_size=500, chunk_overlap=50)
        
        all_documents = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(documents_dir, pdf_file)
            print(f"  📄 {pdf_file} を処理中...")
            try:
                documents = doc_processor.load_pdf_file(pdf_path)
                if documents:
                    all_documents.extend(documents)
                    print(f"    ✅ {len(documents)}個のチャンクを読み込みました")
                else:
                    print(f"    ⚠️  {pdf_file} は空またはサポートされていない形式です")
            except Exception as e:
                print(f"    ❌ {pdf_file} の読み込みエラー: {e}")
                print(f"    💡 ファイルが破損していないか確認してください")
        
        if not all_documents:
            print("❌ PDFファイルの読み込みに失敗しました")
            return
        
        print(f"✅ 合計 {len(all_documents)}個のドキュメントチャンクを読み込みました")
        
        list_loaded_sources(all_documents)
        
        print("🔍 ベクトルストアを作成中...")
        vector_store = create_vector_store("chroma")
        vector_store.add_documents(all_documents)
        print("✅ ベクトルストアの作成が完了しました")
        
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            print("✅ OpenAI APIキーが設定されています - フル機能のRAGエージェントを使用")
            try:
                from rag.rag_agent import create_rag_agent
                agent = create_rag_agent(vector_store)
                use_full_agent = True
            except Exception as e:
                print(f"⚠️  RAGエージェントの作成に失敗: {e}")
                print("💡 シンプルな検索機能を使用します")
                use_full_agent = False
        else:
            print("⚠️  OpenAI APIキーが設定されていません")
            print("💡 シンプルな検索機能を使用します（HuggingFace埋め込み）")
            use_full_agent = False
        
        print("\n" + "="*50)
        if use_full_agent:
            print("🎯 RAGエージェントとの対話を開始します")
            print("💡 PDFの内容に関する質問をどうぞ")
        else:
            print("🎯 ドキュメント検索機能を開始します")
            print("💡 PDFの内容に関する検索クエリを入力してください")
        print("📝 'quit'または'終了'で終了します")
        print("="*50)
        
        while True:
            try:
                if use_full_agent:
                    user_input = input("\n質問: ").strip()
                else:
                    user_input = input("\n検索クエリ: ").strip()
                
                if user_input.lower() in ['quit', '終了', 'exit']:
                    print("👋 終了します")
                    break
                
                if not user_input:
                    continue
                
                if use_full_agent:
                    print("\n🤖 回答:")
                    response = agent.invoke({"input": user_input})
                    print(response.get("output", "回答を生成できませんでした"))
                else:
                    print("\n🔍 検索結果:")
                    results = vector_store.similarity_search(user_input, k=5)
                    
                    if not results:
                        print("関連する情報が見つかりませんでした")
                    else:
                        for i, doc in enumerate(results, 1):
                            content = doc.page_content[:300]
                            if len(doc.page_content) > 300:
                                content += "..."
                            source = doc.metadata.get('source', '不明')
                            page = doc.metadata.get('page', '不明')
                            print(f"\n【結果{i}】(出典: {source}, ページ: {page})")
                            print(content)
                
            except KeyboardInterrupt:
                print("\n👋 終了します")
                break
            except Exception as e:
                print(f"❌ エラーが発生しました: {e}")
                continue
    
    except Exception as e:
        print(f"❌ 初期化に失敗しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

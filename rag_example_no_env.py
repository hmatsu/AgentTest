"""
RAGエージェントの使用例（.env不要版）
エンコーディング問題を回避してRAG対応エージェントと対話
"""
import os
import sys

def main():
    print("🚀 RAGエージェント（.env不要版）を初期化中...")
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OpenAI APIキーが設定されていません")
        print("💡 HuggingFaceの無料エンベディングモデルを使用します")
    else:
        print("✅ OpenAI APIキーが設定されています")
    
    documents_dir = "documents"
    if not os.path.exists(documents_dir):
        print(f"❌ {documents_dir}ディレクトリが見つかりません")
        print(f"📁 {documents_dir}ディレクトリを作成してドキュメントを配置してください")
        return
    
    doc_files = []
    for ext in ['.txt', '.pdf', '.csv']:
        doc_files.extend([f for f in os.listdir(documents_dir) if f.endswith(ext)])
    
    if not doc_files:
        print(f"❌ {documents_dir}ディレクトリにドキュメントが見つかりません")
        print("📄 サポートされている形式: .txt, .pdf, .csv")
        return
    
    print(f"📄 見つかったドキュメント: {', '.join(doc_files)}")
    
    try:
        try:
            from rag.document_loader import create_document_processor
            from rag.vector_store import create_vector_store
        except ImportError as e:
            print(f"❌ RAGモジュールのインポートに失敗しました: {e}")
            print("💡 pip install -r requirements.txt を実行してください")
            return
        
        print("📚 ドキュメントを読み込み中...")
        doc_processor = create_document_processor()
        documents = doc_processor.load_directory(documents_dir, "**/*")
        
        if not documents:
            print("❌ ドキュメントの読み込みに失敗しました")
            return
        
        print(f"✅ {len(documents)}個のドキュメントチャンクを読み込みました")
        
        print("🔍 ベクトルストアを作成中...")
        vector_store = create_vector_store("chroma")
        vector_store.add_documents(documents)
        print("✅ ベクトルストアの作成が完了しました")
        
        print("\n" + "="*50)
        print("🎯 ドキュメント検索機能をテストします")
        print("💡 ドキュメントに関する質問をどうぞ")
        print("📝 'quit'または'終了'で終了します")
        print("="*50)
        
        while True:
            try:
                user_input = input("\n検索クエリ: ").strip()
                
                if user_input.lower() in ['quit', '終了', 'exit']:
                    print("👋 検索機能を終了します")
                    break
                
                if not user_input:
                    continue
                
                print("\n🔍 検索結果:")
                results = vector_store.similarity_search(user_input, k=3)
                
                if not results:
                    print("関連するドキュメントが見つかりませんでした")
                else:
                    for i, doc in enumerate(results, 1):
                        content = doc.page_content[:200]
                        if len(doc.page_content) > 200:
                            content += "..."
                        source = doc.metadata.get('source', '不明')
                        print(f"\n【結果{i}】(出典: {source})")
                        print(content)
                
            except KeyboardInterrupt:
                print("\n👋 検索機能を終了します")
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

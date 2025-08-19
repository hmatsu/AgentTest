"""
CSV読み込み問題の詳細診断スクリプト
"""
import os
import sys
from pathlib import Path

def test_csv_loading():
    print("🔍 CSV読み込み問題を診断中...")
    
    documents_dir = "documents"
    if not os.path.exists(documents_dir):
        print(f"❌ {documents_dir}ディレクトリが見つかりません")
        return
    
    csv_files = [f for f in os.listdir(documents_dir) if f.endswith('.csv')]
    if not csv_files:
        print(f"❌ {documents_dir}ディレクトリにCSVファイルが見つかりません")
        return
    
    csv_path = os.path.join(documents_dir, csv_files[0])
    print(f"✅ CSVファイルが見つかりました: {csv_path}")
    
    file_size = os.path.getsize(csv_path)
    print(f"📊 ファイルサイズ: {file_size} bytes")
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            first_lines = [f.readline().strip() for _ in range(3)]
        print("📄 ファイルの最初の3行:")
        for i, line in enumerate(first_lines, 1):
            print(f"  {i}: {line[:100]}{'...' if len(line) > 100 else ''}")
    except UnicodeDecodeError as e:
        print(f"❌ UTF-8エンコーディングエラー: {e}")
        try:
            with open(csv_path, 'r', encoding='shift_jis') as f:
                first_lines = [f.readline().strip() for _ in range(3)]
            print("📄 Shift_JISで読み込んだ最初の3行:")
            for i, line in enumerate(first_lines, 1):
                print(f"  {i}: {line[:100]}{'...' if len(line) > 100 else ''}")
        except Exception as e2:
            print(f"❌ Shift_JISでも読み込み失敗: {e2}")
    except Exception as e:
        print(f"❌ ファイル読み込みエラー: {e}")
    
    print("\n🔧 依存関係の確認:")
    try:
        import pandas as pd
        print("✅ pandas がインストールされています")
    except ImportError:
        print("❌ pandas がインストールされていません")
    
    try:
        from langchain_community.document_loaders import CSVLoader
        print("✅ CSVLoader がインポートできます")
    except ImportError as e:
        print(f"❌ CSVLoader のインポートに失敗: {e}")
        return
    
    print("\n🧪 CSVLoaderの詳細テスト:")
    try:
        loader = CSVLoader(csv_path)
        print("✅ CSVLoader インスタンス作成成功")
        
        documents = loader.load()
        print(f"✅ ドキュメント読み込み成功: {len(documents)}個のドキュメント")
        
        if documents:
            first_doc = documents[0]
            print(f"📄 最初のドキュメント:")
            print(f"  内容: {first_doc.page_content[:200]}{'...' if len(first_doc.page_content) > 200 else ''}")
            print(f"  メタデータ: {first_doc.metadata}")
        
    except Exception as e:
        print(f"❌ CSVLoader エラー: {e}")
        print(f"エラータイプ: {type(e).__name__}")
        import traceback
        traceback.print_exc()
    
    print("\n🔄 代替方法でのCSV読み込みテスト:")
    try:
        import pandas as pd
        df = pd.read_csv(csv_path)
        print(f"✅ pandas で読み込み成功: {len(df)}行, {len(df.columns)}列")
        print(f"📊 列名: {list(df.columns)}")
        if len(df) > 0:
            print(f"📄 最初の行: {df.iloc[0].to_dict()}")
    except Exception as e:
        print(f"❌ pandas での読み込み失敗: {e}")

if __name__ == "__main__":
    test_csv_loading()

"""
CSVファイルの検証スクリプト
RAG読み込み前にCSVファイルの形式を確認
"""
import os
import csv
from pathlib import Path

def validate_csv_files():
    print("📋 CSVファイルの検証を開始します...")
    
    documents_dir = "documents"
    if not os.path.exists(documents_dir):
        print(f"❌ {documents_dir}ディレクトリが見つかりません")
        return False
    
    csv_files = [f for f in os.listdir(documents_dir) if f.endswith('.csv')]
    if not csv_files:
        print(f"❌ {documents_dir}ディレクトリにCSVファイルが見つかりません")
        return False
    
    all_valid = True
    for csv_file in csv_files:
        csv_path = os.path.join(documents_dir, csv_file)
        print(f"\n📄 {csv_file} を検証中...")
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                content = f.read(100)
            print("  ✅ UTF-8エンコーディング")
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
            
            if len(rows) == 0:
                print("  ❌ ファイルが空です")
                all_valid = False
                continue
            
            print(f"  ✅ {len(rows)}行のデータ")
            print(f"  ✅ {len(rows[0])}列のデータ")
            
            if len(rows) > 0:
                print(f"  📊 ヘッダー: {rows[0]}")
            
        except UnicodeDecodeError:
            print("  ❌ UTF-8エンコーディングエラー")
            print("  💡 ファイルをUTF-8で保存し直してください")
            all_valid = False
        except Exception as e:
            print(f"  ❌ エラー: {e}")
            all_valid = False
    
    return all_valid

if __name__ == "__main__":
    if validate_csv_files():
        print("\n✅ すべてのCSVファイルが有効です")
        print("💡 python rag_csv_example.py でRAG読み込みを開始できます")
    else:
        print("\n❌ 一部のCSVファイルに問題があります")
        print("💡 エラーを修正してから再度実行してください")

"""
.envファイルのエンコーディング問題を修正するスクリプト
"""
import os
import sys

def fix_env_encoding():
    """
    .envファイルをUTF-8エンコーディングで再保存する
    """
    env_file = ".env"
    
    if not os.path.exists(env_file):
        print(f"❌ {env_file}ファイルが見つかりません")
        return False
    
    try:
        encodings = ['utf-8', 'shift-jis', 'cp932', 'windows-1252', 'iso-8859-1']
        content = None
        original_encoding = None
        
        for encoding in encodings:
            try:
                with open(env_file, 'r', encoding=encoding) as f:
                    content = f.read()
                original_encoding = encoding
                print(f"✅ {encoding}エンコーディングで読み込み成功")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print("❌ どのエンコーディングでも読み込めませんでした")
            return False
        
        backup_file = f"{env_file}.backup"
        with open(backup_file, 'w', encoding=original_encoding) as f:
            f.write(content)
        print(f"📁 バックアップを作成: {backup_file}")
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {env_file}をUTF-8エンコーディングで保存しました")
        
        return True
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return False

def create_clean_env():
    """
    クリーンな.envファイルを作成
    """
    env_content = """# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

"""
    
    try:
        with open(".env", 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ 新しい.envファイルを作成しました")
        print("📝 .envファイルを編集してOPENAI_API_KEYを設定してください")
        return True
    except Exception as e:
        print(f"❌ .envファイルの作成に失敗: {e}")
        return False

def main():
    """メイン処理"""
    print("=== .envファイル エンコーディング修正ツール ===\n")
    
    if os.path.exists(".env"):
        print("既存の.envファイルが見つかりました")
        choice = input("修正を試行しますか？ (y/n): ").strip().lower()
        
        if choice in ['y', 'yes', 'はい']:
            if fix_env_encoding():
                print("\n🎉 修正が完了しました！")
                print("python simple_qa_agent_fixed.py を実行してテストしてください")
            else:
                print("\n修正に失敗しました。新しいファイルを作成しますか？")
                choice2 = input("新規作成 (y/n): ").strip().lower()
                if choice2 in ['y', 'yes', 'はい']:
                    create_clean_env()
        else:
            print("修正をキャンセルしました")
    else:
        print(".envファイルが見つかりません。新規作成します")
        create_clean_env()

if __name__ == "__main__":
    main()

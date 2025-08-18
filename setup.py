"""
プロジェクトのセットアップスクリプト
"""
import os
import subprocess
import sys

def check_python_version():
    """Python バージョンをチェック"""
    if sys.version_info < (3, 8):
        print("エラー: Python 3.8以上が必要です")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} を使用")
    return True

def install_requirements():
    """依存関係をインストール"""
    print("📦 依存関係をインストール中...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依存関係のインストールが完了しました")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依存関係のインストールに失敗しました: {e}")
        return False

def setup_env_file():
    """環境変数ファイルをセットアップ"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("📝 .envファイルを作成中...")
            with open(".env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())
            print("✅ .envファイルを作成しました")
            print("⚠️  .envファイルを編集してOPENAI_API_KEYを設定してください")
        else:
            print("❌ .env.exampleファイルが見つかりません")
            return False
    else:
        print("✅ .envファイルは既に存在します")
    return True

def check_api_key():
    """APIキーの設定をチェック"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  OPENAI_API_KEYが設定されていません")
        print("   .envファイルを編集してAPIキーを設定してください")
        return False
    else:
        print("✅ OPENAI_API_KEYが設定されています")
        return True

def main():
    """セットアップメイン処理"""
    print("🚀 LangChain エージェントプロジェクトのセットアップを開始します\n")
    
    if not check_python_version():
        return
    
    if not install_requirements():
        return
    
    if not setup_env_file():
        return
    
    api_key_ok = check_api_key()
    
    print("\n" + "="*50)
    print("🎉 セットアップが完了しました！")
    print("\n次のステップ:")
    
    if not api_key_ok:
        print("1. .envファイルを編集してOPENAI_API_KEYを設定")
        print("2. python simple_qa_agent.py を実行してテスト")
    else:
        print("1. python simple_qa_agent.py を実行してテスト")
    
    print("\nその他の実行例:")
    print("- python main.py (検索機能付きエージェント)")
    print("- python examples.py (複数のエージェント例)")

if __name__ == "__main__":
    main()

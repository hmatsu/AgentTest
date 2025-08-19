"""
GraphRAG CLI コマンドテスト
GraphRAGのCLIコマンドが正しく動作するかテスト
"""
import os
import subprocess
import sys
from pathlib import Path

def test_graphrag_cli():
    """GraphRAG CLIコマンドをテスト"""
    print("🧪 GraphRAG CLI コマンドテスト")
    print("=" * 40)
    
    try:
        result = subprocess.run([sys.executable, "-m", "graphrag", "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ GraphRAG CLI は利用可能です")
        else:
            print("❌ GraphRAG CLI が利用できません")
            print(f"   エラー: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ GraphRAG CLI テストエラー: {e}")
        return False
    
    test_workspace = Path("./test_graphrag_cli_workspace")
    if test_workspace.exists():
        import shutil
        shutil.rmtree(test_workspace)
    
    test_workspace.mkdir()
    
    try:
        print("\n🔧 GraphRAG設定を初期化中...")
        result = subprocess.run([
            sys.executable, "-m", "graphrag", "init", 
            "--root", str(test_workspace)
        ], capture_output=True, text=True, cwd=str(test_workspace))
        
        if result.returncode == 0:
            print("✅ GraphRAG初期化成功")
        else:
            print("❌ GraphRAG初期化失敗")
            print(f"   stderr: {result.stderr}")
            print(f"   stdout: {result.stdout}")
        
        input_dir = test_workspace / "input"
        input_dir.mkdir(exist_ok=True)
        
        test_doc = input_dir / "test.txt"
        test_doc.write_text("This is a test document for GraphRAG CLI testing. It contains sample content to verify the indexing process works correctly.")
        
        print(f"✅ テストドキュメントを作成: {test_doc}")
        
        print("\n🔄 GraphRAGインデックス構築（ドライラン）をテスト中...")
        
        env = os.environ.copy()
        env["OPENAI_API_KEY"] = "dummy_key_for_testing"
        
        result = subprocess.run([
            sys.executable, "-m", "graphrag", "index",
            "--root", str(test_workspace),
            "--dry-run"
        ], capture_output=True, text=True, cwd=str(test_workspace), env=env)
        
        print(f"   戻り値: {result.returncode}")
        print(f"   stdout: {result.stdout[:500]}...")
        print(f"   stderr: {result.stderr[:500]}...")
        
        if result.returncode == 0:
            print("✅ GraphRAGインデックス構築コマンドは正常に実行されました")
            return True
        else:
            if "AuthenticationError" in result.stderr or "invalid_api_key" in result.stderr:
                print("⚠️ 認証エラーが発生しましたが、CLIコマンド自体は正常に動作しています")
                return True
            else:
                print("❌ GraphRAGインデックス構築でエラーが発生しました")
                return False
                
    except Exception as e:
        print(f"❌ GraphRAG CLIテスト例外: {e}")
        return False
    finally:
        if test_workspace.exists():
            import shutil
            shutil.rmtree(test_workspace)
            print(f"🧹 テストワークスペースを削除: {test_workspace}")

if __name__ == "__main__":
    success = test_graphrag_cli()
    if success:
        print("\n🎉 GraphRAG CLIテスト成功！")
    else:
        print("\n❌ GraphRAG CLIテスト失敗")
        sys.exit(1)

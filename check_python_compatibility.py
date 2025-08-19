"""
Python互換性チェックスクリプト
GraphRAGの要件を確認
"""
import sys

def check_python_version():
    """Python バージョンをチェック"""
    version = sys.version_info
    print(f"🐍 現在のPythonバージョン: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 13):
        print("❌ GraphRAGはPython 3.13をサポートしていません")
        print("✅ 推奨: Python 3.10, 3.11, または 3.12を使用してください")
        return False
    elif version >= (3, 10):
        print("✅ GraphRAG対応バージョンです")
        return True
    else:
        print("❌ Python 3.10以上が必要です")
        return False

def check_graphrag_availability():
    """GraphRAGライブラリの利用可能性をチェック"""
    try:
        import graphrag
        print(f"✅ GraphRAGライブラリが利用可能です (バージョン: {getattr(graphrag, '__version__', '不明')})")
        return True
    except ImportError:
        print("❌ GraphRAGライブラリがインストールされていません")
        if sys.version_info >= (3, 13):
            print("   Python 3.13では現在サポートされていません")
        else:
            print("   pip install graphrag でインストールしてください")
        return False

def main():
    """メインチェック"""
    print("🔍 GraphRAG互換性チェック")
    print("=" * 40)
    
    python_ok = check_python_version()
    print()
    
    if python_ok:
        graphrag_ok = check_graphrag_availability()
        print()
        
        if graphrag_ok:
            print("🎉 GraphRAG機能を使用できます！")
            return True
        else:
            print("⚠️ GraphRAGライブラリをインストールしてください")
            return False
    else:
        print("⚠️ 従来のRAG機能のみ使用可能です")
        return False

if __name__ == "__main__":
    main()

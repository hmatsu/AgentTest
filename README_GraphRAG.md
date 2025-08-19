# GraphRAG実装ガイド

## Python バージョン要件

GraphRAG機能を使用するには、**Python 3.10-3.12**が必要です。

### サポート状況
- ✅ Python 3.10: 完全サポート
- ✅ Python 3.11: 完全サポート  
- ✅ Python 3.12: 完全サポート
- ❌ Python 3.13: 未サポート（GraphRAGライブラリの制限）

## セットアップ手順

### Python 3.10-3.12の場合

1. 依存関係をインストール:
```bash
pip install -r requirements.txt
```

2. 互換性チェック:
```bash
python check_python_compatibility.py
```

3. **重要**: OpenAI APIキーを設定:
```bash
# Windows
set OPENAI_API_KEY=your_openai_api_key_here

# Linux/Mac
export OPENAI_API_KEY=your_openai_api_key_here
```

4. GraphRAG CLIテスト:
```bash
python test_graphrag_cli.py
```

5. GraphRAG機能をテスト:
```bash
python graphrag_example.py
```

6. RAG vs GraphRAG比較:
```bash
python graph_rag_comparison.py
```

### Python 3.13の場合

Python 3.13では、GraphRAG機能は利用できませんが、従来のRAG機能は正常に動作します。

1. GraphRAGを除く依存関係をインストール:
```bash
pip install langchain>=0.1.0 langchain-openai>=0.1.0 langchain-community>=0.1.0 python-dotenv>=1.0.0 chromadb>=0.4.0 faiss-cpu>=1.7.4 sentence-transformers>=2.2.0 pypdf>=3.0.0 pydantic>=2.0.0 beautifulsoup4>=4.12.0 requests>=2.31.0 duckduckgo-search>=8.0.0
```

2. 従来のRAGのみを使用:
```bash
python rag_example.py
```

## 機能比較

| 機能 | 従来のRAG | GraphRAG |
|------|-----------|----------|
| ベクトル類似度検索 | ✅ | ✅ |
| エンティティ検索 | ❌ | ✅ |
| 関係性検索 | ❌ | ✅ |
| グラフベース推論 | ❌ | ✅ |
| フォールバック検索 | ❌ | ✅ |
| OpenAI API要件 | ❌ | ✅ |
| Python 3.13サポート | ✅ | ❌ |

## 注意事項

**GraphRAGの制限**:
- OpenAI APIキーが必要（有料）
- インデックス構築に時間がかかる場合がある
- 大量のドキュメントでは高いAPI使用料が発生する可能性

**フォールバック機能**:
- APIキーがない場合、自動的にフォールバック検索を使用
- 日本語-英語クロス言語検索をサポート
- 基本的なテキストマッチング機能を提供

## トラブルシューティング

### GraphRAGインストールエラー
```
ERROR: Could not find a version that satisfies the requirement graphrag>=2.5.0
```

**解決方法**: Python 3.10-3.12を使用してください。

### GraphRAGインデックス構築エラー
```
❌ GraphRAGインデックス構築エラー: AuthenticationError
```

**解決方法**: 有効なOpenAI APIキーが必要です。
1. [OpenAI Platform](https://platform.openai.com/account/api-keys)でAPIキーを取得
2. 環境変数に設定: `OPENAI_API_KEY=your_key_here`
3. APIキーなしでも、フォールバック検索機能は利用可能です

### 互換性チェック
```bash
python check_python_compatibility.py
```

### CLIコマンドテスト
```bash
python test_graphrag_cli.py
```

これらのスクリプトで現在の環境でGraphRAGが利用可能かチェックできます。

## 推奨環境

- **開発環境**: Python 3.12 (最新の安定版)
- **本番環境**: Python 3.11 または 3.12
- **OS**: Windows, macOS, Linux (すべてサポート)

## 参考リンク

- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [GraphRAG Documentation](https://microsoft.github.io/graphrag/)

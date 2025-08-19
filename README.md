# AgentTest

LangChainを用いたエージェントの実装プロジェクト（RAG対応）

## 🚀 クイックスタート

### 1. 自動セットアップ（推奨）
```bash
python setup.py
```

### 2. 手動セットアップ
```bash
# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
cp .env.example .env
# .envファイルを編集してOPENAI_API_KEYを設定
```

### 3. 動作確認
```bash
# シンプルなQ&Aエージェント（推奨）
python simple_qa_agent.py

# 検索機能付きエージェント
python main.py

# 複数のエージェント例
python examples.py

# RAGエージェント（新機能）
python rag_example.py

# 依存関係テスト
python test_rag_imports.py
```

## 📁 プロジェクト構造

```
AgentTest/
├── simple_qa_agent.py    # 🎯 シンプルなQ&Aエージェント（動作確認用）
├── main.py              # 検索機能付きエージェント
├── examples.py          # 複数のエージェントタイプの例
├── rag_example.py       # 🆕 RAGエージェントの例
├── test_rag_imports.py  # 🆕 RAG依存関係テスト
├── setup.py             # 自動セットアップスクリプト
├── requirements.txt     # 依存関係
├── .env.example         # 環境変数テンプレート
├── documents/           # 🆕 ドキュメント保存ディレクトリ
├── agent/               # エージェント実装
│   ├── __init__.py
│   └── custom_agent.py  # カスタムエージェントの例
├── tools/               # カスタムツール
│   ├── __init__.py
│   └── custom_tools.py  # 計算機、天気ツールの例
├── config/              # 設定管理
│   ├── __init__.py
│   ├── settings.py      # アプリケーション設定
│   └── rag_settings.py  # 🆕 RAG設定
└── rag/                 # 🆕 RAG機能
    ├── __init__.py
    ├── vector_store.py  # ベクトルストア管理
    ├── document_loader.py # ドキュメント読み込み
    ├── retrieval_tool.py # RAG検索ツール
    └── rag_agent.py     # RAGエージェント
```

## 🔧 必要な環境

- Python 3.8以上
- OpenAI API キー

## 💡 使用例

### シンプルなQ&A
```python
# simple_qa_agent.py を実行
python simple_qa_agent.py

# 質問例:
# - 日本の首都はどこですか？
# - Pythonとは何ですか？
# - 今日の天気はどうですか？
```

### 検索機能付きエージェント
```python
# main.py を実行
python main.py

# 質問例:
# - 最新のAIニュースを教えて
# - LangChainの最新バージョンは？
```

## 🆕 RAG機能

### RAG（Retrieval-Augmented Generation）とは
ドキュメントベースから関連情報を検索して、より正確で詳細な回答を生成する技術です。

### 主な機能
- **ベクトルストア**: Chroma、FAISS対応
- **エンベディング**: OpenAI、HuggingFace対応  
- **ドキュメント処理**: PDF、テキスト、CSV、Webページ
- **検索拡張**: 関連ドキュメントの自動検索と要約
- **統合エージェント**: 既存ツールとRAGの組み合わせ

### RAG使用方法

#### CSVファイルの読み込み

**重要**: CSVファイルを読み込む場合は、必ず `rag_csv_example.py` を使用してください。

```bash
# CSVファイル専用スクリプト（推奨）
python rag_csv_example.py

# 汎用ドキュメント読み込みスクリプト
python rag_example_no_env.py
```

**スクリプトの違い**:
- `rag_example.py`: 固定のサンプルデータを使用（LangChain、RAGの説明）
- `rag_csv_example.py`: documentsディレクトリからCSVファイルを読み込み
- `rag_example_no_env.py`: .envファイルを使わずに動作、全ファイル形式対応

CSVファイルは `documents/` ディレクトリに配置してください。

#### 1. ドキュメントの準備
```bash
# documentsディレクトリを作成
mkdir -p documents

# ドキュメントファイルを配置
cp your_documents.txt documents/
cp your_pdfs.pdf documents/
```

#### 2. RAGエージェントの使用
```python
from rag.rag_agent import create_rag_agent

# RAGエージェントを作成
agent = create_rag_agent()

# ドキュメントを追加
agent.add_documents_from_path("documents/")

# 質問
response = agent.chat("ドキュメントの内容について教えてください")
```

#### 3. 設定のカスタマイズ
`.env`ファイルで以下の設定が可能:
```bash
# ベクトルストア設定
VECTOR_STORE_TYPE=chroma  # chroma または faiss
EMBEDDING_MODEL=openai    # openai または huggingface

# チャンク設定
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
SEARCH_K=4

# Chroma設定
CHROMA_COLLECTION=documents
CHROMA_PERSIST_DIR=./chroma_db

# FAISS設定
FAISS_INDEX_PATH=./faiss_index
```

## 🔧 トラブルシューティング

### 依存関係の問題
```bash
# RAG依存関係をテスト
python test_rag_imports.py

# 不足している依存関係をインストール
pip install chromadb faiss-cpu sentence-transformers pypdf
```

### エンコーディングエラー（Windows）
```bash
# エンコーディング修正ツールを実行
python fix_encoding.py

# 修正版エージェントを使用
python simple_qa_agent_fixed.py
```

### API制限エラー
```bash
# オフラインテスト
python test_agent_offline.py
```

## 🎯 次のステップ

1. **カスタムツールの追加**: `tools/custom_tools.py`を編集
2. **エージェントのカスタマイズ**: `agent/custom_agent.py`を参考に
3. **設定の調整**: `config/settings.py`で各種パラメータを調整
4. **RAGドキュメントの追加**: `documents/`ディレクトリにファイルを配置
5. **RAGエージェントのテスト**: `python rag_example.py`で動作確認

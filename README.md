# AgentTest

LangChainを用いたエージェントの実装プロジェクト（RAG・GraphRAG対応）

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

# RAGエージェント
python rag_example.py

# GraphRAGエージェント（新機能）
python graphrag_example.py

# RAG vs GraphRAG 比較実験
python graph_rag_comparison.py

# 依存関係テスト
python test_rag_imports.py
```

## 📁 プロジェクト構造

```
AgentTest/
├── simple_qa_agent.py      # 🎯 シンプルなQ&Aエージェント（動作確認用）
├── main.py                # 検索機能付きエージェント
├── examples.py            # 複数のエージェントタイプの例
├── rag_example.py         # RAGエージェントの例
├── graphrag_example.py    # 🆕 GraphRAGエージェントの例
├── graph_rag_comparison.py # 🆕 RAG vs GraphRAG 比較実験
├── test_rag_imports.py    # RAG依存関係テスト
├── setup.py               # 自動セットアップスクリプト
├── requirements.txt       # 依存関係（GraphRAG対応）
├── .env.example           # 環境変数テンプレート
├── documents/             # ドキュメント保存ディレクトリ
├── graphrag_workspace/    # 🆕 GraphRAG作業ディレクトリ
│   ├── settings.yaml      # GraphRAG設定
│   ├── prompts/           # GraphRAGプロンプトテンプレート
│   ├── input/             # GraphRAG入力ファイル
│   ├── output/            # GraphRAGインデックス出力
│   └── logs/              # GraphRAGログ
├── agent/                 # エージェント実装
│   ├── __init__.py
│   └── custom_agent.py    # カスタムエージェントの例
├── tools/                 # カスタムツール
│   ├── __init__.py
│   └── custom_tools.py    # 計算機、天気ツールの例
├── config/                # 設定管理
│   ├── __init__.py
│   ├── settings.py        # アプリケーション設定
│   └── rag_settings.py    # RAG・GraphRAG設定
└── rag/                   # RAG・GraphRAG機能
    ├── __init__.py
    ├── vector_store.py    # ベクトルストア管理（GraphRAG対応）
    ├── document_loader.py # ドキュメント読み込み
    ├── retrieval_tool.py  # RAG・GraphRAG検索ツール
    └── rag_agent.py       # RAG・GraphRAGエージェント
```

## 🔧 必要な環境

### 基本要件
- **Python 3.8以上** (従来のRAG機能)
- **Python 3.10-3.12** (GraphRAG機能 - 推奨)
- **OpenAI API キー** (必須)

### Python バージョン別対応機能
- **Python 3.13**: 従来のRAGのみ対応
- **Python 3.10-3.12**: 従来のRAG + GraphRAG対応
- **Python 3.8-3.9**: 従来のRAGのみ対応

### 互換性確認
```bash
# Python バージョンと対応機能を確認
python check_python_compatibility.py
```

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

## 🆕 RAG・GraphRAG機能

### RAG（Retrieval-Augmented Generation）とは
ドキュメントベースから関連情報を検索して、より正確で詳細な回答を生成する技術です。

### GraphRAG（Graph-based RAG）とは
Microsoft GraphRAGを使用したグラフベースの検索拡張生成技術。エンティティ間の関係性を理解し、より複雑な質問に対応できます。

### 主な機能
- **ベクトルストア**: Chroma、FAISS、GraphRAG対応
- **エンベディング**: OpenAI、HuggingFace対応  
- **ドキュメント処理**: PDF、テキスト、CSV、Webページ
- **検索拡張**: 関連ドキュメントの自動検索と要約
- **グラフ検索**: エンティティ・関係性ベースの高度な検索
- **統合エージェント**: 既存ツールとRAG/GraphRAGの組み合わせ
- **比較実験**: RAG vs GraphRAG の性能比較機能

### RAG・GraphRAG使用方法

#### 基本的な使用方法

**スクリプトの使い分け**:
- `rag_example.py`: 従来のRAGエージェント（選択メニュー付き）
- `graphrag_example.py`: GraphRAGエージェント（選択メニュー付き）
- `graph_rag_comparison.py`: RAG vs GraphRAG 性能比較実験
- `rag_pdf_example.py`: PDF専用スクリプト
- `rag_csv_example.py`: CSV専用スクリプト
- `rag_example_no_env.py`: .envファイル不要版

```bash
# 従来のRAGエージェント
python rag_example.py
# 実行モードを選択:
# 1. 例の実行
# 2. インタラクティブチャット

# GraphRAGエージェント（Python 3.10-3.12が必要）
python graphrag_example.py
# 実行モードを選択:
# 1. 例の実行
# 2. インタラクティブチャット

# RAG vs GraphRAG 比較実験
python graph_rag_comparison.py

# 従来の専用スクリプト
python rag_pdf_example.py
python rag_csv_example.py
python rag_example_no_env.py
```

PDFファイルやCSVファイルは `documents/` ディレクトリに配置してください。

#### 1. ドキュメントの準備
```bash
# documentsディレクトリを作成
mkdir -p documents

# ドキュメントファイルを配置
cp your_documents.txt documents/
cp your_pdfs.pdf documents/
```

#### 2. RAG・GraphRAGエージェントの使用

**従来のRAGエージェント**:
```python
from rag.rag_agent import create_rag_agent

# RAGエージェントを作成
agent = create_rag_agent()

# ドキュメントを追加
agent.add_documents_from_path("documents/")

# 質問
response = agent.chat("ドキュメントの内容について教えてください")
```

**GraphRAGエージェント**:
```python
from rag.rag_agent import create_graphrag_agent

# GraphRAGエージェントを作成（Python 3.10-3.12が必要）
agent = create_graphrag_agent()

# ドキュメントを追加（GraphRAGインデックス構築）
agent.add_documents_from_path("documents/")

# 質問（エンティティ・関係性ベースの検索）
response = agent.chat("ドキュメント内のエンティティ間の関係性について教えてください")
```

**比較実験**:
```python
# 同じ質問で両方のアプローチを比較
rag_agent = create_rag_agent()
graphrag_agent = create_graphrag_agent()

# 同じドキュメントを読み込み
rag_agent.add_documents_from_path("documents/")
graphrag_agent.add_documents_from_path("documents/")

# 同じ質問で比較
query = "重要な概念とその関係性について説明してください"
rag_result = rag_agent.chat(query)
graphrag_result = graphrag_agent.chat(query)
```

#### 3. 設定のカスタマイズ
`.env`ファイルで以下の設定が可能:
```bash
# ベクトルストア設定
VECTOR_STORE_TYPE=chroma  # chroma, faiss, または graphrag
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

# GraphRAG設定
GRAPHRAG_WORKSPACE=./graphrag_workspace
GRAPHRAG_MODEL=gpt-3.5-turbo
GRAPHRAG_EMBEDDING_MODEL=text-embedding-ada-002
```

#### 4. GraphRAG固有の設定
`graphrag_workspace/settings.yaml`でGraphRAG固有の設定が可能:
```yaml
llm:
  api_key: ${OPENAI_API_KEY}
  type: openai_chat
  model: gpt-3.5-turbo

embeddings:
  api_key: ${OPENAI_API_KEY}
  type: openai_embedding
  model: text-embedding-ada-002

chunks:
  size: 1200
  overlap: 100
```

## 🔧 トラブルシューティング

### 依存関係の問題
```bash
# RAG依存関係をテスト
python test_rag_imports.py

# 従来のRAG依存関係をインストール
pip install chromadb faiss-cpu sentence-transformers pypdf

# GraphRAG依存関係をインストール（Python 3.10-3.12のみ）
pip install graphrag>=2.5.0

# Python バージョン互換性を確認
python check_python_compatibility.py
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
4. **ドキュメントの追加**: `documents/`ディレクトリにファイルを配置
5. **RAGエージェントのテスト**: `python rag_example.py`で動作確認
6. **GraphRAGエージェントのテスト**: `python graphrag_example.py`で動作確認
7. **性能比較実験**: `python graph_rag_comparison.py`でRAG vs GraphRAGを比較
8. **GraphRAG設定の調整**: `graphrag_workspace/settings.yaml`でGraphRAG固有の設定を調整

## 📊 RAG vs GraphRAG 比較

### 従来のRAGの特徴
- **高速**: ベクトル類似度検索による高速な検索
- **シンプル**: 設定が簡単で理解しやすい
- **汎用性**: 様々なドキュメント形式に対応
- **軽量**: 計算リソースの消費が少ない

### GraphRAGの特徴
- **高精度**: エンティティ・関係性を理解した検索
- **複雑な質問対応**: 複数エンティティ間の関係性を把握
- **構造化理解**: ドキュメントの構造的な理解
- **高コスト**: OpenAI APIの使用量が多い

### 使い分けの指針
- **シンプルな質問・高速検索**: 従来のRAG
- **複雑な関係性・構造的理解**: GraphRAG
- **コスト重視**: 従来のRAG
- **精度重視**: GraphRAG

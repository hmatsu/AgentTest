# AgentTest

LangChainを用いたエージェントの実装プロジェクト

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
```

## 📁 プロジェクト構造

```
AgentTest/
├── simple_qa_agent.py    # 🎯 シンプルなQ&Aエージェント（動作確認用）
├── main.py              # 検索機能付きエージェント
├── examples.py          # 複数のエージェントタイプの例
├── setup.py             # 自動セットアップスクリプト
├── requirements.txt     # 依存関係
├── .env.example         # 環境変数テンプレート
├── agent/               # エージェント実装
│   ├── __init__.py
│   └── custom_agent.py  # カスタムエージェントの例
├── tools/               # カスタムツール
│   ├── __init__.py
│   └── custom_tools.py  # 計算機、天気ツールの例
└── config/              # 設定管理
    ├── __init__.py
    └── settings.py      # アプリケーション設定
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

## 🎯 次のステップ

1. **カスタムツールの追加**: `tools/custom_tools.py`を編集
2. **エージェントのカスタマイズ**: `agent/custom_agent.py`を参考に
3. **設定の調整**: `config/settings.py`で各種パラメータを調整

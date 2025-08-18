# AgentTest

LangChainを用いたエージェントの実装プロジェクト

## セットアップ

```bash
# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
cp .env.example .env
# .envファイルを編集してAPIキーを設定
```

## 使用方法

```bash
python main.py
```

## プロジェクト構造

- `main.py` - メインのエージェント実行ファイル
- `agent/` - エージェントの実装
- `tools/` - カスタムツールの実装
- `config/` - 設定ファイル

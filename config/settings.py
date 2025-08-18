"""
アプリケーション設定
"""
import os
from typing import Dict, Any

class Settings:
    """アプリケーション設定クラス"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        
        self.default_model = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
        self.temperature = float(os.getenv("TEMPERATURE", "0"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1000"))
        
        self.max_iterations = int(os.getenv("MAX_ITERATIONS", "10"))
        self.verbose = os.getenv("VERBOSE", "true").lower() == "true"
    
    def get_llm_config(self) -> Dict[str, Any]:
        """LLM設定を取得"""
        return {
            "model": self.default_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "api_key": self.openai_api_key
        }
    
    def get_agent_config(self) -> Dict[str, Any]:
        """エージェント設定を取得"""
        return {
            "max_iterations": self.max_iterations,
            "verbose": self.verbose
        }
    
    def validate(self) -> bool:
        """設定の妥当性をチェック"""
        if not self.openai_api_key:
            print("警告: OPENAI_API_KEYが設定されていません")
            return False
        return True

settings = Settings()

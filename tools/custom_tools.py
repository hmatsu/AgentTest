"""
カスタムツールの実装例
"""
from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import requests
import json

class CalculatorInput(BaseModel):
    """計算機ツールの入力スキーマ"""
    expression: str = Field(description="計算する数式（例: 2+2, 10*5）")

class CalculatorTool(BaseTool):
    """シンプルな計算機ツール"""
    name = "calculator"
    description = "数学的な計算を実行します。基本的な算術演算（+, -, *, /）をサポートします。"
    args_schema: Type[BaseModel] = CalculatorInput
    
    def _run(self, expression: str) -> str:
        """計算を実行"""
        try:
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return "エラー: 許可されていない文字が含まれています"
            
            result = eval(expression)
            return f"計算結果: {expression} = {result}"
        except Exception as e:
            return f"計算エラー: {str(e)}"
    
    async def _arun(self, expression: str) -> str:
        """非同期実行（同期版を呼び出し）"""
        return self._run(expression)

class WeatherInput(BaseModel):
    """天気ツールの入力スキーマ"""
    city: str = Field(description="天気を調べる都市名")

class WeatherTool(BaseTool):
    """天気情報取得ツール（デモ用）"""
    name = "weather"
    description = "指定された都市の現在の天気情報を取得します。"
    args_schema: Type[BaseModel] = WeatherInput
    
    def _run(self, city: str) -> str:
        """天気情報を取得（デモ実装）"""
        weather_data = {
            "東京": "晴れ、気温25度",
            "大阪": "曇り、気温23度",
            "札幌": "雨、気温18度",
            "福岡": "晴れ、気温27度"
        }
        
        result = weather_data.get(city, f"{city}の天気情報は現在利用できません")
        return f"{city}の天気: {result}"
    
    async def _arun(self, city: str) -> str:
        """非同期実行（同期版を呼び出し）"""
        return self._run(city)

def get_custom_tools():
    """カスタムツールのリストを返す"""
    return [
        CalculatorTool(),
        WeatherTool(),
    ]

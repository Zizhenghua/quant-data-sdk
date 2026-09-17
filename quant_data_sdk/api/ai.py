"""
AI 接口
"""

from typing import Dict, Any


class AIAPI:
    """
    AI 代码生成

    用自然语言描述回测需求，DeepSeek 生成对应的 Python / Java 代码。

    示例：
        client = QuantDataClient(api_key="your_key")

        result = client.ai.generate_code(
            prompt="我想查看茅台23年到25年的布林带回测情况",
            language="python"
        )
        print(result["raw"])
    """

    def __init__(self, client):
        self._client = client

    # ============================================================
    # 通用方法
    # ============================================================

    def generate_code(
        self,
        prompt: str,
        language: str = "python",
    ) -> Dict[str, Any]:
        """
        生成量化策略代码

        :param prompt: 自然语言描述，如 "我想查看茅台23年到25年的布林带回测情况"
        :param language: "python" 或 "java"，默认 python
        :return: {"language": "python", "raw": "```python\\n...\\n```", "remaining": 29}
        """
        if not prompt or not prompt.strip():
            raise ValueError("prompt 不能为空")
        if len(prompt) > 2000:
            raise ValueError("prompt 长度不能超过 2000 字符")
        if language.lower() not in ("python", "java"):
            raise ValueError("language 只支持 python 或 java")

        return self._client.post(
            "/ai/generate-code",
            json={"prompt": prompt, "language": language.lower()},
        )

    def health(self) -> Dict[str, Any]:
        """检查 AI 服务是否可用"""
        return self._client.get("/ai/health")

    # ============================================================
    # 快捷方法
    # ============================================================

    def generate_bollinger(
        self,
        code: str,
        start_date: str,
        end_date: str,
        language: str = "python",
    ) -> Dict[str, Any]:
        """生成布林带回测代码"""
        prompt = (
            f"我想查看股票 {code} 从 {start_date} 到 {end_date} 的"
            f"布林带策略回测情况"
        )
        return self.generate_code(prompt, language)

    def generate_ma_cross(
        self,
        code: str,
        start_date: str,
        end_date: str,
        fast: int = 5,
        slow: int = 20,
        language: str = "python",
    ) -> Dict[str, Any]:
        """生成双均线金叉回测代码"""
        prompt = (
            f"我想查看股票 {code} 从 {start_date} 到 {end_date} 的"
            f"{fast}日均线和{slow}日均线金叉策略回测情况"
        )
        return self.generate_code(prompt, language)

    def generate_rsi(
        self,
        code: str,
        start_date: str,
        end_date: str,
        oversold: int = 30,
        overbought: int = 70,
        language: str = "python",
    ) -> Dict[str, Any]:
        """生成 RSI 超买超卖回测代码"""
        prompt = (
            f"我想查看股票 {code} 从 {start_date} 到 {end_date} 的"
            f"RSI 策略回测情况，RSI 低于 {oversold} 买入，高于 {overbought} 卖出"
        )
        return self.generate_code(prompt, language)

    def generate_macd(
        self,
        code: str,
        start_date: str,
        end_date: str,
        language: str = "python",
    ) -> Dict[str, Any]:
        """生成 MACD 金叉回测代码"""
        prompt = (
            f"我想查看股票 {code} 从 {start_date} 到 {end_date} 的"
            f"MACD 金叉策略回测情况"
        )
        return self.generate_code(prompt, language)

    def generate_kdj(
        self,
        code: str,
        start_date: str,
        end_date: str,
        language: str = "python",
    ) -> Dict[str, Any]:
        """生成 KDJ 金叉回测代码"""
        prompt = (
            f"我想查看股票 {code} 从 {start_date} 到 {end_date} 的"
            f"KDJ 金叉策略回测情况"
        )
        return self.generate_code(prompt, language)

    def generate_volume_breakout(
        self,
        code: str,
        start_date: str,
        end_date: str,
        language: str = "python",
    ) -> Dict[str, Any]:
        """生成放量突破回测代码"""
        prompt = (
            f"我想查看股票 {code} 从 {start_date} 到 {end_date} 的"
            f"放量突破策略回测情况"
        )
        return self.generate_code(prompt, language)

    # ============================================================
    # 工具方法
    # ============================================================

    @staticmethod
    def extract_code(raw: str, language: str = "python") -> str:
        """
        从 DeepSeek 返回的 markdown 里提取纯代码

        :param raw: DeepSeek 返回的原始文本
        :param language: "python" 或 "java"
        :return: 纯代码字符串
        """
        if not raw:
            return ""

        marker = f"```{language}"
        start = raw.find(marker)
        if start < 0:
            # 尝试通用 ```
            marker = "```"
            start = raw.find(marker)
            if start < 0:
                return raw.strip()

        code_start = raw.find("\n", start) + 1
        code_end = raw.find("```", code_start)
        if code_end < 0:
            return raw[code_start:].strip()

        return raw[code_start:code_end].strip()
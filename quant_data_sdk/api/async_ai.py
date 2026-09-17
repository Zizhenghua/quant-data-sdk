"""
AI 接口（异步）
"""

from typing import Dict, Any


class AsyncAIAPI:
    """AI 代码生成（异步）"""

    def __init__(self, client):
        self._client = client

    async def generate_code(
        self,
        prompt: str,
        language: str = "python",
    ) -> Dict[str, Any]:
        if not prompt or not prompt.strip():
            raise ValueError("prompt 不能为空")
        if len(prompt) > 2000:
            raise ValueError("prompt 长度不能超过 2000 字符")
        if language.lower() not in ("python", "java"):
            raise ValueError("language 只支持 python 或 java")

        return await self._client.post(
            "/ai/generate-code",
            json={"prompt": prompt, "language": language.lower()},
        )

    async def health(self) -> Dict[str, Any]:
        return await self._client.get("/ai/health")

    @staticmethod
    def extract_code(raw: str, language: str = "python") -> str:
        """从 markdown 提取纯代码"""
        if not raw:
            return ""
        marker = f"```{language}"
        start = raw.find(marker)
        if start < 0:
            start = raw.find("```")
            if start < 0:
                return raw.strip()
        code_start = raw.find("\n", start) + 1
        code_end = raw.find("```", code_start)
        if code_end < 0:
            return raw[code_start:].strip()
        return raw[code_start:code_end].strip()
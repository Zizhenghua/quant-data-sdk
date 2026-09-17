"""
AI 接口单元测试

只测参数校验和代码提取，不调真实 API。
"""

import pytest

from quant_data_sdk import QuantDataClient
from quant_data_sdk.api.ai import AIAPI


class TestAIParams:
    """AI 接口参数校验"""

    def setup_method(self):
        self.client = QuantDataClient()
        self.ai = self.client.ai

    def teardown_method(self):
        self.client.close()

    def test_empty_prompt(self):
        with pytest.raises(ValueError, match="prompt 不能为空"):
            self.ai.generate_code(prompt="")

    def test_whitespace_prompt(self):
        with pytest.raises(ValueError, match="prompt 不能为空"):
            self.ai.generate_code(prompt="   ")

    def test_prompt_too_long(self):
        with pytest.raises(ValueError, match="2000"):
            self.ai.generate_code(prompt="a" * 2001)

    def test_invalid_language(self):
        with pytest.raises(ValueError, match="python"):
            self.ai.generate_code(prompt="test", language="ruby")


class TestExtractCode:
    """代码提取"""

    def test_extract_python(self):
        raw = "```python\nprint('hello')\n```"
        code = AIAPI.extract_code(raw, "python")
        assert code == "print('hello')"

    def test_extract_java(self):
        raw = "```java\npublic class Test {}\n```"
        code = AIAPI.extract_code(raw, "java")
        assert code == "public class Test {}"

    def test_extract_no_marker(self):
        raw = "print('hello')"
        code = AIAPI.extract_code(raw, "python")
        assert code == "print('hello')"

    def test_extract_empty(self):
        assert AIAPI.extract_code("", "python") == ""

    def test_extract_multiline(self):
        raw = "```python\nline1\nline2\nline3\n```"
        code = AIAPI.extract_code(raw, "python")
        assert code == "line1\nline2\nline3"

    def test_extract_with_surrounding_text(self):
        raw = "Here is the code:\n\n```python\nprint('hi')\n```\n\nDone."
        code = AIAPI.extract_code(raw, "python")
        assert code == "print('hi')"
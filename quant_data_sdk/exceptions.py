"""
SDK 异常定义
"""


class QuantDataError(Exception):
    """SDK 基础异常"""
    pass


class AuthenticationError(QuantDataError):
    """
    401：未登录 / API Key 无效 / 已禁用 / 已过期

    提示用户去 https://zizhenghua.com/profile 检查或重新创建 Key
    """

    def __init__(self, message: str = "API Key 无效"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return (
            f"{self.message}\n\n"
            f"💡 请检查：\n"
            f"   1. API Key 是否正确（https://zizhenghua.com/profile）\n"
            f"   2. API Key 是否已被禁用或过期\n"
            f"   3. 如需重新创建，请访问 https://zizhenghua.com/profile\n"
        )


class RateLimitError(QuantDataError):
    """
    429：请求次数或行数超限

    区分匿名和带 Key，给不同的引导
    """

    def __init__(self, message: str = "请求过于频繁", is_anonymous: bool = False):
        self.message = message
        self.is_anonymous = is_anonymous
        super().__init__(message)

    def __str__(self):
        if self.is_anonymous:
            return (
                f"{self.message}\n\n"
                f"💡 你正在以【匿名】身份调用，限额较低：\n"
                f"   - 数据接口：10 次/分钟，10,000 行/分钟\n"
                f"   - AI 接口：30 次/天\n\n"
                f"   注册后可获得：\n"
                f"   - 数据接口：300 次/分钟，1000 次/天\n"
                f"   - AI 接口：100 次/天\n\n"
                f"   👉 注册：https://zizhenghua.com/register\n"
                f"   👉 创建 API Key：https://zizhenghua.com/profile\n"
            )
        return self.message


class NotFoundError(QuantDataError):
    """404：资源不存在"""
    pass


class ValidationError(QuantDataError):
    """400：参数错误"""
    pass
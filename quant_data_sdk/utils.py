"""
工具函数
"""

from typing import Any


def to_dataframe(data: Any):
    """
    把 API 返回的 dict / list 转成 pandas DataFrame

    :param data: API 返回的数据
    :return: pandas.DataFrame
    :raises ImportError: 未安装 pandas
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "需要 pandas 才能使用 DataFrame 方法。\n"
            "安装：pip install zizhenghua-quant[pandas]"
        )

    if data is None:
        return pd.DataFrame()

    # dict → 单行 DataFrame
    if isinstance(data, dict):
        return pd.DataFrame([data])

    # list of dict → 多行 DataFrame
    if isinstance(data, list):
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)

    # 其他类型，直接包一层
    return pd.DataFrame([{"value": data}])
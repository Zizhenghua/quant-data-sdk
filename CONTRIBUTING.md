# Contributing

感谢你愿意为 Quant Data SDK 做贡献！

---

## 开发环境

```bash
# 1. Clone
git clone https://github.com/Zizhenghua/quant-data-sdk.git
cd quant-data-sdk

# 2. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux / Mac
# 或
.venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -e ".[dev]"
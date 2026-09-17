@'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-09-17

### Added

- Initial release
- `QuantDataClient` 主入口
- 数据接口：`stock` / `market` / `sector` / `fin` / `factor`
- AI 接口：`ai.generate_code` + 6 个快捷方法
- 匿名支持（无需 API Key）
- 自动重试（指数退避）
- 完整的异常体系
- 代码提取工具 `ai.extract_code`
'@ | Out-File -Encoding UTF8 CHANGELOG.md
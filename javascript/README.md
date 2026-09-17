# zizhenghua-quant

Official JavaScript/TypeScript SDK for [Quant Data API](https://zizhenghua.com).

A 股行情、财务、行业、因子数据的官方 JS/TS SDK。

## Installation

```bash
npm install zizhenghua-quant
```

## Quick Start

```typescript
import { QuantDataClient } from 'zizhenghua-quant';

const client = new QuantDataClient({
  apiKey: 'your_api_key_here',  // 可选，不传则匿名
});

// 实时行情
const data = await client.stock.getRealtime('600519');
console.log(data);

// K 线
const kline = await client.stock.getKline('600519', '2024-01-01', '2024-12-31');

// 涨幅榜
const ranking = await client.stock.getRanking();

// 市场统计
const stats = await client.market.getStats();

// 行业
const sectors = await client.sector.getPerformance();

// 财务
const fin = await client.fin.getLatest('600519');

// 多因子
const factors = await client.factor.getRanking(20);
```

## AI 代码生成

```typescript
const result = await client.ai.generateCode({
  prompt: '我想查看茅台23年到25年的布林带回测情况',
  language: 'python',
});

const code = AIAPI.extractCode(result.raw, 'python');
console.log(code);
```

## Rate Limits

| User | Data API | AI API |
|------|----------|--------|
| Anonymous | 10/min, 10,000 lines/min | 30/day |
| Registered | 300/min, 600,000 lines/min, 1000/day | 100/day |

Throws `RateLimitError` when exceeded.

## Error Handling

```typescript
import {
  AuthenticationError,
  RateLimitError,
  NotFoundError,
  ValidationError,
} from 'zizhenghua-quant';

try {
  const data = await client.stock.getRealtime('600519');
} catch (e) {
  if (e instanceof AuthenticationError) {
    console.log('Auth failed');
  } else if (e instanceof RateLimitError) {
    console.log('Rate limited');
  }
}
```

## Links

- GitHub: https://github.com/Zizhenghua/quant-data-sdk
- PyPI (Python SDK): https://pypi.org/project/zizhenghua-quant/
- API Docs: https://zizhenghua.com/swagger-ui/index.html
- Discussions: https://github.com/Zizhenghua/quant-data-sdk/discussions

## License

[MIT](LICENSE)

## Disclaimer

Data is for quantitative research and backtesting only. Not investment advice.

AI-generated code is not guaranteed to be correct. Please review before use.
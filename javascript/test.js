const { QuantDataClient } = require('./dist');

async function main() {
  const client = new QuantDataClient();

  // 实时行情
  const data = await client.stock.getRealtime('600519');
  console.log('贵州茅台:', data.name, data.latestPrice);

  // 异步并发
  const codes = ['600519', '601318', '300750'];
  const results = await Promise.all(
    codes.map((c) => client.stock.getRealtime(c))
  );
  results.forEach((r) => console.log(r.name, r.latestPrice));
}

main().catch(console.error);
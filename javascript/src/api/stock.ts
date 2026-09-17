import { QuantDataClient } from '../client';

export class StockAPI {
  constructor(private client: QuantDataClient) {}

  async getRealtime(code: string) {
    return this.client.get(`/stock/realtime/${code}`);
  }

  async getKline(code: string, startDate?: string, endDate?: string) {
    const params: Record<string, string> = {};
    if (startDate) params.startDate = startDate;
    if (endDate) params.endDate = endDate;
    return this.client.get(`/stock/detail/${code}`, params);
  }

  async getBasic(code: string) {
    return this.client.get(`/stock/basic/${code}`);
  }

  async filterStocks(filters: Record<string, any>) {
    return this.client.post('/stock/filter', filters);
  }

  async getRanking(refresh: boolean = false) {
    return this.client.get('/stock/ranking', { refresh });
  }

  async getLosers(refresh: boolean = false) {
    return this.client.get('/stock/losers', { refresh });
  }

  async getTurnoverRanking(refresh: boolean = false) {
    return this.client.get('/stock/turnover-ranking', { refresh });
  }
}
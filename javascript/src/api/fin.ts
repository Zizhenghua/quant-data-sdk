import { QuantDataClient } from '../client';

export class FinAPI {
  constructor(private client: QuantDataClient) {}

  async getLatest(code: string, refresh: boolean = false) {
    return this.client.get(`/fin/latest/${code}`, { refresh });
  }

  async getHistory(code: string, n: number = 8, refresh: boolean = false) {
    return this.client.get(`/fin/history/${code}`, { n, refresh });
  }

  async getTopRoe(limit: number = 20, minRoe: number = 0, refresh: boolean = false) {
    return this.client.get('/fin/top/roe', { limit, minRoe: minRoe, refresh });
  }
}
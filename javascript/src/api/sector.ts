import { QuantDataClient } from '../client';

export class SectorAPI {
  constructor(private client: QuantDataClient) {}

  async getPerformance(refresh: boolean = false) {
    return this.client.get('/sector/performance', { refresh });
  }

  async getAmountRanking(refresh: boolean = false) {
    return this.client.get('/sector/amount-ranking', { refresh });
  }
}
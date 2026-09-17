import { QuantDataClient } from '../client';

export class FactorAPI {
  constructor(private client: QuantDataClient) {}

  async getRanking(topN: number = 20, refresh: boolean = false) {
    return this.client.get('/factor/ranking', { topN, refresh });
  }
}
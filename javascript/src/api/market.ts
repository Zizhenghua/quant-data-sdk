import { QuantDataClient } from '../client';

export class MarketAPI {
  constructor(private client: QuantDataClient) {}

  async getStats(refresh: boolean = false) {
    return this.client.get('/market/stats', { refresh });
  }

  async getHistogram(refresh: boolean = false) {
    return this.client.get('/market/histogram', { refresh });
  }

  async getConcentration(refresh: boolean = false) {
    return this.client.get('/market/concentration', { refresh });
  }

  async getVolumeSpike(refresh: boolean = false) {
    return this.client.get('/market/volume-spike', { refresh });
  }

  async getAmplitudeExtreme(refresh: boolean = false) {
    return this.client.get('/market/amplitude-extreme', { refresh });
  }
}
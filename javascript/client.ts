import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import {
  QuantDataError,
  AuthenticationError,
  RateLimitError,
  NotFoundError,
  ValidationError,
} from './exceptions';
import { StockAPI } from './api/stock';
import { MarketAPI } from './api/market';
import { SectorAPI } from './api/sector';
import { FinAPI } from './api/fin';
import { FactorAPI } from './api/factor';
import { AIAPI } from './api/ai';

const DEFAULT_BASE_URL = 'https://zizhenghua.com/api';
const USER_AGENT = 'zizhenghua-quant-js/1.0.0';

export interface ClientOptions {
  apiKey?: string;
  baseUrl?: string;
  timeout?: number;
  maxRetries?: number;
}

export class QuantDataClient {
  public apiKey?: string;
  public baseUrl: string;
  public timeout: number;
  public maxRetries: number;

  public stock: StockAPI;
  public market: MarketAPI;
  public sector: SectorAPI;
  public fin: FinAPI;
  public factor: FactorAPI;
  public ai: AIAPI;

  private http: AxiosInstance;

  constructor(options: ClientOptions = {}) {
    this.apiKey = options.apiKey;
    this.baseUrl = (options.baseUrl || DEFAULT_BASE_URL).replace(/\/$/, '');
    this.timeout = options.timeout || 30000;
    this.maxRetries = options.maxRetries || 3;

    const headers: Record<string, string> = {
      'User-Agent': USER_AGENT,
    };
    if (this.apiKey) {
      headers['X-API-Key'] = this.apiKey;
    }

    this.http = axios.create({
      baseURL: this.baseUrl,
      timeout: this.timeout,
      headers,
    });

    this.stock = new StockAPI(this);
    this.market = new MarketAPI(this);
    this.sector = new SectorAPI(this);
    this.fin = new FinAPI(this);
    this.factor = new FactorAPI(this);
    this.ai = new AIAPI(this);
  }

  async request<T = any>(
    method: 'GET' | 'POST' | 'DELETE',
    path: string,
    config: AxiosRequestConfig = {}
  ): Promise<T> {
    let lastError: any;

    for (let attempt = 0; attempt < this.maxRetries; attempt++) {
      try {
        const resp = await this.http.request({
          method,
          url: path,
          ...config,
        });

        const data = resp.data;

        if (data && typeof data === 'object' && 'success' in data) {
          if (!data.success) {
            throw new QuantDataError(data.message || 'Unknown error');
          }
          return data.data as T;
        }
        return data as T;
      } catch (err: any) {
        if (err.response) {
          const status = err.response.status;
          const msg = err.response.data?.message || '';

          if (status === 401) throw new AuthenticationError(msg);
          if (status === 404) throw new NotFoundError(msg);
          if (status === 429) throw new RateLimitError(msg, !this.apiKey);
          if (status === 400) throw new ValidationError(msg);

          throw new QuantDataError(msg || `HTTP ${status}`);
        }

        // 网络错误，重试
        lastError = err;
        if (attempt < this.maxRetries - 1) {
          const wait = Math.pow(2, attempt) * 1000;
          await new Promise((r) => setTimeout(r, wait));
        }
      }
    }

    throw new QuantDataError(`请求失败（重试 ${this.maxRetries} 次）: ${lastError}`);
  }

  async get<T = any>(path: string, params?: Record<string, any>): Promise<T> {
    return this.request<T>('GET', path, { params });
  }

  async post<T = any>(path: string, data?: any): Promise<T> {
    return this.request<T>('POST', path, { data });
  }
}
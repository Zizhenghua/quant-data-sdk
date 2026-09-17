export class QuantDataError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'QuantDataError';
  }
}

export class AuthenticationError extends QuantDataError {
  constructor(message: string = 'API Key 无效') {
    super(
      `${message}\n\n` +
      `💡 请检查：\n` +
      `   1. API Key 是否正确（https://zizhenghua.com/profile）\n` +
      `   2. API Key 是否已被禁用或过期\n`
    );
    this.name = 'AuthenticationError';
  }
}

export class RateLimitError extends QuantDataError {
  public isAnonymous: boolean;

  constructor(message: string = '请求过于频繁', isAnonymous: boolean = false) {
    super(
      isAnonymous
        ? `${message}\n\n` +
          `💡 你正在以【匿名】身份调用，限额较低：\n` +
          `   - 数据接口：10 次/分钟，10,000 行/分钟\n` +
          `   - AI 接口：30 次/天\n\n` +
          `   注册后可获得更高限额：\n` +
          `   👉 https://zizhenghua.com/register`
        : message
    );
    this.name = 'RateLimitError';
    this.isAnonymous = isAnonymous;
  }
}

export class NotFoundError extends QuantDataError {
  constructor(message: string = '资源不存在') {
    super(message);
    this.name = 'NotFoundError';
  }
}

export class ValidationError extends QuantDataError {
  constructor(message: string = '参数错误') {
    super(message);
    this.name = 'ValidationError';
  }
}
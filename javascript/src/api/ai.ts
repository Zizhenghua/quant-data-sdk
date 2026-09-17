import { QuantDataClient } from '../client';

export class AIAPI {
  constructor(private client: QuantDataClient) {}

  async generateCode(prompt: string, language: string = 'python') {
    if (!prompt || !prompt.trim()) {
      throw new Error('prompt 不能为空');
    }
    if (prompt.length > 2000) {
      throw new Error('prompt 长度不能超过 2000 字符');
    }
    if (!['python', 'java'].includes(language.toLowerCase())) {
      throw new Error('language 只支持 python 或 java');
    }
    return this.client.post('/ai/generate-code', {
      prompt,
      language: language.toLowerCase(),
    });
  }

  async health() {
    return this.client.get('/ai/health');
  }

  static extractCode(raw: string, language: string = 'python'): string {
    if (!raw) return '';
    let marker = `\`\`\`${language}`;
    let start = raw.indexOf(marker);
    if (start < 0) {
      marker = '```';
      start = raw.indexOf(marker);
      if (start < 0) return raw.trim();
    }
    const codeStart = raw.indexOf('\n', start) + 1;
    const codeEnd = raw.indexOf('```', codeStart);
    if (codeEnd < 0) return raw.slice(codeStart).trim();
    return raw.slice(codeStart, codeEnd).trim();
  }
}
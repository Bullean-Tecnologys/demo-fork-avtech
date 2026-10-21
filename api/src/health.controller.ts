import { Controller, Get } from '@nestjs/common';
import { DataService } from './data.service';

@Controller('health')
export class HealthController {
  constructor(private readonly data: DataService) { }

  @Get()
  async saude() {
    const dados = await this.data.ping();
    return { api: 'ok-atualizado', data: dados.status === 'ok' ? 'ok-atualizado' : 'indisponivel', fonte: dados.fonte };
  }
}

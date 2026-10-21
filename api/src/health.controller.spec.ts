import { HealthController } from './health.controller';
import { DataService } from './data.service';

describe('HealthController: contrato do frontend e do deploy', () => {
  it('mantém os estados de máquina e a mensagem de demonstração separados', async () => {
    const ping = jest.fn(async () => ({ status: 'ok', fonte: 'csv' }));
    const controller = new HealthController({ ping } as unknown as DataService);

    await expect(controller.saude()).resolves.toEqual({
      api: 'ok', data: 'ok', fonte: 'csv', mensagem: 'ok-atualizado',
    });
  });

  it('continua indicando falha quando o serviço de dados não responde', async () => {
    const ping = jest.fn(async () => ({ status: 'indisponivel' }));
    const controller = new HealthController({ ping } as unknown as DataService);

    await expect(controller.saude()).resolves.toMatchObject({
      api: 'ok', data: 'indisponivel',
    });
  });
});

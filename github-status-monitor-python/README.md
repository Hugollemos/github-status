# Monitor de Status do GitHub

Este é um script Python que monitora o status do GitHub e envia notificações para o Microsoft Teams quando há mudanças no status.

## Funcionalidades

- Monitoramento contínuo do status do GitHub
- Notificações em tempo real para o Microsoft Teams
- Exibição do status geral e dos componentes individuais
- Indicadores visuais com emojis para diferentes estados
- Configurável através de variáveis de ambiente

## Requisitos

- Python 3.6 ou superior
- Acesso à internet
- Webhook do Microsoft Teams configurado

## Instalação

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/github-status-monitor-python.git
cd github-status-monitor-python
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```
Edite o arquivo `.env` e adicione sua URL do webhook do Teams.

## Configuração

O arquivo `.env` deve conter as seguintes variáveis:

- `TEAMS_WEBHOOK_URL`: URL do webhook do Microsoft Teams (obrigatório)
- `GITHUB_STATUS_API_URL`: URL da API de status do GitHub (opcional, padrão: https://www.githubstatus.com/api/v2/summary.json)
- `CHECK_INTERVAL`: Intervalo de verificação em minutos (opcional, padrão: 5)

## Uso

Execute o script:
```bash
python monitor.py
```

O script irá:
1. Verificar o status atual do GitHub
2. Enviar uma notificação para o Teams com o status
3. Aguardar o intervalo configurado
4. Repetir o processo

## Notificações

As notificações no Teams incluem:
- Status geral do GitHub com emoji indicador
- Descrição do status atual
- Status individual de cada componente

## Emojis de Status

- 🟢 Operational (Operacional)
- 🟡 Degraded Performance (Desempenho Degradado)
- 🟠 Partial Outage (Parcialmente Fora do Ar)
- 🔴 Major Outage (Fora do Ar)
- 🔧 Under Maintenance (Em Manutenção)
- ⚪ Unknown (Desconhecido)

## Logs

O script mantém logs detalhados das operações, incluindo:
- Início do monitoramento
- Erros de conexão
- Sucesso no envio de notificações
- Intervalos de verificação

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes. 
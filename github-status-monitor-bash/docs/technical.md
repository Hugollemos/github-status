# GitHub Status Monitor (Bash) - Documentação Técnica

## Visão Geral
O GitHub Status Monitor é um bot desenvolvido em Bash que monitora continuamente o status da API do GitHub. O bot verifica periodicamente o endpoint de status do GitHub e registra as informações sobre o estado atual dos serviços, alertando apenas quando encontra serviços com problemas.

## Arquitetura

### Estrutura do Projeto
```
github-status-monitor-bash/
├── src/
│   └── monitor.sh         # Script principal do bot
├── docs/                 # Documentação
│   └── technical.md      # Esta documentação
└── Dockerfile           # Configuração do container
```

### Componentes Principais

1. **Função log()**
   - Responsável por registrar mensagens de log
   - Adiciona timestamp e nível de log
   - Salva logs em arquivo e exibe no console

2. **Função is_service_down()**
   - Verifica se o serviço está fora do ar
   - Analisa indicadores e descrições para detectar problemas
   - Retorna verdadeiro se o serviço estiver com problemas

3. **Função check_github_status()**
   - Responsável por fazer requisições HTTP para a API do GitHub Status
   - Extrai informações do JSON usando grep e sed
   - Trata erros e falhas de forma adequada
   - Controla o estado do serviço para evitar alertas repetidos

4. **Função cleanup()**
   - Gerencia o encerramento gracioso do script
   - Captura sinais de interrupção (SIGINT, SIGTERM)
   - Registra mensagem de encerramento

### API do GitHub Status
- Endpoint: `https://www.githubstatus.com/api/v2/summary.json`
- Método: GET
- Resposta: JSON com informações sobre o status atual do GitHub

## Configuração e Execução

### Pré-requisitos
- Bash 4.0 ou superior
- curl (para requisições HTTP)
- Docker (opcional, para execução em container)

### Execução Local
1. Clone o repositório
2. Torne o script executável:
   ```bash
   chmod +x src/monitor.sh
   ```
3. Execute o bot:
   ```bash
   ./src/monitor.sh
   ```

### Execução com Docker
1. Construa a imagem:
   ```bash
   docker build -t github-status-monitor-bash .
   ```
2. Execute o container:
   ```bash
   docker run -d github-status-monitor-bash
   ```

## Monitoramento e Logs
- O bot verifica o status a cada 5 minutos
- Logs incluem:
  - Alertas quando o GitHub está com problemas
  - Notificações quando o serviço volta ao normal
  - Timestamp da última atualização
- Formato de log: `YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE`
- Logs são salvos em `/var/log/github-status-monitor.log`

## Detecção de Problemas
- O bot identifica problemas através de:
  - Indicadores de status: "critical", "major", "minor"
  - Palavras-chave na descrição: "outage", "degraded"
- Alertas são gerados apenas quando:
  - Um problema é detectado pela primeira vez
  - O status muda (piora ou melhora)

## Tratamento de Erros
- Verificação do código de retorno do curl
- Verificação da presença de dados extraídos do JSON
- Logs de erro detalhados com mensagens informativas
- Retry automático após falhas

## Manutenção e Escalabilidade
- Código modular e bem estruturado
- Funções bem definidas para cada responsabilidade
- Fácil de estender com novas funcionalidades
- Possibilidade de adicionar:
  - Notificações (email, Slack, etc.)
  - Métricas e monitoramento
  - Interface web
  - Banco de dados para histórico

## Segurança
- Sem necessidade de credenciais
- Comunicação via HTTPS
- Containerização para isolamento
- Tratamento de sinais para encerramento gracioso

## Limitações e Considerações
- Intervalo fixo de 5 minutos entre verificações
- Sem persistência de dados
- Sem interface de usuário
- Sem sistema de notificação externa
- Processamento de JSON limitado (usa grep e sed em vez de jq)

## Próximos Passos Sugeridos
1. Implementar sistema de notificações (email, Slack, etc.)
2. Adicionar interface web
3. Implementar persistência de dados
4. Adicionar métricas e monitoramento
5. Configurar alertas personalizados
6. Melhorar o processamento de JSON usando jq
7. Adicionar testes automatizados 
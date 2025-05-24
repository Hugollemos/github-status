# GitHub Status Monitor (Python) - Documentação Técnica

## Visão Geral
O GitHub Status Monitor é um bot desenvolvido em Python que monitora continuamente o status da API do GitHub. O bot verifica periodicamente o endpoint de status do GitHub e registra as informações sobre o estado atual dos serviços, alertando apenas quando encontra serviços com problemas. Além disso, o bot pode enviar notificações para o Microsoft Teams quando detecta mudanças no status.

## Arquitetura

### Estrutura do Projeto
```
github-status-monitor-python/
├── src/
│   └── main.py           # Script principal do bot
├── docs/                 # Documentação
│   └── technical.md      # Esta documentação
├── Dockerfile           # Configuração do container
└── requirements.txt     # Dependências Python
```

### Componentes Principais

1. **Classe GitHubStatus**
   - Representa os dados de status do GitHub
   - Método de classe `from_json` para criar instâncias a partir de dados JSON
   - Método `is_down()` para verificar se o serviço está fora do ar
   - Atributos para armazenar todas as informações relevantes do status

2. **Função check_github_status()**
   - Responsável por fazer requisições HTTP para a API do GitHub Status
   - Trata exceções e erros de forma robusta
   - Retorna um objeto GitHubStatus ou None em caso de erro

3. **Função send_teams_notification()**
   - Envia notificações para o Microsoft Teams
   - Cria um cartão adaptativo com informações sobre o status
   - Trata erros de envio de notificações

4. **Função main()**
   - Ponto de entrada do programa
   - Implementa o loop principal de monitoramento
   - Configura o logging e gerencia o ciclo de vida do bot
   - Controla o estado do serviço para evitar alertas repetidos
   - Envia notificações para o Teams quando necessário

### API do GitHub Status
- Endpoint: `https://www.githubstatus.com/api/v2/summary.json`
- Método: GET
- Resposta: JSON com informações sobre o status atual do GitHub

## Configuração e Execução

### Pré-requisitos
- Python 3.6 ou superior
- Docker (opcional, para execução em container)
- Webhook do Microsoft Teams (para notificações)

### Configuração do Webhook do Microsoft Teams
1. Abra o Microsoft Teams
2. Vá para o canal onde deseja receber as notificações
3. Clique nos três pontos (...) ao lado do nome do canal
4. Selecione "Conectores"
5. Procure por "Incoming Webhook" e clique nele
6. Clique em "Configurar"
7. Dê um nome para o webhook (ex: "GitHub Status Monitor")
8. Opcionalmente, faça upload de um ícone
9. Clique em "Criar"
10. Copie a URL do webhook gerada

### Execução Local
1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure a variável de ambiente do webhook do Teams:
   ```bash
   export TEAMS_WEBHOOK_URL="https://outlook.office.com/webhook/..."
   ```
4. Execute o bot:
   ```bash
   python src/main.py
   ```

### Execução com Docker
1. Construa a imagem:
   ```bash
   docker build -t github-status-monitor-python .
   ```
2. Execute o container com a URL do webhook:
   ```bash
   docker run -d -e TEAMS_WEBHOOK_URL="https://outlook.office.com/webhook/..." github-status-monitor-python
   ```

## Monitoramento e Logs
- O bot verifica o status a cada 5 minutos
- Logs incluem:
  - Alertas quando o GitHub está com problemas
  - Notificações quando o serviço volta ao normal
  - Timestamp da última atualização
  - Confirmação de envio de notificações para o Teams
- Formato de log: `YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE`

## Notificações do Microsoft Teams
- O bot envia notificações para o Teams quando:
  - Um problema é detectado pela primeira vez
  - O status muda (piora ou melhora)
- As notificações incluem:
  - Título do monitor
  - Status atual do GitHub
  - Descrição do status
  - Timestamp da última atualização
  - Link para a página de status do GitHub
- O cartão de notificação é colorido:
  - Vermelho para problemas
  - Verde para status normal

## Detecção de Problemas
- O bot identifica problemas através de:
  - Indicadores de status: "critical", "major", "minor"
  - Palavras-chave na descrição: "outage", "degraded"
- Alertas são gerados apenas quando:
  - Um problema é detectado pela primeira vez
  - O status muda (piora ou melhora)

## Tratamento de Erros
- Tratamento específico para diferentes tipos de exceções:
  - `requests.exceptions.RequestException`: Erros de conexão
  - `json.JSONDecodeError`: Erros de parsing JSON
  - Exceções genéricas para capturar outros erros inesperados
- Logs de erro detalhados com mensagens informativas
- Retry automático após falhas
- Tratamento de erros ao enviar notificações para o Teams

## Manutenção e Escalabilidade
- Código modular e bem estruturado
- Uso de classes para encapsulamento de dados
- Fácil de estender com novas funcionalidades
- Possibilidade de adicionar:
  - Notificações para outros serviços (Slack, Email, etc.)
  - Métricas e monitoramento
  - Interface web
  - Banco de dados para histórico

## Segurança
- Sem necessidade de credenciais para a API do GitHub
- Comunicação via HTTPS
- Containerização para isolamento
- Timeout nas requisições HTTP para evitar bloqueios
- A URL do webhook do Teams é tratada como uma variável de ambiente sensível

## Limitações e Considerações
- Intervalo fixo de 5 minutos entre verificações
- Sem persistência de dados
- Sem interface de usuário
- Dependência do webhook do Teams para notificações

## Próximos Passos Sugeridos
1. Implementar notificações para outros serviços (Slack, Email, etc.)
2. Adicionar interface web
3. Implementar persistência de dados
4. Adicionar métricas e monitoramento
5. Configurar alertas personalizados
6. Adicionar testes unitários e de integração 
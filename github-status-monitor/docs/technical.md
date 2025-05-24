# GitHub Status Monitor - Documentação Técnica

## Visão Geral
O GitHub Status Monitor é um bot desenvolvido em Go que monitora continuamente o status da API do GitHub. O bot verifica periodicamente o endpoint de status do GitHub e registra as informações sobre o estado atual dos serviços.

## Arquitetura

### Estrutura do Projeto
```
github-status-monitor/
├── cmd/
│   └── main.go           # Ponto de entrada da aplicação
├── internal/             # Código interno do projeto
├── pkg/                  # Pacotes públicos
├── docs/                 # Documentação
│   └── technical.md      # Esta documentação
├── Dockerfile           # Configuração do container
└── go.mod              # Gerenciamento de dependências
```

### Componentes Principais

1. **Monitor de Status (main.go)**
   - Responsável por fazer requisições HTTP para a API do GitHub Status
   - Processa e formata os dados recebidos
   - Registra logs do status atual

2. **Estrutura de Dados**
   - `GitHubStatus`: Struct que representa a resposta da API
   - Campos principais:
     - Page: Informações sobre a página de status
     - Status: Indicador atual e descrição do status

### API do GitHub Status
- Endpoint: `https://www.githubstatus.com/api/v2/summary.json`
- Método: GET
- Resposta: JSON com informações sobre o status atual do GitHub

## Configuração e Execução

### Pré-requisitos
- Go 1.21 ou superior
- Docker (para execução em container)

### Execução Local
1. Clone o repositório
2. Execute:
   ```bash
   go mod download
   go run cmd/main.go
   ```

### Execução com Docker
1. Construa a imagem:
   ```bash
   docker build -t github-status-monitor .
   ```
2. Execute o container:
   ```bash
   docker run -d github-status-monitor
   ```

## Monitoramento e Logs
- O bot verifica o status a cada 5 minutos
- Logs incluem:
  - Status atual do GitHub
  - Indicador de status
  - Descrição do status
  - Timestamp da última atualização

## Tratamento de Erros
- Tratamento de erros de conexão
- Tratamento de erros de parsing JSON
- Logs de erro detalhados
- Retry automático após falhas

## Manutenção e Escalabilidade
- Código modular e bem estruturado
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

## Limitações e Considerações
- Intervalo fixo de 5 minutos entre verificações
- Sem persistência de dados
- Sem interface de usuário
- Sem sistema de notificação

## Próximos Passos Sugeridos
1. Implementar sistema de notificações
2. Adicionar interface web
3. Implementar persistência de dados
4. Adicionar métricas e monitoramento
5. Configurar alertas personalizados 
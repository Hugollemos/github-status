# GitHub Status Monitor

Um bot simples e eficiente desenvolvido em Go para monitorar o status do GitHub em tempo real.

## Características

- Monitoramento contínuo do status do GitHub
- Containerização com Docker
- Logs detalhados
- Fácil de configurar e executar

## Requisitos

- Go 1.21 ou superior
- Docker (opcional, para execução em container)

## Instalação

### Execução Local

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/github-status-monitor.git
cd github-status-monitor
```

2. Instale as dependências:
```bash
go mod download
```

3. Execute o bot:
```bash
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

## Documentação

Para documentação técnica detalhada, consulte [docs/technical.md](docs/technical.md).

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter pull requests.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 
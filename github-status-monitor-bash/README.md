# GitHub Status Monitor (Bash)

Um bot simples e eficiente desenvolvido em Bash para monitorar o status do GitHub em tempo real e alertar quando encontrar serviços com problemas.

## Características

- Monitoramento contínuo do status do GitHub
- Alertas apenas quando serviços estão com problemas
- Notificação quando serviços voltam ao normal
- Containerização com Docker
- Logs detalhados e formatados
- Tratamento robusto de erros
- Encerramento gracioso com tratamento de sinais

## Requisitos

- Bash 4.0 ou superior
- curl (para requisições HTTP)
- Docker (opcional, para execução em container)

## Instalação

### Execução Local

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/github-status-monitor-bash.git
cd github-status-monitor-bash
```

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

## Documentação

Para documentação técnica detalhada, consulte [docs/technical.md](docs/technical.md).

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter pull requests.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 
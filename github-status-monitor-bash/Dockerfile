FROM alpine:latest

# Instalar curl para fazer requisições HTTP
RUN apk add --no-cache curl

# Criar diretório para logs
RUN mkdir -p /var/log

# Copiar o script
COPY src/monitor.sh /app/monitor.sh

# Tornar o script executável
RUN chmod +x /app/monitor.sh

# Definir o diretório de trabalho
WORKDIR /app

# Executar o script
CMD ["/app/monitor.sh"] 
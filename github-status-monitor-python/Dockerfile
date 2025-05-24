FROM python:3.11-slim

WORKDIR /app

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY src/ .

# Definir variável de ambiente para o webhook do Teams (opcional)
# Você pode sobrescrever isso ao executar o container
ENV TEAMS_WEBHOOK_URL=""

# Executar o bot
CMD ["python", "main.py"] 
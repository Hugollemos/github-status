#!/bin/bash

# GitHub Status Monitor
# Script para monitorar o status do GitHub

# Configurações
API_URL="https://www.githubstatus.com/api/v2/summary.json"
CHECK_INTERVAL=300  # 5 minutos em segundos
LOG_FILE="/var/log/github-status-monitor.log"

# Variáveis para controle de estado
LAST_INDICATOR=""
LAST_DESCRIPTION=""
SERVICE_DOWN_ALERTED=false

# Função para registrar logs
log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "$timestamp - $level - $message" | tee -a "$LOG_FILE"
}

# Função para verificar se o serviço está fora do ar
is_service_down() {
    local indicator="$1"
    local description="$2"
    
    # Verifica se o indicador ou a descrição indicam que o serviço está fora do ar
    if [[ "$indicator" == "critical" || "$indicator" == "major" || "$indicator" == "minor" ]]; then
        return 0  # Verdadeiro, serviço está fora do ar
    fi
    
    if [[ "$description" == *"outage"* || "$description" == *"degraded"* ]]; then
        return 0  # Verdadeiro, serviço está fora do ar
    fi
    
    return 1  # Falso, serviço está funcionando
}

# Função para verificar o status do GitHub
check_github_status() {
    log "INFO" "Verificando status do GitHub..."
    
    # Fazer a requisição para a API
    response=$(curl -s "$API_URL")
    
    # Verificar se a requisição foi bem-sucedida
    if [ $? -ne 0 ]; then
        log "ERROR" "Falha ao acessar a API do GitHub Status"
        return 1
    fi
    
    # Extrair informações do JSON usando grep e sed
    # Nota: Em um ambiente de produção, seria melhor usar jq, mas mantemos compatibilidade
    indicator=$(echo "$response" | grep -o '"indicator":"[^"]*"' | sed 's/"indicator":"//;s/"//')
    description=$(echo "$response" | grep -o '"description":"[^"]*"' | sed 's/"description":"//;s/"//')
    updated_at=$(echo "$response" | grep -o '"updated_at":"[^"]*"' | sed 's/"updated_at":"//;s/"//')
    
    # Verificar se conseguimos extrair as informações
    if [ -z "$indicator" ] || [ -z "$description" ]; then
        log "ERROR" "Falha ao extrair informações do status do GitHub"
        return 1
    fi
    
    # Verificar se o status mudou em relação ao último conhecido
    status_changed=false
    if [ "$indicator" != "$LAST_INDICATOR" ] || [ "$description" != "$LAST_DESCRIPTION" ]; then
        status_changed=true
    fi
    
    # Verificar se o serviço está fora do ar
    if is_service_down "$indicator" "$description"; then
        # Se o serviço estiver fora do ar e ainda não alertamos ou o status mudou
        if [ "$SERVICE_DOWN_ALERTED" = false ] || [ "$status_changed" = true ]; then
            log "WARNING" "ALERTA: GitHub está com problemas! Status: $indicator - $description"
            log "WARNING" "Última Atualização: $updated_at"
            SERVICE_DOWN_ALERTED=true
        fi
    else
        # Se o serviço voltou ao normal, registra a recuperação
        if [ "$SERVICE_DOWN_ALERTED" = true ] || [ "$status_changed" = true ]; then
            log "INFO" "GitHub está funcionando normalmente. Status: $indicator - $description"
            log "INFO" "Última Atualização: $updated_at"
            SERVICE_DOWN_ALERTED=false
        fi
    fi
    
    # Atualizar o último status conhecido
    LAST_INDICATOR="$indicator"
    LAST_DESCRIPTION="$description"
    
    return 0
}

# Função para limpar ao encerrar
cleanup() {
    log "INFO" "Encerrando o monitor de status do GitHub..."
    exit 0
}

# Capturar sinais de interrupção
trap cleanup SIGINT SIGTERM

# Iniciar o monitor
log "INFO" "GitHub Status Monitor Bot Iniciado"

# Loop principal
while true; do
    check_github_status
    
    # Aguardar o intervalo configurado
    sleep "$CHECK_INTERVAL"
done 
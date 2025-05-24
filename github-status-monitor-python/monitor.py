#!/usr/bin/env python3
import os
import time
import json
import logging
import requests
from dotenv import load_dotenv

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

# Configurações
TEAMS_WEBHOOK_URL = os.getenv('TEAMS_WEBHOOK_URL')
GITHUB_STATUS_API_URL = os.getenv('GITHUB_STATUS_API_URL', 'https://www.githubstatus.com/api/v2/summary.json')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 5))

def get_github_status():
    """Obtém o status atual do GitHub."""
    try:
        response = requests.get(GITHUB_STATUS_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao obter status do GitHub: {e}")
        return None

def get_status_emoji(status):
    """Retorna o emoji correspondente ao status."""
    status_emojis = {
        'operational': '🟢',
        'degraded_performance': '🟡',
        'partial_outage': '🟠',
        'major_outage': '🔴',
        'under_maintenance': '🔧',
        'unknown': '⚪'
    }
    return status_emojis.get(status.lower(), '⚪')

def send_teams_notification(status_data):
    """Envia notificação para o Microsoft Teams."""
    if not TEAMS_WEBHOOK_URL:
        logger.error("URL do webhook do Teams não configurada")
        return

    # Obtém o status geral
    overall_status = status_data.get('status', {}).get('indicator', 'unknown')
    overall_description = status_data.get('status', {}).get('description', 'Status desconhecido')
    
    # Prepara a mensagem
    message = {
        "type": "message",
        "attachments": [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "version": "1.0",
                "body": [{
                    "type": "TextBlock",
                    "size": "Large",
                    "weight": "Bolder",
                    "text": f"GitHub Status {get_status_emoji(overall_status)}"
                }, {
                    "type": "TextBlock",
                    "text": overall_description,
                    "wrap": True
                }, {
                    "type": "TextBlock",
                    "text": "Status dos Componentes:",
                    "weight": "Bolder",
                    "spacing": "Medium"
                }]
            }
        }]
    }

    # Adiciona status dos componentes
    components = status_data.get('components', [])
    for component in components:
        component_status = component.get('status', 'unknown')
        component_name = component.get('name', 'Componente desconhecido')
        message['attachments'][0]['content']['body'].append({
            "type": "TextBlock",
            "text": f"{get_status_emoji(component_status)} {component_name}",
            "wrap": True
        })

    try:
        response = requests.post(TEAMS_WEBHOOK_URL, json=message)
        response.raise_for_status()
        logger.info("Notificação enviada com sucesso")
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao enviar notificação: {e}")

def main():
    """Função principal do monitor."""
    if not TEAMS_WEBHOOK_URL:
        logger.error("URL do webhook do Teams não configurada. Configure a variável TEAMS_WEBHOOK_URL no arquivo .env")
        return

    logger.info("Iniciando monitoramento do status do GitHub")
    
    while True:
        status_data = get_github_status()
        if status_data:
            send_teams_notification(status_data)
        
        logger.info(f"Aguardando {CHECK_INTERVAL} minutos para próxima verificação...")
        time.sleep(CHECK_INTERVAL * 60)

if __name__ == "__main__":
    main() 
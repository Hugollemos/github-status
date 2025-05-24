#!/usr/bin/env python3
import json
import logging
import time
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

# Configurações
GITHUB_STATUS_URL = "https://www.githubstatus.com/api/v2/summary.json"
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")
CHECK_INTERVAL = 300  # 5 minutos em segundos

class GitHubStatus:
    def __init__(self, page_id, page_name, page_url, time_zone, updated_at, indicator, description):
        self.page_id = page_id
        self.page_name = page_name
        self.page_url = page_url
        self.time_zone = time_zone
        self.updated_at = updated_at
        self.indicator = indicator
        self.description = description

    @classmethod
    def from_json(cls, data):
        page = data.get('page', {})
        status = data.get('status', {})
        
        return cls(
            page_id=page.get('id', ''),
            page_name=page.get('name', ''),
            page_url=page.get('url', ''),
            time_zone=page.get('time_zone', ''),
            updated_at=page.get('updated_at', ''),
            indicator=status.get('indicator', ''),
            description=status.get('description', '')
        )
    
    def is_down(self):
        """
        Verifica se o status indica que o serviço está fora do ar.
        
        Returns:
            bool: True se o serviço estiver fora do ar, False caso contrário
        """
        # Verifica se o indicador ou a descrição indicam que o serviço está fora do ar
        down_indicators = ['critical', 'major', 'minor']
        return self.indicator.lower() in down_indicators or 'outage' in self.description.lower() or 'degraded' in self.description.lower()

def send_teams_notification(message):
    """Envia notificação para o Microsoft Teams."""
    if not TEAMS_WEBHOOK_URL:
        logger.error("URL do webhook do Teams não configurada")
        return

    payload = {
        "text": message
    }

    try:
        response = requests.post(TEAMS_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        logger.info("Notificação enviada com sucesso para o Teams")
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao enviar notificação para o Teams: {e}")

def get_github_status():
    """Obtém o status atual do GitHub."""
    try:
        response = requests.get(GITHUB_STATUS_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao obter status do GitHub: {e}")
        return None

def format_status_message(status_data):
    """Formata a mensagem de status para o Teams."""
    components = status_data.get("components", [])
    status_message = "## Status do GitHub\n\n"
    
    for component in components:
        name = component.get("name", "Desconhecido")
        status = component.get("status", "desconhecido")
        status_message += f"- **{name}**: {status}\n"
    
    return status_message

def main():
    """Função principal do bot."""
    logger.info("Iniciando monitoramento do status do GitHub")
    
    previous_status = None
    
    while True:
        try:
            current_status = get_github_status()
            
            if current_status:
                if previous_status is None:
                    # Primeira execução
                    previous_status = current_status
                    logger.info("Status inicial obtido")
                else:
                    # Verifica mudanças no status
                    current_components = {c["name"]: c["status"] for c in current_status.get("components", [])}
                    previous_components = {c["name"]: c["status"] for c in previous_status.get("components", [])}
                    
                    for name, status in current_components.items():
                        if name in previous_components and status != previous_components[name]:
                            message = f"## Alteração no Status do GitHub\n\n"
                            message += f"**{name}** mudou de '{previous_components[name]}' para '{status}'"
                            send_teams_notification(message)
                    
                    previous_status = current_status
                
                # Se houver serviços com problemas, envia notificação
                if any(c["status"] != "operational" for c in current_status.get("components", [])):
                    message = format_status_message(current_status)
                    send_teams_notification(message)
            
            time.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main() 
#!/bin/bash

declare -A STATUS_SERVICOS

echo "🔍 Verificando status dos serviços do GitHub..."
check_github_services() {

  RESPONSE=$(curl -s https://www.githubstatus.com/api/v2/summary.json)
  SERVICES=$(echo "$RESPONSE" | jq -c '.components[] | {id: .id, name: .name, status: .status, impact: .impact}')

  while read -r service; do
    ID=$(echo "$service" | jq -r '.id')
    NAME=$(echo "$service" | jq -r '.name')
    STATUS=$(echo "$service" | jq -r '.status')
    IMPACT=$(echo "$service" | jq -r '.impact')

    if [[ "$STATUS" == "major_outage" || "$STATUS" == "partial_outage" ]]; then
      if [[ -z "${STATUS_SERVICOS[$ID]}" ]]; then
        echo "🚨 ALERTA: Serviço fora do ar!"
        echo "🔹 Serviço: $NAME"
        echo "🔹 Impacto: $IMPACT"
        echo "🔹 ID: $ID"
        echo "--------------------------------"
        STATUS_SERVICOS[$ID]=$STATUS
      fi
    else
      if [[ -n "${STATUS_SERVICOS[$ID]}" ]]; then
        echo "✅ RECUPERAÇÃO: Serviço voltou ao normal!"
        echo "🔹 Serviço: $NAME"
        echo "🔹 ID: $ID"
        echo "--------------------------------"
        unset STATUS_SERVICOS[$ID]
      fi
    fi
  done <<<"$SERVICES"
}

while true; do
  check_github_services
  sleep 60
done

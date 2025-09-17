#!/bin/bash
SERVICE_NAME="csvconverter"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

echo "==> Removendo serviço $SERVICE_NAME..."

# Parar e desabilitar
sudo systemctl stop $SERVICE_NAME
sudo systemctl disable $SERVICE_NAME

# Remover arquivo do systemd
if [ -f "$SERVICE_FILE" ]; then
    sudo rm -f $SERVICE_FILE
fi

# Recarregar systemd
sudo systemctl daemon-reload

echo "==> Serviço $SERVICE_NAME removido!"


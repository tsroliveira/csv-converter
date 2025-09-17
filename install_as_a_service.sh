#!/bin/bash
SERVICE_NAME="csvconverter"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
APP_DIR="/var/www/csv-converter"
PYTHON_BIN="/usr/bin/python3.12"
STREAMLIT_BIN="/usr/local/bin/streamlit"

echo "==> Instalando serviço $SERVICE_NAME..."

# Criar arquivo systemd
cat <<EOF | sudo tee $SERVICE_FILE
[Unit]
Description=Streamlit App Service
After=network.target

[Service]
WorkingDirectory=$APP_DIR
ExecStart=$STREAMLIT_BIN run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always
User=root
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# Recarregar systemd e habilitar
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo "==> Serviço $SERVICE_NAME instalado e iniciado!"
echo "==> Para verificar status: sudo systemctl status $SERVICE_NAME"
echo "==> Para logs: sudo journalctl -u $SERVICE_NAME -f"


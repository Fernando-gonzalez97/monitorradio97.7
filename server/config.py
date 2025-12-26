# ===================================
# Configuración - Servidor
# Monitor Radio LG
# ===================================

import os

# ========================
# TELEGRAM BOT
# ========================
TELEGRAM_BOT_TOKEN = "7661456231:AAEJ5E169mxgVWGJhTilblt6rj20cy_sztc"
TELEGRAM_CHAT_ID = "-5265595769"

# ========================
# VIGILANCIA
# ========================
# Tiempo máximo sin recibir heartbeat antes de alertar (segundos)
# Si no llega señal en este tiempo → "Radio caída"
MAX_HEARTBEAT_TIMEOUT = 120  # 2 minutos

# Intervalo de chequeo del monitor (segundos)
MONITOR_CHECK_INTERVAL = 30

# ========================
# SERVIDOR FLASK
# ========================
# Puerto (PythonAnywhere usa 80 automáticamente)
FLASK_PORT = 5000

# Debug mode (False en producción)
FLASK_DEBUG = False

# Host (0.0.0.0 para aceptar conexiones externas)
FLASK_HOST = "0.0.0.0"

# ========================
# BASE DE DATOS SIMPLE
# ========================
# Archivo donde guardar último heartbeat
HEARTBEAT_FILE = "last_heartbeat.json"

# ========================
# LOGS
# ========================
LOG_FILE = "../logs/servidor.log"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

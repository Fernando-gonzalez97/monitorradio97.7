# ===================================
# Configuración - Servidor
# Monitor Radio 97.7
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
MAX_HEARTBEAT_TIMEOUT = 90  # 1.5 minutos (más rápido que antes)

# Intervalo de chequeo del monitor (segundos)
MONITOR_CHECK_INTERVAL = 30  # Revisar cada 30 segundos

# ========================
# SERVIDOR FLASK
# ========================
FLASK_PORT = 5000
FLASK_DEBUG = False
FLASK_HOST = "0.0.0.0"

# ========================
# ALMACENAMIENTO
# ========================
# En Render, usar /tmp que es el único directorio con escritura
HEARTBEAT_FILE = "/tmp/last_heartbeat.json"
LOG_FILE = "/tmp/servidor.log"
LOG_LEVEL = "INFO"
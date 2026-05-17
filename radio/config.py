# ===================================
# Configuración - Monitor Radio 
# PC de la Radio 
# ===================================

# ========================
# STREAM DE AUDIO
# ========================
STREAM_URL = "http://stream.lgcomunicaciones.com:8045/;stream/1"

# ID de esta radio (para identificarla en el servidor)
RADIO_ID = "radio_fm_97.7"

# ========================
# SERVIDOR EXTERNO
# ========================
# URL del servidor donde enviar heartbeats
SERVER_URL = "https://monitorradio97-7.onrender.com/heartbeat"

# ========================
# TELEGRAM (Alertas locales)
# ========================
TELEGRAM_BOT_TOKEN = "7661456231:AAEJ5E169mxgVWGJhTilblt6rj20cy_sztc"
TELEGRAM_CHAT_ID = "-5265595769"

# ========================
# DETECCIÓN DE SILENCIO
# ========================
# Umbral de silencio en dBFS (decibelios)
# Valores recomendados para Line-In físico:
# -80 = Silencio casi total
# -82 = Recomendado (señal normal ~-78 dBFS)
# -85 = Más permisivo
SILENCE_THRESH = -82  # ← Ajustado para Line-In físico
# Duración mínima de silencio antes de alertar (segundos)
MIN_SILENCE_DURATION = 45  # ← Sincronizado con el servidor (45 seg)

# ========================
# HEARTBEAT
# ========================
# Cada cuántos segundos enviar señal al servidor
HEARTBEAT_INTERVAL = 30

# ========================
# MONITOREO
# ========================
# Intervalo entre chequeos de audio (segundos)
CHECK_INTERVAL = 2

# Timeout para conexiones HTTP (segundos)
TIMEOUT = 10

# ========================
# INTERFAZ GRÁFICA
# ========================
# Título de la ventana
WINDOW_TITLE = "Monitor Radio 97.7"

# Tamaño de ventana (ancho x alto)
WINDOW_SIZE = "700x500"

# Tema: "dark" o "light"
THEME = "dark"

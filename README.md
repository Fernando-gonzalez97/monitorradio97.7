🎙️ Radio Monitor
Sistema de monitoreo automático para emisoras de radio. Detecta caídas del stream, silencios prolongados y envía alertas instantáneas vía Telegram.
📋 ¿Qué hace?

Detecta silencio en el stream de audio en tiempo real
Envía alertas a Telegram cuando hay problemas
Monitorea 24/7 el estado de la radio
Interfaz gráfica moderna y fácil de usar
Sistema de heartbeat para detectar caídas del servidor

🏗️ Arquitectura
📻 PC RADIO (Windows)           🌐 SERVIDOR EXTERNO          📱 TELEGRAM
   ├─ monitor.py              ├─ app.py (Flask API)        └─ Alertas
   ├─ Detecta audio           ├─ monitor.py (Vigilante)
   └─ Envía heartbeats        └─ Detecta timeouts
📁 Estructura del Proyecto
radio-monitor/
├── radio/              # Scripts para PC de la radio
│   ├── monitor.py     # Monitor con interfaz gráfica
│   ├── config.py      # Configuración
│   ├── instalar.bat   # Instalador automático
│   └── iniciar.bat    # Ejecutar monitor
│
├── server/            # Código del servidor externo
│   ├── app.py        # API Flask
│   ├── monitor.py    # Vigilante de heartbeats
│   ├── telegram_bot.py
│   ├── config.py
│   └── requirements.txt
│
├── docs/             # Documentación
└── logs/             # Archivos de log
🚀 Instalación
PC de la Radio (Windows)

Cloná este repositorio o descargá la carpeta radio/
Ejecutá instalar.bat (instala dependencias automáticamente)
Configurá config.py con tus credenciales
Ejecutá iniciar.bat para iniciar el monitor

Servidor Externo (PythonAnywhere)
Ver documentación completa en docs/instalacion_servidor.md
⚙️ Configuración
Radio (radio/config.py)

URL del stream de audio
URL del servidor externo
Tokens de Telegram
Umbrales de detección

Servidor (server/config.py)

Tokens de Telegram
Timeouts de heartbeat
Puerto Flask

📖 Documentación

Instalación PC Radio
Instalación Servidor
Cómo Funciona

🛠️ Tecnologías

Python 3.8+
CustomTkinter - Interfaz gráfica moderna
Flask - API del servidor
Pydub - Análisis de audio
Requests - Comunicación HTTP
Telegram Bot API - Alertas

📝 Licencia
Proyecto privado - Uso interno
👤 Autor
Desarrollado para Radio Monitor
"""
API Flask - Servidor Monitor Radio 
Recibe heartbeats de la radio y muestra estado
"""

from flask import Flask, request, jsonify, render_template
from datetime import datetime, timezone, timedelta
import threading

# Importar módulos propios
from config import *
from utils import cargar_heartbeat, guardar_heartbeat, log_evento
from monitor import monitor_conexion, resetear_alerta

app = Flask(__name__)

# Zona horaria Argentina (UTC-3)
ARGENTINA_TZ = timezone(timedelta(hours=-3))

# ========================
# Rutas de la API
# ========================

@app.route('/')
def index():
    """Página principal - Estado del servidor"""
    ultimo = cargar_heartbeat()
    
    if ultimo:
        # Convertir timestamp a hora de Argentina
        timestamp = datetime.fromtimestamp(ultimo['timestamp'], tz=ARGENTINA_TZ)
        hace = int((datetime.now(timezone.utc).timestamp() - ultimo['timestamp']))
        
        estado = {
            'online': hace < MAX_HEARTBEAT_TIMEOUT,
            'tiempo_str': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'hace': hace,
            'audio_level': ultimo.get('audio_level', 'N/A'),
            'is_silent': ultimo.get('is_silent', False),
            'radio_id': ultimo.get('radio_id', 'N/A')
        }
        
        return render_template('index.html', estado=estado)
    else:
        return render_template('esperando.html')

@app.route('/heartbeat', methods=['POST'])
def recibir_heartbeat():
    """Recibir heartbeat de la radio"""
    try:
        datos = request.get_json()
        
        if not datos:
            return jsonify({"error": "No se recibieron datos"}), 400
        
        # Validar datos requeridos
        campos_requeridos = ['radio_id', 'timestamp', 'audio_level']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({"error": f"Falta campo: {campo}"}), 400
        
        # Guardar heartbeat
        if guardar_heartbeat(datos):
            resetear_alerta()  # Resetear flag de alerta
            
            log_evento(f"✅ Heartbeat recibido | Audio: {datos['audio_level']:.1f} dBFS | "
                      f"Silencio: {datos.get('is_silent', False)}")
            
            return jsonify({
                "status": "ok",
                "mensaje": "Heartbeat recibido correctamente",
                "timestamp": datetime.now(ARGENTINA_TZ).isoformat()
            }), 200
        else:
            return jsonify({"error": "Error guardando datos"}), 500
            
    except Exception as e:
        log_evento(f"❌ Error procesando heartbeat: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def obtener_estado():
    """Obtener estado actual en JSON"""
    ultimo = cargar_heartbeat()
    
    if ultimo:
        hace = int((datetime.now(timezone.utc).timestamp() - ultimo['timestamp']))
        timestamp = datetime.fromtimestamp(ultimo['timestamp'], tz=ARGENTINA_TZ)
        
        estado = {
            "online": hace < MAX_HEARTBEAT_TIMEOUT,
            "ultimo_heartbeat": timestamp.isoformat(),
            "hace_segundos": hace,
            "audio_level": ultimo.get('audio_level'),
            "is_silent": ultimo.get('is_silent', False),
            "radio_id": ultimo.get('radio_id')
        }
    else:
        estado = {
            "online": False,
            "mensaje": "Sin datos de la radio"
        }
    
    return jsonify(estado)

@app.route('/ping', methods=['GET'])
def ping():
    """Verificar que el servidor está activo"""
    return jsonify({
        "status": "ok",
        "mensaje": "Servidor activo",
        "timestamp": datetime.now(ARGENTINA_TZ).isoformat()
    })

# ========================
# Iniciar servidor
# ========================
# Iniciar hilo FUERA del if (para que corra en Render)
log_evento("🚀 Servidor iniciado")
monitor_thread = threading.Thread(target=monitor_conexion, daemon=True)
monitor_thread.start()
log_evento("👁️ Monitor de conexión iniciado")
"""
API Flask - Servidor Monitor Radio 
Recibe heartbeats de la radio y guarda estado
"""

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from config import *

app = Flask(__name__)

# ========================
# Funciones auxiliares
# ========================

def cargar_heartbeat():
    """Cargar último heartbeat del archivo"""
    if os.path.exists(HEARTBEAT_FILE):
        try:
            with open(HEARTBEAT_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def guardar_heartbeat(datos):
    """Guardar heartbeat en archivo"""
    try:
        with open(HEARTBEAT_FILE, 'w') as f:
            json.dump(datos, f, indent=2)
        return True
    except Exception as e:
        print(f"Error guardando heartbeat: {e}")
        return False

def log_evento(mensaje):
    """Registrar evento en log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {mensaje}\n"
    
    try:
        # Crear carpeta logs si no existe
        os.makedirs("../logs", exist_ok=True)
        
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_msg)
    except Exception as e:
        print(f"Error escribiendo log: {e}")
    
    # También imprimir en consola
    print(log_msg.strip())

# ========================
# Rutas de la API
# ========================

@app.route('/')
def index():
    """Página principal - Estado del servidor"""
    ultimo = cargar_heartbeat()
    
    if ultimo:
        timestamp = datetime.fromtimestamp(ultimo['timestamp'])
        tiempo_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        hace = int((datetime.now().timestamp() - ultimo['timestamp']))
        
        html = f"""
        <html>
        <head>
            <title>Monitor Radio  - Servidor</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .card {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }}
                h1 {{ color: #333; }}
                .status {{ font-size: 24px; font-weight: bold; }}
                .online {{ color: green; }}
                .offline {{ color: red; }}
                .metric {{ 
                    display: flex; 
                    justify-content: space-between;
                    padding: 10px 0;
                    border-bottom: 1px solid #eee;
                }}
                .metric:last-child {{ border-bottom: none; }}
                .label {{ font-weight: bold; }}
            </style>
            <meta http-equiv="refresh" content="30">
        </head>
        <body>
            <div class="card">
                <h1>🎙️ Monitor Radio </h1>
                <p class="status {'online' if hace < MAX_HEARTBEAT_TIMEOUT else 'offline'}">
                    {'🟢 ONLINE' if hace < MAX_HEARTBEAT_TIMEOUT else '🔴 OFFLINE'}
                </p>
            </div>
            
            <div class="card">
                <h2>📊 Estado Actual</h2>
                <div class="metric">
                    <span class="label">Última señal:</span>
                    <span>{tiempo_str}</span>
                </div>
                <div class="metric">
                    <span class="label">Hace:</span>
                    <span>{hace} segundos</span>
                </div>
                <div class="metric">
                    <span class="label">Nivel de audio:</span>
                    <span>{ultimo.get('audio_level', 'N/A')} dBFS</span>
                </div>
                <div class="metric">
                    <span class="label">Estado audio:</span>
                    <span>{'🔇 Silencio' if ultimo.get('is_silent') else '🔊 Con audio'}</span>
                </div>
                <div class="metric">
                    <span class="label">Radio ID:</span>
                    <span>{ultimo.get('radio_id', 'N/A')}</span>
                </div>
            </div>
            
            <div class="card">
                <p style="text-align: center; color: #666;">
                    Página actualizada automáticamente cada 30 segundos
                </p>
            </div>
        </body>
        </html>
        """
        return html
    else:
        return """
        <html>
        <head>
            <title>Monitor Radio  - Servidor</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    text-align: center;
                }}
                .card {{
                    background: white;
                    padding: 40px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🎙️ Monitor Radio </h1>
                <p style="font-size: 24px; color: #999;">
                    ⏳ Esperando primera señal...
                </p>
                <p>El servidor está activo pero aún no ha recibido datos de la radio.</p>
            </div>
        </body>
        </html>
        """

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
            log_evento(f"✅ Heartbeat recibido | Audio: {datos['audio_level']:.1f} dBFS | "
                      f"Silencio: {datos.get('is_silent', False)}")
            
            return jsonify({
                "status": "ok",
                "mensaje": "Heartbeat recibido correctamente",
                "timestamp": datetime.now().isoformat()
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
        hace = int((datetime.now().timestamp() - ultimo['timestamp']))
        estado = {
            "online": hace < MAX_HEARTBEAT_TIMEOUT,
            "ultimo_heartbeat": datetime.fromtimestamp(ultimo['timestamp']).isoformat(),
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
        "timestamp": datetime.now().isoformat()
    })

# ========================
# Iniciar servidor
# ========================

if __name__ == '__main__':
    log_evento("🚀 Servidor iniciado")
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG
    )
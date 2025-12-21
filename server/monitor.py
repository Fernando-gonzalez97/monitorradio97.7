"""
Monitor del Servidor
Vigila heartbeats y envía alertas si la radio cae
"""

import json
import os
import time
from datetime import datetime
from config import *
from telegram_bot import enviar_alerta

# Estado global
ultimo_estado = None  # None, "online", "offline"

def cargar_heartbeat():
    """Cargar último heartbeat del archivo"""
    if os.path.exists(HEARTBEAT_FILE):
        try:
            with open(HEARTBEAT_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def log(mensaje):
    """Registrar en log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mensaje}")
    
    try:
        os.makedirs("../logs", exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {mensaje}\n")
    except:
        pass

def vigilar():
    """Loop principal de vigilancia"""
    global ultimo_estado
    
    log("🔍 Monitor iniciado")
    
    while True:
        try:
            ultimo = cargar_heartbeat()
            
            if ultimo:
                hace = int(time.time() - ultimo['timestamp'])
                
                # Determinar estado actual
                if hace < MAX_HEARTBEAT_TIMEOUT:
                    estado_actual = "online"
                else:
                    estado_actual = "offline"
                
                # Detectar cambio de estado
                if ultimo_estado != estado_actual:
                    if estado_actual == "offline":
                        # Radio caída
                        msg = f"🚨 ALERTA: Radio caída\n\n"
                        msg += f"Última señal: hace {hace}s\n"
                        msg += f"Nivel audio: {ultimo.get('audio_level', 'N/A')} dBFS\n"
                        msg += f"Hora: {datetime.now().strftime('%H:%M:%S')}"
                        
                        enviar_alerta(msg)
                        log(f"🔴 RADIO CAÍDA (sin señal hace {hace}s)")
                        
                    elif estado_actual == "online" and ultimo_estado == "offline":
                        # Radio restaurada
                        msg = f"✅ Radio restaurada\n\n"
                        msg += f"Señal recibida correctamente\n"
                        msg += f"Hora: {datetime.now().strftime('%H:%M:%S')}"
                        
                        enviar_alerta(msg)
                        log("🟢 RADIO RESTAURADA")
                    
                    ultimo_estado = estado_actual
                
            else:
                # Sin datos
                if ultimo_estado != "sin_datos":
                    log("⏳ Sin datos de la radio")
                    ultimo_estado = "sin_datos"
            
        except Exception as e:
            log(f"❌ Error en monitor: {str(e)}")
        
        time.sleep(MONITOR_CHECK_INTERVAL)

if __name__ == "__main__":
    vigilar()
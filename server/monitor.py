"""
Monitor de conexión del servidor
Detecta desconexiones y envía alertas
"""

import time
from datetime import datetime, timezone
from config import MAX_HEARTBEAT_TIMEOUT, MONITOR_CHECK_INTERVAL
from utils import cargar_heartbeat, log_evento
from telegram_bot import enviar_alerta

# Variable global para rastrear alertas
alerta_desconexion_enviada = False
contador_chequeos = 0

def monitor_conexion():
    """
    Monitorear conexión y enviar alertas si se desconecta
    Esta función corre en un hilo separado
    """
    global alerta_desconexion_enviada, contador_chequeos
    
    log_evento("🔍 Monitor de conexión INICIADO")
    log_evento(f"⏱️ Timeout configurado: {MAX_HEARTBEAT_TIMEOUT}s")
    log_evento(f"🔄 Intervalo de chequeo: {MONITOR_CHECK_INTERVAL}s")
    
    while True:
        time.sleep(MONITOR_CHECK_INTERVAL)
        
        contador_chequeos += 1
        
        ultimo = cargar_heartbeat()
        
        if ultimo:
            ahora = datetime.now(timezone.utc).timestamp()
            hace = int(ahora - ultimo['timestamp'])
            
            # Log cada 10 chequeos (cada 5 minutos aprox)
            if contador_chequeos % 10 == 0:
                log_evento(f"💓 Monitor activo - Último heartbeat hace {hace}s")
            
            # Si pasaron más de MAX_HEARTBEAT_TIMEOUT sin señal
            if hace > MAX_HEARTBEAT_TIMEOUT:
                if not alerta_desconexion_enviada:
                    # Enviar alerta de desconexión
                    timestamp_ultimo = datetime.fromtimestamp(ultimo['timestamp'], tz=timezone.utc)
                    tiempo_str = timestamp_ultimo.strftime("%Y-%m-%d %H:%M:%S UTC")
                    minutos = hace // 60
                    
                    mensaje = (
                        f"🔴 ALERTA: PC RADIO DESCONECTADA\n\n"
                        f"📻 Monitor Radio 97.7 FM\n"
                        f"🕐 Última señal: {tiempo_str}\n"
                        f"⏱️ Sin señal hace: {minutos} min {hace % 60} seg\n\n"
                        f"⚠️ Verificar conexión URGENTE"
                    )
                    
                    log_evento(f"🚨 DESCONEXIÓN DETECTADA - Sin señal hace {minutos} min")
                    
                    if enviar_alerta(mensaje):
                        log_evento("📤 ✅ Alerta de desconexión ENVIADA a Telegram")
                        alerta_desconexion_enviada = True
                    else:
                        log_evento("📤 ❌ ERROR: No se pudo enviar alerta a Telegram")
            else:
                # Si volvió la conexión y estaba marcada como desconectada
                if alerta_desconexion_enviada:
                    mensaje = (
                        f"✅ RECONEXIÓN EXITOSA\n\n"
                        f"📻 Monitor Radio 97.7 FM\n"
                        f"🟢 La PC volvió a responder\n"
                        f"⏱️ Estuvo offline brevemente"
                    )
                    
                    log_evento("🎉 RECONEXIÓN DETECTADA")
                    
                    if enviar_alerta(mensaje):
                        log_evento("📤 ✅ Alerta de reconexión ENVIADA")
                    
                    alerta_desconexion_enviada = False
        else:
            # No hay ningún heartbeat guardado
            if contador_chequeos % 5 == 0:  # Log cada 5 chequeos
                log_evento("⚠️ Sin datos de heartbeat - Esperando primera señal...")

def resetear_alerta():
    """Resetear flag de alerta cuando llega un heartbeat"""
    global alerta_desconexion_enviada
    
    # Si estaba desconectado, enviar mensaje de reconexión
    if alerta_desconexion_enviada:
        mensaje = (
            f"✅ RECONEXIÓN EXITOSA\n\n"
            f"📻 Monitor Radio 97.7 FM\n"
            f"🟢 La PC volvió a responder\n"
            f"⏱️ Heartbeat recibido correctamente"
        )
        
        log_evento("🎉 RECONEXIÓN por heartbeat recibido")
        
        if enviar_alerta(mensaje):
            log_evento("📤 ✅ Alerta de reconexión ENVIADA")
        
        alerta_desconexion_enviada = False
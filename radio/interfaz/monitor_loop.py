"""
Monitor Loop - Hilo de monitoreo
Captura audio, detecta silencio, envía heartbeat y alertas
"""

import threading
import time
from datetime import datetime

from config import (
    SILENCE_THRESH,
    MIN_SILENCE_DURATION,
    HEARTBEAT_INTERVAL,
    CHECK_INTERVAL
)
from audio import capturar_audio
from heartbeat import enviar_heartbeat
from telegram import enviar_alerta


class MonitorLoop:
    def __init__(self, on_db_update, on_silencio, on_restaurado, on_heartbeat, on_error):
        # Callbacks
        self.on_db_update = on_db_update
        self.on_silencio = on_silencio
        self.on_restaurado = on_restaurado
        self.on_heartbeat = on_heartbeat
        self.on_error = on_error

        # Estado interno
        self.corriendo = False
        self.hilo = None
        self.silence_start = None
        self.alerta_enviada = False
        self.errores_consecutivos = 0

        # Datos gráfica
        from collections import deque
        self.audio_data = deque([0.0] * 60, maxlen=60)

    # ========================
    # CONTROL
    # ========================
    def iniciar(self):
        if self.corriendo:
            return
        self.corriendo = True
        self.hilo = threading.Thread(target=self._loop, daemon=True)
        self.hilo.start()

    def detener(self):
        self.corriendo = False

    # ========================
    # LOOP
    # ========================
    def _loop(self):
        ultimo_heartbeat = time.time()

        while self.corriendo:
            db, es_silencio = capturar_audio()

            # Error de captura
            if db is None:
                self.errores_consecutivos += 1
                if self.errores_consecutivos <= 2:
                    self.on_error("Error capturando audio")
                time.sleep(CHECK_INTERVAL)
                continue

            self.errores_consecutivos = 0
            self.audio_data.append(db)
            self.on_db_update(db, list(self.audio_data))

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Detección de silencio
            if es_silencio:
                if self.silence_start is None:
                    self.silence_start = time.time()
                duracion = time.time() - self.silence_start
                if duracion >= MIN_SILENCE_DURATION and not self.alerta_enviada:
                    enviar_alerta(f"⚠️ ALERTA: Silencio detectado\n{now}\nDuración: {duracion:.0f}s")
                    self.on_silencio(duracion)
                    self.alerta_enviada = True
            else:
                if self.silence_start is not None:
                    self.silence_start = None
                if self.alerta_enviada:
                    enviar_alerta(f"✅ Audio restaurado\n{now}")
                    self.on_restaurado()
                    self.alerta_enviada = False

            # Heartbeat
            if time.time() - ultimo_heartbeat >= HEARTBEAT_INTERVAL:
                ok = enviar_heartbeat(db, es_silencio)
                self.on_heartbeat(ok)
                if not ok:
                    self.on_error("Error enviando heartbeat")
                ultimo_heartbeat = time.time()

            time.sleep(CHECK_INTERVAL)
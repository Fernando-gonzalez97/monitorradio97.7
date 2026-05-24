"""
Envío de heartbeat al servidor externo
"""

import requests
import time
from config import SERVER_URL, RADIO_ID


def enviar_heartbeat(audio_level, es_silencio):
    """
    Envía señal de vida al servidor.
    Returns: bool
    """
    try:
        datos = {
            "radio_id": RADIO_ID,
            "timestamp": time.time(),
            "audio_level": float(audio_level) if audio_level is not None else -999.0,
            "is_silent": bool(es_silencio) if es_silencio is not None else False,
            "status": "ok"
        }
        response = requests.post(SERVER_URL, json=datos, timeout=5)
        return response.status_code == 200

    except Exception:
        return False
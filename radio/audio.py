"""
Captura y análisis de audio desde Line-In
"""

import sounddevice as sd
import numpy as np
from config import SILENCE_THRESH

DURATION = 3
SAMPLERATE = 44100


def capturar_audio():
    """
    Captura audio desde el dispositivo predeterminado y retorna el nivel en dBFS.
    Returns: (db_level: float, es_silencio: bool) o (None, None) si hay error
    """
    try:
        recording = sd.rec(
            int(DURATION * SAMPLERATE),
            samplerate=SAMPLERATE,
            channels=1,
            dtype='float32'
        )
        sd.wait()

        volume = np.linalg.norm(recording) / len(recording)
        db_level = 20 * np.log10(volume + 1e-9)
        es_silencio = db_level < SILENCE_THRESH

        return db_level, es_silencio

    except Exception as e:
        return None, None
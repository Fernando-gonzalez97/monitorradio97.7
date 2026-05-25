"""
Panel Métricas - Panel derecho
Migrado de customtkinter a PyQt6
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout,
    QLabel, QProgressBar, QPlainTextEdit, QGridLayout
)
from PyQt6.QtCore import Qt
from datetime import datetime
from config import SILENCE_THRESH, MIN_SILENCE_DURATION, HEARTBEAT_INTERVAL
from css.colores import VERDE, NARANJA, ROJO
from css.fuentes import DB_GRANDE, NORMAL, NORMAL_BOLD, LOG, SECCION


class PanelMetricas(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel_der")
        self._crear_panel()

    # ========================
    # LAYOUT
    # ========================
    def _crear_panel(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        # Título sección
        titulo = QLabel("▪ Métricas")
        titulo.setObjectName("seccion")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # dBFS grande
        self.db_label = QLabel("-- dBFS")
        self.db_label.setObjectName("db_grande")
        self.db_label.setFont(DB_GRANDE)
        self.db_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.db_label.setStyleSheet(f"color: {VERDE};")
        layout.addWidget(self.db_label)

        # Barra de nivel
        nivel_lbl = QLabel("Nivel de señal")
        nivel_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nivel_lbl.setObjectName("info_key")
        layout.addWidget(nivel_lbl)

        self.barra_nivel = QProgressBar()
        self.barra_nivel.setObjectName("barra_nivel")
        self.barra_nivel.setRange(0, 1000)
        self.barra_nivel.setValue(0)
        self.barra_nivel.setTextVisible(False)
        self.barra_nivel.setFixedHeight(8)
        layout.addWidget(self.barra_nivel)

        layout.addSpacing(6)

        # Info frame
        info_frame = QFrame()
        info_frame.setObjectName("info_frame")
        info_layout = QGridLayout(info_frame)
        info_layout.setContentsMargins(10, 8, 10, 8)
        info_layout.setSpacing(6)

        def fila(row, icon, key, value, val_id=None):
            lbl_k = QLabel(f"{icon}  {key}")
            lbl_k.setObjectName("info_key")
            lbl_v = QLabel(value)
            lbl_v.setObjectName(val_id if val_id else "info_val")
            info_layout.addWidget(lbl_k, row, 0)
            info_layout.addWidget(lbl_v, row, 1)
            return lbl_v

        self.entrada_label  = fila(0, "🎚", "Entrada:",       "--",                   "entrada_ok")
        self.heartbeat_label= fila(1, "♥",  "Heartbeat:",     "Nunca",                "info_val")
        fila(2, "🔇", "Umbral:",        f"{SILENCE_THRESH} dBFS")
        fila(3, "⏱",  "Silencio mín:", f"{MIN_SILENCE_DURATION} s")
        fila(4, "📡", "Heartbeat c/:", f"{HEARTBEAT_INTERVAL} s")

        layout.addWidget(info_frame)
        layout.addSpacing(4)

        # Log eventos
        log_titulo = QLabel("▪ Eventos")
        log_titulo.setObjectName("seccion")
        log_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(log_titulo)

        self.log_text = QPlainTextEdit()
        self.log_text.setObjectName("log_box")
        self.log_text.setReadOnly(True)
        self.log_text.setFont(LOG)
        layout.addWidget(self.log_text)

    # ========================
    # MÉTODOS PÚBLICOS
    # ========================
    def set_db(self, db):
        self.entrada_label.setText("Line-In ✓")
        self.db_label.setText(f"{db:.1f} dBFS")

        if db < SILENCE_THRESH:
            color = ROJO
        elif db < SILENCE_THRESH + 10:
            color = NARANJA
        else:
            color = VERDE

        self.db_label.setStyleSheet(f"color: {color}; font-family: Consolas; font-size: 26px; font-weight: bold;")

        norm = max(0, min(1000, int((db + 120) / 120 * 1000)))
        self.barra_nivel.setValue(norm)

    def set_heartbeat(self, ok):
        if ok:
            hora = datetime.now().strftime("%H:%M:%S")
            self.heartbeat_label.setText(hora)
            self.heartbeat_label.setObjectName("heartbeat_ok")
            self.heartbeat_label.setStyleSheet("color: #00ff88; font-weight: bold;")
        else:
            self.heartbeat_label.setText("Error !!")
            self.heartbeat_label.setObjectName("heartbeat_error")
            self.heartbeat_label.setStyleSheet("color: #e74c3c; font-weight: bold;")

    def add_log(self, mensaje):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.appendPlainText(f"[{timestamp}] {mensaje}")
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

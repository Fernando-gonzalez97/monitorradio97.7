"""
Ventana principal - Monitor Radio 97.7
Migrado de customtkinter a PyQt6
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # radio/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))                   # radio/interfaz/

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout,
    QVBoxLayout, QHBoxLayout, QFrame,
    QLabel, QPushButton, QApplication
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont

from config import WINDOW_TITLE
from grafica import Grafica
from panel_metricas import PanelMetricas
from monitor_loop import MonitorLoop
from css.estilos import QSS_GLOBAL
from css.colores import VERDE, ROJO


class MonitorRadio(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(960, 620)
        self.resize(960, 640)
        self.setStyleSheet(QSS_GLOBAL)

        # icono logo microfono
        self.setWindowIcon(self._crear_icono())

        self._crear_layout()

        # Iniciar monitoreo automático después de 500ms
        QTimer.singleShot(500, self._iniciar_monitoreo)

    # ========================
    # ICONO LOGO MICROFONO
    # ========================
    def _crear_icono(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setFont(QFont("Segoe UI Emoji", 20))
        painter.drawText(0, 26, "🎙️")
        painter.end()
        return QIcon(pixmap)

    # ========================
    # LAYOUT
    # ========================
    def _crear_layout(self):
        central = QWidget()
        central.setObjectName("root")
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(15, 15, 15, 15)
        root_layout.setSpacing(12)

        # ---- PANEL IZQUIERDO ----
        panel_izq = QFrame()
        panel_izq.setObjectName("panel_izq")
        izq_layout = QVBoxLayout(panel_izq)
        izq_layout.setContentsMargins(12, 12, 12, 12)
        izq_layout.setSpacing(6)

        # Cabecera: ícono + título + estado
        header = QHBoxLayout()
        icono = QLabel("🎙️")
        icono.setStyleSheet("font-size: 28px;")
        header.addWidget(icono)

        titulo_col = QVBoxLayout()
        titulo_col.setSpacing(2)

        titulo_lbl = QLabel(WINDOW_TITLE)
        titulo_lbl.setObjectName("titulo")
        titulo_col.addWidget(titulo_lbl)

        self.estado_label = QLabel("🟢 En el aire")
        self.estado_label.setObjectName("estado_vivo")
        titulo_col.addWidget(self.estado_label)

        header.addLayout(titulo_col)
        header.addStretch()
        izq_layout.addLayout(header)

        # Gráfica
        self.grafica = Grafica()
        izq_layout.addWidget(self.grafica, stretch=1)

        # Botón toggle
        self.toggle_btn = QPushButton("⏸  Detener Monitoreo")
        self.toggle_btn.setObjectName("btn_detener")
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.clicked.connect(self._toggle_monitoreo)
        self.toggle_btn.setFixedHeight(42)
        izq_layout.addWidget(self.toggle_btn)

        root_layout.addWidget(panel_izq, stretch=2)

        # ---- PANEL DERECHO ----
        self.metricas = PanelMetricas()
        root_layout.addWidget(self.metricas, stretch=1)

        # Monitor loop
        self.loop = MonitorLoop(
            on_db_update=self._on_db_update,
            on_silencio=self._on_silencio,
            on_restaurado=self._on_restaurado,
            on_heartbeat=self._on_heartbeat,
            on_error=self._on_error,
        )

    # ========================
    # CALLBACKS (desde hilo)
    # ========================
    def _on_db_update(self, db, datos):
        QTimer.singleShot(0, lambda: self.grafica.actualizar(db, datos))
        QTimer.singleShot(0, lambda: self.metricas.set_db(db))

    def _on_silencio(self, duracion):
        QTimer.singleShot(0, lambda: self.metricas.add_log(f"🔴 SILENCIO DETECTADO ({duracion:.0f}s)"))

    def _on_restaurado(self):
        QTimer.singleShot(0, lambda: self.metricas.add_log("🟢 AUDIO RESTAURADO"))

    def _on_heartbeat(self, ok):
        QTimer.singleShot(0, lambda: self.metricas.set_heartbeat(ok))

    def _on_error(self, msg):
        QTimer.singleShot(0, lambda: self.metricas.add_log(f"❌ {msg}"))

    # ========================
    # CONTROL
    # ========================
    def _toggle_monitoreo(self):
        if self.loop.corriendo:
            self._detener_monitoreo()
        else:
            self._iniciar_monitoreo()

    def _iniciar_monitoreo(self):
        self.loop.iniciar()
        self.estado_label.setText("🟢 En el aire")
        self.estado_label.setStyleSheet("color: #00ff88; font-weight: bold; font-size: 13px;")
        self.toggle_btn.setText("⏸  Detener Monitoreo")
        self.toggle_btn.setStyleSheet("""
            background-color: #e74c3c; color: white; border-radius: 8px;
            padding: 10px 20px; font-size: 13px; font-weight: bold;
        """)
        self.metricas.add_log("✅ Monitoreo iniciado")

    def _detener_monitoreo(self):
        self.loop.detener()
        self.estado_label.setText("🔴 Detenido")
        self.estado_label.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 13px;")
        self.toggle_btn.setText("▶  Iniciar Monitoreo")
        self.toggle_btn.setStyleSheet("""
            background-color: #2980b9; color: white; border-radius: 8px;
            padding: 10px 20px; font-size: 13px; font-weight: bold;
        """)
        self.metricas.add_log("⛔ Monitoreo detenido")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MonitorRadio()
    window.show()
    sys.exit(app.exec())
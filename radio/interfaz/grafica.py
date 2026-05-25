"""
Grafica - Canvas de onda de audio en tiempo real
Migrado de tkinter.Canvas a PyQt6 QPainter
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRect, QPoint
from PyQt6.QtGui import (
    QPainter, QColor, QPen, QBrush, QPolygon,
    QFont, QLinearGradient, QPainterPath
)
from config import SILENCE_THRESH
from css.colores import (
    FONDO, GRILLA,
    VERDE, NARANJA, ROJO,
    BARRA_FONDO, BARRA_BORDE,
    BARRA_VERDE, BARRA_NARANJA, BARRA_ROJO,
    ESCALA_DB, TEXTO_MUTED
)


class Grafica(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_actual = -120.0
        self.datos = [-120.0] * 60
        self.setMinimumSize(300, 200)

        # Timer de refresco
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(150)

    # ========================
    # DATOS
    # ========================
    def actualizar(self, db, datos):
        self.db_actual = db
        self.datos = datos

    # ========================
    # COLOR SEGÚN NIVEL
    # ========================
    def _color_actual(self):
        if self.db_actual < SILENCE_THRESH:
            return QColor(ROJO)
        elif self.db_actual < SILENCE_THRESH + 10:
            return QColor(NARANJA)
        return QColor(VERDE)

    # ========================
    # PAINT
    # ========================
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        self._dibujar_fondo(painter, w, h)
        self._dibujar_grilla(painter, w, h)
        self._dibujar_umbral(painter, w, h)
        self._dibujar_onda(painter, w, h)
        self._dibujar_medidores(painter, w, h)
        self._dibujar_nivel(painter, w, h)

        painter.end()

    def _dibujar_fondo(self, p, w, h):
        grad = QLinearGradient(0, 0, 0, h)
        grad.setColorAt(0, QColor("#0d1117"))
        grad.setColorAt(1, QColor("#1a1a2e"))
        p.fillRect(0, 0, w, h, grad)

    def _dibujar_grilla(self, p, w, h):
        pen = QPen(QColor(GRILLA), 1)
        p.setPen(pen)
        for i in range(0, w, 40):
            p.drawLine(i, 0, i, h)
        for j in range(0, h, 30):
            p.drawLine(0, j, w, j)

    def _dibujar_umbral(self, p, w, h):
        umbral_y = int(h * 0.3)
        pen = QPen(QColor(ROJO), 1, Qt.PenStyle.DashLine)
        p.setPen(pen)
        p.drawLine(0, umbral_y, w - 60, umbral_y)

        p.setPen(QColor(ROJO))
        f = QFont("Consolas", 8)
        p.setFont(f)
        p.drawText(w - 115, umbral_y - 5, f"umbral {SILENCE_THRESH} dBFS")

    def _dibujar_onda(self, p, w, h):
        datos = self.datos
        if len(datos) < 2:
            return

        MIN_DB = -120
        MAX_DB = 0
        color = self._color_actual()
        paso = w / (len(datos) - 1)

        puntos = []
        for i, db in enumerate(datos):
            x = int(i * paso)
            norm = (db - MIN_DB) / (MAX_DB - MIN_DB)
            norm = max(0.0, min(1.0, norm))
            y = int(h - (norm * h * 0.85) - (h * 0.05))
            puntos.append((x, y))

        # Path del área rellena
        path = QPainterPath()
        path.moveTo(puntos[0][0], h)
        for x, y in puntos:
            path.lineTo(x, y)
        path.lineTo(puntos[-1][0], h)
        path.closeSubpath()

        # Gradiente de relleno
        grad = QLinearGradient(0, 0, 0, h)
        fill_color = QColor(color)
        fill_color.setAlpha(60)
        fill_color2 = QColor(color)
        fill_color2.setAlpha(10)
        grad.setColorAt(0, fill_color)
        grad.setColorAt(1, fill_color2)
        p.fillPath(path, grad)

        # Línea principal
        pen = QPen(color, 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        p.setPen(pen)
        for i in range(len(puntos) - 1):
            p.drawLine(puntos[i][0], puntos[i][1], puntos[i+1][0], puntos[i+1][1])

    def _dibujar_medidores(self, p, w, h):
        MIN_DB = -60
        MAX_DB = 0
        db = max(MIN_DB, min(MAX_DB, self.db_actual))
        norm = (db - MIN_DB) / (MAX_DB - MIN_DB)

        barra_h_total = int(h * 0.75)
        barra_y_base = int(h * 0.92)
        barra_ancho = 16
        gap = 8

        x_r = w - 18
        x_l = x_r - barra_ancho - gap

        for x in [x_l, x_r]:
            # Fondo de la barra
            p.setPen(QPen(QColor(BARRA_BORDE), 1))
            p.setBrush(QBrush(QColor(BARRA_FONDO)))
            p.drawRoundedRect(x, barra_y_base - barra_h_total, barra_ancho, barra_h_total, 2, 2)

            # Segmentos activos
            seg_h = 4
            seg_gap = 2
            barra_activa = int(barra_h_total * norm)

            s = 0
            while s < barra_h_total:
                sy_bottom = barra_y_base - s
                sy_top = sy_bottom - seg_h
                if sy_top < barra_y_base - barra_h_total:
                    break
                if barra_y_base - s > barra_y_base - barra_activa:
                    s += seg_h + seg_gap
                    continue
                pct = s / barra_h_total
                if pct > 0.85:
                    seg_color = QColor(BARRA_ROJO)
                elif pct > 0.65:
                    seg_color = QColor(BARRA_NARANJA)
                else:
                    seg_color = QColor(BARRA_VERDE)

                # Brillo en el segmento
                seg_color.setAlpha(220)
                p.setPen(Qt.PenStyle.NoPen)
                p.setBrush(QBrush(seg_color))
                p.drawRect(x + 2, sy_top, barra_ancho - 4, seg_h)
                s += seg_h + seg_gap

        # Etiquetas L / R
        p.setPen(QColor(TEXTO_MUTED))
        f = QFont("Segoe UI", 8, QFont.Weight.Bold)
        p.setFont(f)
        p.drawText(x_l + barra_ancho // 2 - 4, barra_y_base + 14, "L")
        p.drawText(x_r + barra_ancho // 2 - 4, barra_y_base + 14, "R")

        # Escala dB lateral
        p.setPen(QColor(ESCALA_DB))
        f2 = QFont("Consolas", 7)
        p.setFont(f2)
        for db_mark, label in [(-60, "-60"), (-42, "-42"), (-24, "-24"), (-12, "-12"), (-6, "-6"), (0, "0")]:
            norm_m = (db_mark - MIN_DB) / (MAX_DB - MIN_DB)
            y_mark = barra_y_base - int(barra_h_total * norm_m)
            p.drawText(x_l - 28, y_mark + 4, label)

    def _dibujar_nivel(self, p, w, h):
        color = self._color_actual()
        p.setPen(color)
        f = QFont("Consolas", 11, QFont.Weight.Bold)
        p.setFont(f)
        p.drawText(10, 22, f"{self.db_actual:.1f} dBFS")
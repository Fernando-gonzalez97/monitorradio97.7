"""
Grafica - Canvas de onda de audio en tiempo real
"""

import tkinter as tk
from config import SILENCE_THRESH
from css.colores import (
    FONDO, GRILLA,
    VERDE, NARANJA, ROJO,
    BARRA_FONDO, BARRA_BORDE,
    BARRA_VERDE, BARRA_NARANJA, BARRA_ROJO,
    ESCALA_DB, TEXTO_MUTED
)
from css.fuentes import DB_CANVAS, ESCALA, ETIQUETA_LR, UMBRAL

class Grafica(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=FONDO)

        self.db_actual = 0.0
        self.datos = [0.0] * 60

        self.canvas = tk.Canvas(
            self,
            bg=FONDO,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)

        self._actualizar_loop()

    # ========================
    # DATOS
    # ========================
    def actualizar(self, db, datos):
        self.db_actual = db
        self.datos = datos

    # ========================
    # DIBUJO
    # ========================
    def _actualizar_loop(self):
        if not self.canvas.winfo_exists():
            return
        self._dibujar()
        self.after(150, self._actualizar_loop)

    def _dibujar(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w < 10 or h < 10:
            return

        self._dibujar_grilla(w, h)
        self._dibujar_umbral(w, h)
        self._dibujar_onda(w, h)
        self._dibujar_medidores(w, h)
        self._dibujar_nivel(w, h)

    def _dibujar_grilla(self, w, h):
        for i in range(0, w, 40):
            self.canvas.create_line(i, 0, i, h, fill=GRILLA, width=1)
        for j in range(0, h, 30):
            self.canvas.create_line(0, j, w, j, fill=GRILLA, width=1)

    def _dibujar_umbral(self, w, h):
        umbral_y = h * 0.3
        self.canvas.create_line(
            0, umbral_y, w, umbral_y,
            fill=ROJO, width=1, dash=(6, 4)
        )
        self.canvas.create_text(
            w - 10, umbral_y - 8,
            text=f"umbral {SILENCE_THRESH} dBFS",
            fill=ROJO,
            font=UMBRAL,
            anchor="e"
        )

    def _dibujar_onda(self, w, h):
        datos = self.datos
        if len(datos) < 2:
            return

        MIN_DB = -120
        MAX_DB = 0
        color = self._color_actual()
        paso = w / (len(datos) - 1)
        puntos = []

        for i, db in enumerate(datos):
            x = i * paso
            norm = (db - MIN_DB) / (MAX_DB - MIN_DB)
            norm = max(0.0, min(1.0, norm))
            y = h - (norm * h * 0.85) - (h * 0.05)
            puntos.append((x, y))

        # Área rellena
        poly = []
        for x, y in puntos:
            poly.extend([x, y])
        poly.extend([puntos[-1][0], h, puntos[0][0], h])
        self.canvas.create_polygon(poly, fill=color, stipple="gray25", outline="")

        # Línea principal
        for i in range(len(puntos) - 1):
            self.canvas.create_line(
                puntos[i][0], puntos[i][1],
                puntos[i+1][0], puntos[i+1][1],
                fill=color, width=2, smooth=True
            )

    def _dibujar_medidores(self, w, h):
        MIN_DB = -60
        MAX_DB = 0
        db = max(MIN_DB, min(MAX_DB, self.db_actual))
        norm = (db - MIN_DB) / (MAX_DB - MIN_DB)

        barra_h = int(h * 0.7 * norm)
        barra_y_base = int(h * 0.9)
        barra_ancho = 14
        gap = 8

        x_r = w - 15
        x_l = x_r - barra_ancho - gap

        for x in [x_l, x_r]:
            # Fondo
            self.canvas.create_rectangle(
                x, barra_y_base - int(h * 0.7),
                x + barra_ancho, barra_y_base,
                fill=BARRA_FONDO, outline=BARRA_BORDE
            )
            # Segmentos
            seg_total = int(h * 0.7)
            seg_h = 4
            seg_gap = 2
            for s in range(0, seg_total, seg_h + seg_gap):
                sy_bottom = barra_y_base - s
                sy_top = sy_bottom - seg_h
                if sy_top < barra_y_base - barra_h:
                    break
                pct = s / seg_total
                if pct > 0.85:
                    color_seg = BARRA_ROJO
                elif pct > 0.65:
                    color_seg = BARRA_NARANJA
                else:
                    color_seg = BARRA_VERDE
                self.canvas.create_rectangle(
                    x + 1, sy_top,
                    x + barra_ancho - 1, sy_bottom,
                    fill=color_seg, outline=""
                )

        # Etiquetas L R
        self.canvas.create_text(
            x_l + barra_ancho // 2, barra_y_base + 10,
            text="L", fill=TEXTO_MUTED, font=ETIQUETA_LR
        )
        self.canvas.create_text(
            x_r + barra_ancho // 2, barra_y_base + 10,
            text="R", fill=TEXTO_MUTED, font=ETIQUETA_LR
        )

        # Escala dB
        for db_mark, label in [(-60, "-60"), (-42, "-42"), (-24, "-24"), (-12, "-12"), (-6, "-6"), (0, "0")]:
            norm_m = (db_mark - MIN_DB) / (MAX_DB - MIN_DB)
            y_mark = barra_y_base - int(h * 0.7 * norm_m)
            self.canvas.create_text(
                x_l - 6, y_mark,
                text=label, fill=ESCALA_DB,
                font=ESCALA, anchor="e"
            )

    def _dibujar_nivel(self, w, h):
        color = self._color_actual()
        self.canvas.create_text(
            10, 15,
            text=f"{self.db_actual:.1f} dBFS",
            fill=color,
            font=DB_CANVAS,
            anchor="w"
        )

    def _color_actual(self):
        if self.db_actual < SILENCE_THRESH:
            return ROJO
        elif self.db_actual < SILENCE_THRESH + 10:
            return NARANJA
        return VERDE
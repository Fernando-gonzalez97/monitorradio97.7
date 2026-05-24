"""
Panel Métricas - Panel derecho
Muestra dBFS, barra de nivel, info y log de eventos
"""

import customtkinter as ctk
from datetime import datetime
from config import SILENCE_THRESH, MIN_SILENCE_DURATION, HEARTBEAT_INTERVAL
from css.colores import VERDE, NARANJA, ROJO
from css.fuentes import SECCION, DB_GRANDE, NORMAL, NORMAL_BOLD, LOG
from css.componentes import BARRA_NIVEL

class PanelMetricas(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self._crear_panel()

    # ========================
    # LAYOUT
    # ========================
    def _crear_panel(self):
        ctk.CTkLabel(
            self,
            text="📊 Métricas",
            font=SECCION
        ).pack(pady=(15, 10))

        # Nivel dBFS grande
        self.db_label = ctk.CTkLabel(
            self,
            text="-- dBFS",
            font=DB_GRANDE,
            text_color=VERDE
        )
        self.db_label.pack(pady=10)

        # Barra de nivel
        ctk.CTkLabel(self, text="Nivel de señal", font=NORMAL).pack()
        self.barra_nivel = ctk.CTkProgressBar(self, **BARRA_NIVEL)
        self.barra_nivel.pack(pady=(5, 15))
        self.barra_nivel.set(0)

        # Info
        info_frame = ctk.CTkFrame(self)
        info_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(info_frame, text="🎚️ Entrada:", font=NORMAL).grid(
            row=0, column=0, sticky="w", padx=8, pady=4)
        self.entrada_label = ctk.CTkLabel(
            info_frame, text="--", font=NORMAL_BOLD)
        self.entrada_label.grid(row=0, column=1, sticky="w", padx=8, pady=4)

        ctk.CTkLabel(info_frame, text="💓 Heartbeat:", font=NORMAL).grid(
            row=1, column=0, sticky="w", padx=8, pady=4)
        self.heartbeat_label = ctk.CTkLabel(
            info_frame, text="Nunca", font=NORMAL_BOLD)
        self.heartbeat_label.grid(row=1, column=1, sticky="w", padx=8, pady=4)

        ctk.CTkLabel(info_frame, text="🔇 Umbral:", font=NORMAL).grid(
            row=2, column=0, sticky="w", padx=8, pady=4)
        ctk.CTkLabel(
            info_frame,
            text=f"{SILENCE_THRESH} dBFS",
            font=NORMAL_BOLD
        ).grid(row=2, column=1, sticky="w", padx=8, pady=4)

        ctk.CTkLabel(info_frame, text="⏱ Silencio mín:", font=NORMAL).grid(
            row=3, column=0, sticky="w", padx=8, pady=4)
        ctk.CTkLabel(
            info_frame,
            text=f"{MIN_SILENCE_DURATION} s",
            font=NORMAL_BOLD
        ).grid(row=3, column=1, sticky="w", padx=8, pady=4)

        ctk.CTkLabel(info_frame, text="📡 Heartbeat c/:", font=NORMAL).grid(
            row=4, column=0, sticky="w", padx=8, pady=4)
        ctk.CTkLabel(
            info_frame,
            text=f"{HEARTBEAT_INTERVAL} s",
            font=NORMAL_BOLD
        ).grid(row=4, column=1, sticky="w", padx=8, pady=4)

        # Log
        ctk.CTkLabel(
            self,
            text="📋 Eventos",
            font=SECCION
        ).pack(pady=(15, 5))

        self.log_text = ctk.CTkTextbox(self, font=LOG)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 15))

    # ========================
    # MÉTODOS PÚBLICOS
    # ========================
    def set_db(self, db):
        self.entrada_label.configure(text="Line-In ✓")
        self.db_label.configure(text=f"{db:.1f} dBFS")

        if db < SILENCE_THRESH:
            color = ROJO
        elif db < SILENCE_THRESH + 10:
            color = NARANJA
        else:
            color = VERDE

        self.db_label.configure(text_color=color)

        norm = max(0.0, min(1.0, (db + 120) / 120))
        self.barra_nivel.set(norm)

    def set_heartbeat(self, ok):
        if ok:
            hora = datetime.now().strftime("%H:%M:%S")
            self.heartbeat_label.configure(text=hora, text_color=VERDE)
        else:
            self.heartbeat_label.configure(text="Error", text_color=ROJO)

    def add_log(self, mensaje):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {mensaje}\n")
        self.log_text.see("end")
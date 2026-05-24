"""
Ventana principal - Monitor Radio 97.7
Solo layout y conexión entre clases
"""


import customtkinter as ctk
from config import THEME, WINDOW_TITLE
from grafica import Grafica
from panel_metricas import PanelMetricas
from monitor_loop import MonitorLoop
from css.componentes import BTN_DETENER, BTN_INICIAR, ESTADO_VIVO, ESTADO_DETENIDO
from css.fuentes import TITULO, SUBTITULO

class MonitorRadio(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(WINDOW_TITLE)
        self.geometry("950x620")
        ctk.set_appearance_mode(THEME)
        ctk.set_default_color_theme("blue")

        self._crear_layout()
        self.after(500, self._iniciar_monitoreo)

    # ========================
    # LAYOUT
    # ========================
    def _crear_layout(self):
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Panel izquierdo
        panel_izq = ctk.CTkFrame(self)
        panel_izq.grid(row=0, column=0, sticky="nsew", padx=(15, 8), pady=15)
        panel_izq.columnconfigure(0, weight=1)
        panel_izq.rowconfigure(2, weight=1)

        # Título
        ctk.CTkLabel(
            panel_izq,
            text="🎙️ Monitor Radio 97.7",
            font=TITULO
        ).grid(row=0, column=0, pady=(15, 2))

        # Estado
        self.estado_label = ctk.CTkLabel(
            panel_izq,
            font=SUBTITULO,
            **ESTADO_DETENIDO
        )
        self.estado_label.grid(row=1, column=0, pady=2)

        # Gráfica
        self.grafica = Grafica(panel_izq)
        self.grafica.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Botón
        self.toggle_btn = ctk.CTkButton(
            panel_izq,
            command=self._toggle_monitoreo,
            **BTN_DETENER
        )
        self.toggle_btn.grid(row=3, column=0, pady=(5, 15), padx=20, sticky="ew")

        # Panel derecho
        self.metricas = PanelMetricas(self)
        self.metricas.grid(row=0, column=1, sticky="nsew", padx=(8, 15), pady=15)

        # Monitor loop
        self.loop = MonitorLoop(
            on_db_update=self._on_db_update,
            on_silencio=self._on_silencio,
            on_restaurado=self._on_restaurado,
            on_heartbeat=self._on_heartbeat,
            on_error=self._on_error,
        )

    # ========================
    # CALLBACKS
    # ========================
    def _on_db_update(self, db, datos):
        self.after(0, lambda: self.grafica.actualizar(db, datos))
        self.after(0, lambda: self.metricas.set_db(db))

    def _on_silencio(self, duracion):
        self.after(0, lambda: self.metricas.add_log(f"🔴 SILENCIO DETECTADO ({duracion:.0f}s)"))

    def _on_restaurado(self):
        self.after(0, lambda: self.metricas.add_log("🟢 AUDIO RESTAURADO"))

    def _on_heartbeat(self, ok):
        self.after(0, lambda: self.metricas.set_heartbeat(ok))

    def _on_error(self, msg):
        self.after(0, lambda: self.metricas.add_log(f"❌ {msg}"))

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
        self.estado_label.configure(**ESTADO_VIVO)
        self.toggle_btn.configure(**BTN_DETENER)
        self.metricas.add_log("✅ Monitoreo iniciado")

    def _detener_monitoreo(self):
        self.loop.detener()
        self.estado_label.configure(**ESTADO_DETENIDO)
        self.toggle_btn.configure(**BTN_INICIAR)
        self.metricas.add_log("⛔ Monitoreo detenido")


if __name__ == "__main__":
    app = MonitorRadio()
    app.mainloop()
"""
QSS global - equivalente al css/ de customtkinter
"""

QSS_GLOBAL = """
/* ========================
   VENTANA PRINCIPAL
   ======================== */
QMainWindow, QWidget#root {
    background-color: #0d1117;
}

/* ========================
   PANELES
   ======================== */
QFrame#panel_izq, QFrame#panel_der {
    background-color: #16213e;
    border: 1px solid #0f3460;
    border-radius: 12px;
}

/* ========================
   LABELS
   ======================== */
QLabel {
    color: #e0e0e0;
    background: transparent;
}

QLabel#titulo {
    color: #ffffff;
    font-size: 18px;
    font-weight: bold;
    font-family: 'Segoe UI';
}

QLabel#estado_vivo {
    color: #00ff88;
    font-size: 13px;
    font-weight: bold;
}

QLabel#estado_detenido {
    color: #e74c3c;
    font-size: 13px;
    font-weight: bold;
}

QLabel#db_grande {
    font-family: 'Consolas';
    font-size: 28px;
    font-weight: bold;
}

QLabel#seccion {
    color: #aaaacc;
    font-size: 11px;
    font-weight: bold;
    font-family: 'Segoe UI';
    letter-spacing: 1px;
}

QLabel#info_key {
    color: #8888aa;
    font-size: 10px;
    font-family: 'Segoe UI';
}

QLabel#info_val {
    color: #e0e0e0;
    font-size: 10px;
    font-weight: bold;
    font-family: 'Segoe UI';
}

QLabel#entrada_ok {
    color: #00ff88;
    font-weight: bold;
}

QLabel#heartbeat_error {
    color: #e74c3c;
    font-weight: bold;
}

QLabel#heartbeat_ok {
    color: #00ff88;
    font-weight: bold;
}

/* ========================
   INFO FRAME INTERNO
   ======================== */
QFrame#info_frame {
    background-color: #1e2a45;
    border: 1px solid #0f3460;
    border-radius: 8px;
}

/* ========================
   LOG / TEXTBOX
   ======================== */
QPlainTextEdit#log_box {
    background-color: #0d1117;
    color: #cccccc;
    border: 1px solid #0f3460;
    border-radius: 6px;
    font-family: 'Consolas';
    font-size: 9px;
    padding: 6px;
}

/* ========================
   BARRA DE PROGRESO
   ======================== */
QProgressBar#barra_nivel {
    background-color: #111122;
    border: 1px solid #333355;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}

QProgressBar#barra_nivel::chunk {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #00cc66,
        stop:0.65 #f39c12,
        stop:1 #e74c3c
    );
    border-radius: 4px;
}

/* ========================
   BOTONES
   ======================== */
QPushButton#btn_detener {
    background-color: #e74c3c;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: bold;
    font-family: 'Segoe UI';
}
QPushButton#btn_detener:hover {
    background-color: #c0392b;
}
QPushButton#btn_detener:pressed {
    background-color: #a93226;
}

QPushButton#btn_iniciar {
    background-color: #2980b9;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: bold;
    font-family: 'Segoe UI';
}
QPushButton#btn_iniciar:hover {
    background-color: #1a6fa8;
}
QPushButton#btn_iniciar:pressed {
    background-color: #145a87;
}

/* ========================
   SCROLLBAR
   ======================== */
QScrollBar:vertical {
    background: #1a1a2e;
    width: 6px;
    border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: #0f3460;
    border-radius: 3px;
    min-height: 20px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

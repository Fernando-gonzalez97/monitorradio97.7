from PyQt6.QtGui import QFont

def _f(family, size, bold=False):
    f = QFont(family, size)
    f.setBold(bold)
    return f

# ========================
# TÍTULOS
# ========================
TITULO       = _f("Segoe UI", 18, bold=True)
SUBTITULO    = _f("Segoe UI", 13, bold=True)
SECCION      = _f("Segoe UI", 11, bold=True)

# ========================
# MÉTRICAS
# ========================
DB_GRANDE    = _f("Consolas", 26, bold=True)
DB_CANVAS    = _f("Consolas", 10, bold=True)

# ========================
# UI GENERAL
# ========================
NORMAL       = _f("Segoe UI", 10)
NORMAL_BOLD  = _f("Segoe UI", 10, bold=True)
BTN          = _f("Segoe UI", 11, bold=True)

# ========================
# LOG
# ========================
LOG          = _f("Consolas", 9)

# ========================
# CANVAS
# ========================
ESCALA       = _f("Segoe UI", 7)
ETIQUETA_LR  = _f("Segoe UI", 8, bold=True)
UMBRAL       = _f("Segoe UI", 8)

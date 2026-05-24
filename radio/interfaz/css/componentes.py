from css.colores import ROJO, ROJO_HOVER, AZUL, AZUL_HOVER
from css.fuentes import BTN

# ========================
# BOTONES
# ========================
BTN_DETENER = {
    "text"        : "⏸ Detener Monitoreo",
    "fg_color"    : ROJO,
    "hover_color" : ROJO_HOVER,
    "font"        : BTN,
    "height"      : 38
}

BTN_INICIAR = {
    "text"        : "▶ Iniciar Monitoreo",
    "fg_color"    : AZUL,
    "hover_color" : AZUL_HOVER,
    "font"        : BTN,
    "height"      : 38
}

# ========================
# LABELS ESTADO
# ========================
ESTADO_VIVO = {
    "text"       : "🟢 En el aire",
    "text_color" : "#00ff88"
}

ESTADO_DETENIDO = {
    "text"       : "🔴 Detenido",
    "text_color" : "red"
}

# ========================
# BARRA DE NIVEL
# ========================
BARRA_NIVEL = {
    "width" : 180
}
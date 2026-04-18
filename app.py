import streamlit as st
import itertools
from openpyxl import Workbook
from io import BytesIO

st.set_page_config(page_title="Calculadora de Tabla de Verdad", layout="centered")

# ===== CSS ULTRA PERSONALIZADO =====
st.markdown("""
<style>

/* Fondo general */
body {
    background-color: #f9fafb;
}

/* Contenedor */
.block-container {
    padding-top: 2rem;
}

/* Título */
h1 {
    text-align: center;
    font-weight: 700;
    color: #111827;
}

/* Subtexto */
.subtitle {
    text-align: center;
    color: #6b7280;
    margin-bottom: 20px;
}

/* Botones */
div.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    background-color: #f3f4f6;
    font-size: 16px;
    font-weight: 500;
    transition: 0.2s;
}

/* Hover botones */
div.stButton > button:hover {
    background-color: #6366f1;
    color: white;
    border: none;
}

/* Botón generar */
div.stButton > button[kind="primary"] {
    background-color: #ef4444;
    color: white;
    font-weight: bold;
    height: 60px;
}

/* Input */
.stTextInput input {
    text-align: center;
    font-size: 20px;
    border-radius: 10px;
    height: 50px;
}

/* Secciones */
.section {
    margin-top: 25px;
    font-weight: 600;
    font-size: 18px;
}

/* Caja gris */
.box {
    background-color: #f3f4f6;
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ===== ESTADO =====
if "expr" not in st.session_state:
    st.session_state.expr = ""

def add(val):
    st.session_state.expr += val

def clear():
    st.session_state.expr = ""

# ===== UI =====
st.title("🔢 Calculadora de Tabla de la Verdad")
st.markdown('<div class="subtitle">Construye tu expresión haciendo clic.</div>', unsafe_allow_html=True)

# ===== CONSTRUCTOR =====
st.markdown('<div class="section">🛠 Constructor de Expresión</div>', unsafe_allow_html=True)
st.text_input("", value=st.session_state.expr, disabled=True)

# VARIABLES
cols = st.columns(6)
for i, v in enumerate(["A","B","C","D","E","F"]):
    if cols[i].button(v):
        add(v)

# OPERADORES
cols = st.columns(6)
if cols[0].button("Y"):
    add(" and ")
if cols[1].button("O"):
    add(" or ")
if cols[2].button("NO"):
    add(" not ")
if cols[3].button("XOR"):
    add(" ^ ")
if cols[4].button("→"):
    add(" <= ")
if cols[5].button("↔"):
    add(" == ")

# PARÉNTESIS
cols = st.columns(2)
if cols[0].button("("):
    add("(")
if cols[1].button(")"):
    add(")")

# LIMPIAR
st.button("🗑 Limpiar", on_click=clear)

# ===== EVALUAR =====
def evaluar(expr, valores):
    try:
        return eval(expr, {}, valores)
    except:
        return None

# ===== GENERAR + EXPORTAR =====
if st.button("🚀 Generar Tabla y Descargar Excel", type="primary"):

    expr = st.session_state.expr

    if expr == "":
        st.warning("Construye una expresión primero")
    else:
        variables = ["A","B","C","D","E","F"]
        vars_usadas = [v for v in variables if v in expr]

        combinaciones = list(itertools.product([0,1], repeat=len(vars_usadas)))
        resultados = []

        # Crear Excel en memoria
        wb = Workbook()
        ws = wb.active
        ws.title = "Tabla de Verdad"

        headers = vars_usadas + ["Resultado"]
        ws.append(headers)

        st.markdown("### 📊 Tabla de Verdad")

        # Mostrar en pantalla + guardar
        cols = st.columns(len(vars_usadas) + 1)
        for i, v in enumerate(headers):
            cols[i].write(f"**{v}**")

        for comb in combinaciones:
            valores = dict(zip(vars_usadas, comb))
            res = evaluar(expr, valores)

            res_val = int(bool(res)) if res is not None else "Error"
            resultados.append(res_val)

            ws.append(list(comb) + [res_val])

            cols = st.columns(len(vars_usadas) + 1)
            for i, val in enumerate(comb):
                cols[i].write(val)
            cols[-1].write(res_val)

        # Guardar en memoria
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        st.download_button(
            label="📥 Descargar Excel",
            data=buffer,
            file_name="tabla_verdad.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

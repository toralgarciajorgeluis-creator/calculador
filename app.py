import streamlit as st
import itertools
from openpyxl import Workbook
from io import BytesIO

st.set_page_config(layout="centered")

# ===== CSS =====
st.markdown("""
<style>

h1 {text-align:center;}

.subtitle {
    text-align:center;
    color:#6b7280;
}

/* Botones */
div.stButton > button {
    width:100%;
    height:50px;
    border-radius:10px;
    background:#f3f4f6;
    border:1px solid #e5e7eb;
}

div.stButton > button:hover {
    background:#6366f1;
    color:white;
}

/* Botón rojo */
div.stButton > button[kind="primary"] {
    background:#ef4444;
    color:white;
    font-weight:bold;
}

/* Caja gris */
.box {
    background:#f3f4f6;
    padding:15px;
    border-radius:10px;
}

/* Mensaje verde */
.success {
    background:#d1fae5;
    padding:10px;
    border-radius:8px;
    color:#065f46;
    margin-top:15px;
}

/* Tabla */
table {
    width:100%;
    border-collapse:collapse;
}
th, td {
    border:1px solid #e5e7eb;
    text-align:center;
    padding:8px;
}

</style>
""", unsafe_allow_html=True)

# ===== ESTADO =====
if "expr" not in st.session_state:
    st.session_state.expr = ""

def add(x):
    st.session_state.expr += x

def clear():
    st.session_state.expr = ""

# ===== UI =====
st.title("Calculadora de Tabla de la Verdad")
st.markdown('<div class="subtitle">Construye tu expresión haciendo clic.</div>', unsafe_allow_html=True)

# ===== CONSTRUCTOR =====
st.subheader("🛠 Constructor de Expresión")

# BOTONES
cols = st.columns(6)
for i, v in enumerate(["A","B","C","D","E","F"]):
    if cols[i].button(v):
        add(v)

cols = st.columns(6)
if cols[0].button("Y"): add(" and ")
if cols[1].button("O"): add(" or ")
if cols[2].button("NO"): add(" not ")
if cols[3].button("XOR"): add(" ^ ")
if cols[4].button("→"): add(" <= ")
if cols[5].button("↔"): add(" == ")

cols = st.columns(2)
if cols[0].button("("): add("(")
if cols[1].button(")"): add(")")

st.divider()

# ===== OPERADORES =====
st.subheader("➕ Operadores")

col1, col2 = st.columns([1,3])

if col1.button("🗑 Limpiar"):
    clear()

# Caja gris expresión
col2.markdown(f'<div class="box">{st.session_state.expr or "(vacío)"}</div>', unsafe_allow_html=True)

# ===== GENERAR =====
def evaluar(expr, valores):
    try:
        return eval(expr, {}, valores)
    except:
        return None

if st.button("🚀 Generar Tabla", type="primary"):

    expr = st.session_state.expr

    if expr == "":
        st.warning("Expresión vacía")
    else:
        variables = ["A","B","C","D","E","F"]
        vars_usadas = [v for v in variables if v in expr]

        combinaciones = list(itertools.product([0,1], repeat=len(vars_usadas)))

        resultados = []

        # Excel
        wb = Workbook()
        ws = wb.active

        headers = vars_usadas + ["Resultado"]
        ws.append(headers)

        # Mensaje verde
        st.markdown(f'<div class="success">✔ Tabla generada para {len(vars_usadas)} variable(s)</div>', unsafe_allow_html=True)

        # Tabla HTML
        html = "<table><tr>"
        for h in headers:
            html += f"<th>{h}</th>"
        html += "</tr>"

        for comb in combinaciones:
            valores = dict(zip(vars_usadas, comb))
            res = evaluar(expr, valores)
            res = int(bool(res)) if res is not None else "Error"

            ws.append(list(comb)+[res])

            html += "<tr>"
            for v in comb:
                html += f"<td>{v}</td>"
            html += f"<td>{res}</td></tr>"

        html += "</table>"

        st.markdown(html, unsafe_allow_html=True)

        # Descargar Excel
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        st.download_button(
            "📥 Descargar Excel",
            data=buffer,
            file_name="tabla_verdad.xlsx"

import streamlit as st
import itertools

st.set_page_config(page_title="Calculadora de Tabla de Verdad", layout="centered")

# ===== CSS PERSONALIZADO =====
st.markdown("""
<style>
/* Fondo */
body {
    background-color: #f5f7fa;
}

/* Título */
h1 {
    text-align: center;
    color: #1f2937;
}

/* Botones grandes */
div.stButton > button {
    width: 100%;
    height: 60px;
    font-size: 18px;
    border-radius: 12px;
    border: none;
    background-color: #e5e7eb;
    color: black;
    transition: 0.2s;
}

/* Hover */
div.stButton > button:hover {
    background-color: #6366f1;
    color: white;
}

/* Botón principal */
div.stButton > button[kind="primary"] {
    background-color: #ef4444;
    color: white;
    height: 55px;
    font-weight: bold;
}

/* Caja expresión */
.stTextInput input {
    font-size: 20px;
    text-align: center;
    border-radius: 10px;
}

/* Secciones */
.section {
    margin-top: 20px;
    font-weight: bold;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# ===== ESTADO =====
if "expr" not in st.session_state:
    st.session_state.expr = ""

def agregar(valor):
    st.session_state.expr += valor

def limpiar():
    st.session_state.expr = ""

# ===== UI =====
st.title("🧮 Calculadora de Tabla de Verdad")

st.markdown('<div class="section">Constructor de Expresión</div>', unsafe_allow_html=True)
st.text_input("", value=st.session_state.expr, key="expr_box", disabled=True)

# ===== VARIABLES =====
st.markdown('<div class="section">Variables</div>', unsafe_allow_html=True)
cols = st.columns(6)
variables = ["A", "B", "C", "D", "E", "F"]

for i, v in enumerate(variables):
    if cols[i].button(v):
        agregar(v)

# ===== OPERADORES =====
st.markdown('<div class="section">Operadores</div>', unsafe_allow_html=True)
cols = st.columns(6)

if cols[0].button("Y"):
    agregar(" and ")
if cols[1].button("O"):
    agregar(" or ")
if cols[2].button("NO"):
    agregar(" not ")
if cols[3].button("XOR"):
    agregar(" ^ ")
if cols[4].button("→"):
    agregar(" <= ")
if cols[5].button("↔"):
    agregar(" == ")

# ===== PARÉNTESIS =====
cols = st.columns(2)
if cols[0].button("("):
    agregar("(")
if cols[1].button(")"):
    agregar(")")

# ===== LIMPIAR =====
st.button("🗑 Limpiar", on_click=limpiar)

# ===== EVALUAR =====
def evaluar(expr, valores):
    try:
        return eval(expr, {}, valores)
    except:
        return None

# ===== GENERAR TABLA =====
if st.button("🚀 Generar Tabla", type="primary"):
    expr = st.session_state.expr

    if expr == "":
        st.warning("Construye una expresión primero")
    else:
        vars_usadas = [v for v in variables if v in expr]
        combinaciones = list(itertools.product([0, 1], repeat=len(vars_usadas)))

        st.markdown("### 📊 Tabla de Verdad")

        cols = st.columns(len(vars_usadas) + 1)
        for i, v in enumerate(vars_usadas):
            cols[i].write(f"**{v}**")
        cols[-1].write("**Resultado**")

        for comb in combinaciones:
            valores = dict(zip(vars_usadas, comb))
            resultado = evaluar(expr, valores)

            cols = st.columns(len(vars_usadas) + 1)
            for i, val in enumerate(comb):
                cols[i].write(val)

            cols[-1].write(int(bool(resultado)) if resultado is not None else "Error")

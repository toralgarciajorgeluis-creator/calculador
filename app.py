import streamlit as st
import itertools
import pandas as pd
import re

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="Calculadora Lógica", layout="centered")

# ---------------------------
# FUNCIONES LÓGICAS
# ---------------------------

def traducir_expresion(expr):
    expr = expr.upper().strip()

    # Normalizar operadores
    expr = expr.replace("<=", "→")
    expr = expr.replace("->", "→")

    # Reemplazos
    expr = expr.replace("Y", " and ")
    expr = expr.replace("O", " or ")
    expr = expr.replace("NO", " not ")
    expr = expr.replace("XOR", " != ")

    # Implicación
    while "→" in expr:
        izq, der = expr.split("→", 1)
        expr = f"(not ({izq}) or ({der}))"

    # Bicondicional
    while "↔" in expr:
        izq, der = expr.split("↔", 1)
        expr = f"(({izq}) and ({der})) or (not ({izq}) and not ({der}))"

    return expr


def evaluar(expr, valores):
    try:
        expr_python = traducir_expresion(expr)
        return int(eval(expr_python, {}, valores))
    except:
        return "Error"


def detectar_variables(expr):
    return sorted(set(re.findall(r'\b[A-F]\b', expr)))


def generar_tabla(expr, variables):
    combinaciones = list(itertools.product([0, 1], repeat=len(variables)))
    tabla = []

    for comb in combinaciones:
        valores = dict(zip(variables, comb))
        resultado = evaluar(expr, valores)
        tabla.append({**valores, "Resultado": resultado})

    return tabla


# ---------------------------
# ESTADO
# ---------------------------
if "expr" not in st.session_state:
    st.session_state.expr = ""

# ---------------------------
# UI
# ---------------------------

st.title("📊 Calculadora de Tabla de Verdad")
st.write("Construye tu expresión haciendo clic.")

# ---------------------------
# CONSTRUCTOR
# ---------------------------

st.subheader("🛠️ Constructor de Expresión")

cols = st.columns(6)
variables = ["A", "B", "C", "D", "E", "F"]

for i, var in enumerate(variables):
    if cols[i].button(var):
        st.session_state.expr += var

cols2 = st.columns(6)
ops = ["Y", "O", "NO", "XOR", "→", "↔"]

for i, op in enumerate(ops):
    if cols2[i].button(op):
        st.session_state.expr += f" {op} "

cols3 = st.columns(3)

if cols3[0].button("("):
    st.session_state.expr += "("

if cols3[1].button(")"):
    st.session_state.expr += ")"

if cols3[2].button("Limpiar"):
    st.session_state.expr = ""

# ---------------------------
# INPUT
# ---------------------------

expr = st.text_input("Expresión:", value=st.session_state.expr)

# ---------------------------
# BOTÓN PRINCIPAL
# ---------------------------

if st.button("🚀 Generar Tabla"):
    variables = detectar_variables(expr)

    if not variables:
        st.error("No hay variables válidas (usa A-F)")
    else:
        tabla = generar_tabla(expr, variables)

        st.success(f"Tabla generada para {len(variables)} variable(s)")

        df = pd.DataFrame(tabla)
        st.dataframe(df, use_container_width=True)

        # Descargar CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Descargar CSV",
            csv,
            "tabla_logica.csv",
            "text/csv"
        )

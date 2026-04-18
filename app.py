import streamlit as st
import itertools
import pandas as pd
import re

# ===============================
# CONFIGURACIÓN
# ===============================
st.set_page_config(
    page_title="Calculadora Lógica",
    page_icon="🧮",
    layout="centered"
)

# ===============================
# ESTILOS (CSS)
# ===============================
st.markdown("""
<style>
.result-1 {
    background-color: #d4edda;
    color: #155724;
    font-weight: bold;
    text-align: center;
}
.result-0 {
    background-color: #f8d7da;
    color: #721c24;
    font-weight: bold;
    text-align: center;
}
.expr-box {
    background-color: #f1f3f6;
    padding: 10px;
    border-radius: 8px;
    font-size: 18px;
    font-weight: bold;
}
.calc-btn {
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# FUNCIONES LÓGICAS
# ===============================
def traducir_expresion(expr):
    expr = expr.upper().strip()

    expr = expr.replace("<=", "→")
    expr = expr.replace("->", "→")

    expr = expr.replace("Y", " and ")
    expr = expr.replace("O", " or ")
    expr = expr.replace("NO", " not ")
    expr = expr.replace("XOR", " != ")

    while "→" in expr:
        izq, der = expr.split("→", 1)
        expr = f"(not ({izq}) or ({der}))"

    while "↔" in expr:
        izq, der = expr.split("↔", 1)
        expr = f"(({izq}) and ({der})) or (not ({izq}) and not ({der}))"

    return expr


def evaluar(expr, valores):
    try:
        return int(eval(traducir_expresion(expr), {}, valores))
    except:
        return None


def detectar_variables(expr):
    return sorted(set(re.findall(r'\b[A-F]\b', expr)))


def generar_tabla(expr, variables):
    combinaciones = list(itertools.product([0, 1], repeat=len(variables)))
    filas = []

    for comb in combinaciones:
        valores = dict(zip(variables, comb))
        res = evaluar(expr, valores)
        filas.append({**valores, "Resultado": res})

    return filas


# ===============================
# ESTADO
# ===============================
if "expr" not in st.session_state:
    st.session_state.expr = ""

# ===============================
# UI
# ===============================
st.title("🧮 Calculadora de Tabla de Verdad")
st.caption("Resultados visuales tipo calculadora profesional")

st.subheader("🛠️ Constructor de Expresión")

# VARIABLES
cols = st.columns(6)
for i, v in enumerate(["A", "B", "C", "D", "E", "F"]):
    if cols[i].button(v):
        st.session_state.expr += v
        st.rerun()

# OPERADORES
cols2 = st.columns(6)
for i, op in enumerate(["Y", "O", "NO", "XOR", "→", "↔"]):
    if cols2[i].button(op):
        st.session_state.expr += f" {op} "
        st.rerun()

# PARÉNTESIS Y LIMPIAR
cols3 = st.columns(3)
if cols3[0].button("("):
    st.session_state.expr += "("
    st.rerun()

if cols3[1].button(")"):
    st.session_state.expr += ")"
    st.rerun()

if cols3[2].button("🧹 Limpiar"):
    st.session_state.expr = ""
    st.rerun()

# EXPRESIÓN
st.markdown(
    f"<div class='expr-box'>{st.session_state.expr or 'Escribe tu expresión...'}</div>",
    unsafe_allow_html=True
)

# ===============================
# GENERAR TABLA
# ===============================
if st.button("🚀 Generar Tabla"):
    expr = st.session_state.expr
    variables = detectar_variables(expr)

    if not variables:
        st.error("❌ No se detectaron variables válidas (A–F)")
    else:
        tabla = generar_tabla(expr, variables)
        df = pd.DataFrame(tabla)

        st.success(f"✔ Tabla generada para {len(variables)} variable(s)")

        # Mostrar tabla con colores
        st.markdown("### 📊 Tabla de Verdad")

        for _, row in df.iterrows():
            cols = st.columns(len(variables) + 1)
            for i, v in enumerate(variables):
                cols[i].write(row[v])

            if row["Resultado"] == 1:
                cols[-1].markdown("<div class='result-1'>1</div>", unsafe_allow_html=True)
            elif row["Resultado"] == 0:
                cols[-1].markdown("<div class='result-0'>0</div>", unsafe_allow_html=True)
            else:
                cols[-1].write("Error")

        # DESCARGAR
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar CSV", csv, "tabla_logica.csv", "text/csv")

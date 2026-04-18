import streamlit as st
import itertools

st.set_page_config(page_title="Calculadora de Tabla de Verdad")

st.title("🧮 Calculadora de Tabla de Verdad")

# Inicializar expresión
if "expr" not in st.session_state:
    st.session_state.expr = ""

# Función para agregar texto
def agregar(valor):
    st.session_state.expr += valor

# Función limpiar
def limpiar():
    st.session_state.expr = ""

# Mostrar expresión
st.subheader("Constructor de Expresión")
st.text_input("Expresión:", value=st.session_state.expr, key="input_expr", disabled=True)

# Botones de variables
st.write("### Variables")
cols = st.columns(6)
variables = ["A", "B", "C", "D", "E", "F"]

for i, v in enumerate(variables):
    if cols[i].button(v):
        agregar(v)

# Botones de operadores
st.write("### Operadores")
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
    agregar(" <= ")  # A → B ≈ A <= B
if cols[5].button("↔"):
    agregar(" == ")

# Paréntesis
cols = st.columns(2)
if cols[0].button("("):
    agregar("(")
if cols[1].button(")"):
    agregar(")")

# Limpiar
st.button("🗑 Limpiar", on_click=limpiar)

# Evaluación
def evaluar(expr, valores):
    try:
        return eval(expr, {}, valores)
    except:
        return None

# Generar tabla
if st.button("🚀 Generar Tabla"):
    expr = st.session_state.expr

    if expr == "":
        st.warning("Construye una expresión primero")
    else:
        vars_usadas = [v for v in variables if v in expr]

        combinaciones = list(itertools.product([0, 1], repeat=len(vars_usadas)))

        st.write("### Tabla de Verdad")

        # Encabezado
        cols = st.columns(len(vars_usadas) + 1)
        for i, v in enumerate(vars_usadas):
            cols[i].write(f"**{v}**")
        cols[-1].write("**Resultado**")

        # Filas
        for comb in combinaciones:
            valores = dict(zip(vars_usadas, comb))
            resultado = evaluar(expr, valores)

            cols = st.columns(len(vars_usadas) + 1)
            for i, val in enumerate(comb):
                cols[i].write(val)

            if resultado is None:
                cols[-1].write("Error")
            else:
                cols[-1].write(int(bool(resultado)))

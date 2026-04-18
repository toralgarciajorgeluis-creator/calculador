import streamlit as st
import itertools

st.set_page_config(page_title="Calculadora de Tabla de Verdad")

st.title("🧮 Calculadora de Tabla de Verdad")

# Variables disponibles
variables = ["A", "B", "C", "D", "E", "F"]

expr = st.text_input("Escribe la expresión lógica (ej: A and B or not C):")

def evaluar(expr, valores):
    try:
        return eval(expr, {}, valores)
    except:
        return "Error"

if st.button("Generar Tabla"):
    if expr == "":
        st.warning("Escribe una expresión primero")
    else:
        # Detectar variables usadas
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
            cols[-1].write(int(bool(resultado)))

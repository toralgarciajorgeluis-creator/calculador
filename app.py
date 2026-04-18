# app.py
import streamlit as st
import pandas as pd
from truth_table import generar_tabla

st.title("Calculadora de Tabla de Verdad")

expr = st.text_input("Ingresa la expresión lógica (ej: A AND B OR NOT C)")

if st.button("Generar tabla"):
    if expr.strip() == "":
        st.error("Por favor ingresa una expresión.")
    else:
        try:
            variables, tabla = generar_tabla(expr)

            columnas = variables + ["Resultado"]
            df = pd.DataFrame(tabla, columns=columnas)

            st.dataframe(df)

            # Descargar CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Descargar CSV", csv, "tabla.csv", "text/csv")

        except:
            st.error("Error en la expresión lógica.")

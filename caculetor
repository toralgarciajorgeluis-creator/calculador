# app.py
import itertools
import re

def extraer_variables(expr):
    return sorted(set(re.findall(r'[A-Z]', expr)))

def generar_combinaciones(n):
    return list(itertools.product([0, 1], repeat=n))

def evaluar_expresion(expr, valores):
    # Reemplazos seguros
    expr = expr.replace("AND", "and")
    expr = expr.replace("OR", "or")
    expr = expr.replace("NOT", "not")
    expr = expr.replace("XOR", "^")

    for var, val in valores.items():
        expr = expr.replace(var, str(val))

    try:
        resultado = eval(expr)
        return int(resultado)
    except:
        return "Error"

def generar_tabla(expr):
    variables = extraer_variables(expr)
    combinaciones = generar_combinaciones(len(variables))

    tabla = []

    for comb in combinaciones:
        valores = dict(zip(variables, comb))
        resultado = evaluar_expresion(expr, valores)
        fila = list(comb) + [resultado]
        tabla.append(fila)

    return variables, tabla

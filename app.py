import itertools

def traducir_expresion(expr):
    # Normalizar entrada
    expr = expr.upper().strip()

    # Reemplazos de operadores
    expr = expr.replace("<=", "→")
    expr = expr.replace("->", "→")
    expr = expr.replace("Y", " and ")
    expr = expr.replace("O", " or ")
    expr = expr.replace("NO", " not ")
    expr = expr.replace("XOR", " ^ ")

    # Implicación: A → B = (not A) or B
    if "→" in expr:
        partes = expr.split("→")
        izquierda = partes[0].strip()
        derecha = partes[1].strip()
        expr = f"(not ({izquierda}) or ({derecha}))"

    return expr


def evaluar_expresion(expr, valores):
    try:
        expr_python = traducir_expresion(expr)
        return int(eval(expr_python, {}, valores))
    except:
        return "Error"


def generar_tabla(expr, variables):
    combinaciones = list(itertools.product([0, 1], repeat=len(variables)))
    tabla = []

    for comb in combinaciones:
        valores = dict(zip(variables, comb))
        resultado = evaluar_expresion(expr, valores)
        tabla.append({**valores, "Resultado": resultado})

    return tabla


# 🔥 EJEMPLO DE USO
expr = "A <= B"   # el usuario escribe esto
variables = ["A", "B"]

tabla = generar_tabla(expr, variables)

for fila in tabla:
    print(fila)

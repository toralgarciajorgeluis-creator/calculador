<!DOCTYPE html>
<html>
<head>
  <title>Tabla de Verdad</title>
</head>
<body>
  <h2>Calculadora de Tabla de Verdad</h2>

  <input type="text" id="expresion" placeholder="Ej: A && B || !C">
  <button onclick="generarTabla()">Calcular</button>

  <table border="1" id="tabla"></table>

  <script>
    function generarTabla() {
      let expr = document.getElementById("expresion").value;
      let variables = ["A", "B", "C"];
      let tabla = document.getElementById("tabla");
      tabla.innerHTML = "";

      // Encabezado
      let header = "<tr>";
      variables.forEach(v => header += "<th>" + v + "</th>");
      header += "<th>Resultado</th></tr>";
      tabla.innerHTML += header;

      // Combinaciones
      for (let i = 0; i < 8; i++) {
        let valores = {
          A: !!(i & 1),
          B: !!(i & 2),
          C: !!(i & 4)
        };

        let resultado = eval(
          expr.replace(/A|B|C/g, m => valores[m])
        );

        let fila = "<tr>";
        variables.forEach(v => fila += "<td>" + valores[v] + "</td>");
        fila += "<td>" + resultado + "</td></tr>";

        tabla.innerHTML += fila;
      }
    }
  </script>
</body>
</html>

from flask import Flask, render_template_string
import json
import os

app = Flask(__name__)

# Variáveis globais para repetições de flexão, abdominal, agachamento, barras
repeticoes_flexao = 0
repeticoes_abdominais = 0
repeticoes_agachamento = 0
repeticoes_barras = 0

agachamentos = 0
abdominais = 0
flexao = 0
barras = 0

# Caminho do arquivo JSON onde os contadores serão salvos
FILE_PATH = 'contadores.json'

# Função para carregar os contadores do arquivo JSON
def carregar_contadores():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            try:
                # Tenta carregar o JSON do arquivo
                contadores = json.load(file)
                # Verifica se todas as chaves necessárias existem, caso contrário, usa valores padrão
                if not all(key in contadores for key in ["repeticoes_1", "flexao", "repeticoes_2", "abdominais", "repeticoes_3", "agachamento", "repeticoes_4", "barras"]):
                    return {"repeticoes_1": 0, "flexao": 0, "repeticoes_2": 0, "abdominais": 0, "repeticoes_3": 0, "agachamento": 0, "repeticoes_4": 0, "barras": 0}
                return contadores
            except (json.JSONDecodeError, KeyError):
                # Em caso de erro ao ler ou se o arquivo for inválido
                return {"repeticoes_1": 0, "flexao": 0, "repeticoes_2": 0, "abdominais": 0, "repeticoes_3": 0, "agachamento": 0, "repeticoes_4": 0, "barras": 0}
    return {"repeticoes_1": 0, "flexao": 0, "repeticoes_2": 0, "abdominais": 0, "repeticoes_3": 0, "agachamento": 0, "repeticoes_4": 0, "barras": 0}  # Valor padrão

# Função para salvar os contadores no arquivo JSON
def salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras):
    contadores = {
        "repeticoes_1": repeticoes_1,
        "flexao": flexao,
        "repeticoes_2": repeticoes_2,
        "abdominais": abdominais,
        "repeticoes_3": repeticoes_3,
        "agachamento": agachamento,
        "repeticoes_4": repeticoes_4,
        "barras": barras
    }
    with open(FILE_PATH, 'w') as file:
        json.dump(contadores, file)

# Carregar os contadores ao iniciar o aplicativo
contadores = carregar_contadores()
repeticoes_1 = contadores["repeticoes_1"]
flexao = contadores["flexao"]
repeticoes_2 = contadores["repeticoes_2"]
abdominais = contadores["abdominais"]
repeticoes_3 = contadores["repeticoes_3"]
agachamento = contadores["agachamento"]
repeticoes_4 = contadores["repeticoes_4"]
barras = contadores["barras"]

# Função para verificar e atualizar exercícios ao completar 5 repetições
def verificar_repeticoes():
    global repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras
    while repeticoes_1 >= 5:
        repeticoes_1 -= 5
        flexao += 5  # Adiciona +1 ao contador de flexões completas
    while repeticoes_2 >= 5:
        repeticoes_2 -= 5
        abdominais += 5  # Adiciona +1 ao contador de abdominais completos
    while repeticoes_3 >= 5:
        repeticoes_3 -= 5
        agachamento += 5  # Adiciona +1 ao contador de agachamentos completos
    while repeticoes_4 >= 5:
        repeticoes_4 -= 5
        barras += 5  # Adiciona +1 ao contador de barras completas
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)

# Página principal
@app.route("/")
def homepage():
    global repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras
    return render_template_string("""
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Nome da Empresa</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      text-align: center;
    }

    header {
      padding: 20px;
      font-size: 24px;
      font-weight: bold;
    }

    nav {
      border-top: 3px solid black;
      border-bottom: 3px solid black;
      padding: 10px 0;
    }

    nav a {
      text-decoration: none;
      color: black;
      margin: 0 15px;
      font-size: 18px;
    }

    nav span {
      margin: 0 10px;
      color: black;
    }

    .team-section {
      margin-top: 40px;
    }

    .team-section p {
      font-size: 18px;
      margin-bottom: 10px;
    }

    .team-image {
      width: 600px;
      height: 200px;
      border: 4px solid black;
      margin: 0 auto;
    }
  </style>
</head>
<body>

  <header>nome da empresa</header>

  <nav>
    <a href="#">inicio</a>
    <span>|</span>
    <a href="#">quem nos somos</a>
    <span>|</span>
    <a href="#">financeiro</a>
    <span>|</span>
    <a href="#">nossa Historia</a>
  </nav>

  <div class="team-section">
    <p>imagem de equipe</p>
    <div class="team-image"></div>
  </div>

</body>
</html>

    """, ex1=flexao, rep1=repeticoes_1, ex2=abdominais, rep2=repeticoes_2, ex3=agachamento, rep3=repeticoes_3, ex4=barras, rep4=repeticoes_4)

# Rota para incrementar a flexão completa
@app.route("/incrementar_flexao")
def incrementar_flexao():
    global flexao
    flexao += 1
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para decrementar a flexão completa
@app.route("/decrementar_flexao")
def decrementar_flexao():
    global flexao
    if flexao > 0:
        flexao -= 1
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para incrementar 10 flexões completas
@app.route("/incrementar_flexao_10")
def incrementar_flexao_10():
    global flexao
    flexao += 10  # Incrementa 10 flexões
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para decrementar 10 flexões completas
@app.route("/decrementar_flexao_10")
def decrementar_flexao_10():
    global flexao
    if flexao >= 10:
        flexao -= 10  # Decrementa 10 flexões
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para incrementar a barra completa
@app.route("/incrementar_barras")
def incrementar_barras():
    global barras
    barras += 1
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para decrementar a barra completa
@app.route("/decrementar_barras")
def decrementar_barras():
    global barras
    if barras > 0:
        barras -= 1
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para incrementar 10 barras completas
@app.route("/incrementar_barras_10")
def incrementar_barras_10():
    global barras
    barras += 10  # Incrementa 10 barras
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para decrementar 10 barras completas
@app.route("/decrementar_barras_10")
def decrementar_barras_10():
    global barras
    if barras >= 10:
        barras -= 10  # Decrementa 10 barras
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

#--------------------------------------------------------------------------------
# Rota para incrementar o agachamento completo
@app.route("/incrementar_agachamento")
def incrementar_agachamento():
    global agachamento
    agachamento += 1
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para decrementar o agachamento completo
@app.route("/decrementar_agachamento")
def decrementar_agachamento():
    global agachamento
    if agachamento > 0:
        agachamento -= 1
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para incrementar 10 agachamentos completos
@app.route("/incrementar_agachamento_10")
def incrementar_agachamento_10():
    global agachamento
    agachamento += 10  # Incrementa 10 agachamentos
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para decrementar 10 agachamentos completos
@app.route("/decrementar_agachamento_10")
def decrementar_agachamento_10():
    global agachamento
    if agachamento >= 10:
        agachamento -= 10  # Decrementa 10 agachamentos
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para incrementar o abdominal completo
@app.route("/incrementar_abdominais")
def incrementar_abdominais():
    global abdominais
    abdominais += 1
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para decrementar o abdominal completo
@app.route("/decrementar_abdominais")
def decrementar_abdominais():
    global abdominais
    if abdominais > 0:
        abdominais -= 1
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para incrementar 10 abdominais completos
@app.route("/incrementar_abdominais_10")
def incrementar_abdominais_10():
    global abdominais
    abdominais += 10  # Incrementa 10 abdominais
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

# Rota para decrementar 10 abdominais completos
@app.route("/decrementar_abdominais_10")
def decrementar_abdominais_10():
    global abdominais
    if abdominais >= 10:
        abdominais -= 10  # Decrementa 10 abdominais
    salvar_contadores(repeticoes_1, flexao, repeticoes_2, abdominais, repeticoes_3, agachamento, repeticoes_4, barras)
    return homepage()

#---------------------------------------------------------------------------------


# Função de incrementar a quantidade de repetições de cada exercício
@app.route("/incrementar_repeticoes_1")
def incrementar_repeticoes_1():
    global repeticoes_1
    repeticoes_1 += 1
    verificar_repeticoes()  # Verificar se atingiu múltiplos de 5
    return homepage()

@app.route("/decrementar_repeticoes_1")
def decrementar_repeticoes_1():
    global repeticoes_1
    if repeticoes_1 > 0:
        repeticoes_1 -= 1
    verificar_repeticoes()  # Verificar se atingiu múltiplos de 5
    return homepage()

@app.route("/incrementar_repeticoes_2")
def incrementar_repeticoes_2():
    global repeticoes_2
    repeticoes_2 += 1
    verificar_repeticoes()  # Verificar se atingiu múltiplos de 5
    return homepage()

@app.route("/decrementar_repeticoes_2")
def decrementar_repeticoes_2():
    global repeticoes_2
    if repeticoes_2 > 0:
        repeticoes_2 -= 1
    verificar_repeticoes()  # Verificar se atingiu múltiplos de 5
    return homepage()

@app.route("/incrementar_repeticoes_3")
def incrementar_repeticoes_3():
    global repeticoes_3
    repeticoes_3 += 1
    verificar_repeticoes()  # Verificar se atingiu múltiplos de 5
    return homepage()

@app.route("/decrementar_repeticoes_3")
def decrementar_repeticoes_3():
    global repeticoes_3
    if repeticoes_3 > 0:
        repeticoes_3 -= 1
    verificar_repeticoes()  # Verificar se atingiu múltiplos de 5
    return homepage()

@app.route("/incrementar_repeticoes_4")
def incrementar_repeticoes_4():
    global repeticoes_4
    repeticoes_4 += 1
    verificar_repeticoes()  # Verificar se atingiu múltiplos de 5
    return homepage()

@app.route("/decrementar_repeticoes_4")
def decrementar_repeticoes_4():
    global repeticoes_4
    if repeticoes_4 > 0:
        repeticoes_4 -= 1
    verificar_repeticoes()  # Verificar se atingiu múltiplos de 5
    return homepage()

if __name__ == "__main__":
    app.run(debug=True)

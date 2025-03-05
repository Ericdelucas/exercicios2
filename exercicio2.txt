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
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Contador de Exercícios</title>
            <style>
                body {
                    background-color: #121212;
                    color: white;
                    font-family: Arial, sans-serif;
                }
                h1 {
                    color: #ff0000;
                    text-align: center;
                }
                .container {
                    display: flex;
                    justify-content: space-between;
                    padding: 20px;
                }
                .contador {
                    background-color: #1e1e1e;
                    padding: 20px;
                    border-radius: 10px;
                    width: 22%;
                    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
                }
                .contador p {
                    font-size: 14px;
                }
                button {
                    background-color: #333;
                    color: white;
                    border: 1px solid #444;
                    padding: 10px;
                    margin: 5px;
                    border-radius: 5px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #444;
                }
                input {
                    padding: 5px;
                    width: 50px;
                    margin: 5px;
                    border: 1px solid #444;
                    border-radius: 5px;
                    background-color: #222;
                    color: white;
                }
            </style>
        </head>
        <body>
            <h1>Contador de Exercícios</h1>
            <div class="container">
                <!-- Contador de Flexões -->
                <div class="contador">
                    <h2>Flexão</h2>
                    <p>Flexões completas: {{ ex1 }}</p>
                    <p>Repetições: {{ rep1 }}/5</p>
                    <button onclick="window.location.href='/incrementar_repeticoes_1'">+1</button>
                    <button onclick="window.location.href='/decrementar_repeticoes_1'">-1</button>
                    <input type="number" id="num1" placeholder="Qtd" min="1">
                    <button onclick="adicionarRepeticoes(1)">Adicionar</button>

                    <br><br>

                    <!-- Botões para incrementar e decrementar as flexões completas -->
                    <button onclick="window.location.href='/incrementar_flexao'">+1 Flexão Completa</button>
                    <button onclick="window.location.href='/decrementar_flexao'">-1 Flexão Completa</button>

                    <br><br>

                    <!-- Botões para incrementar e decrementar as flexões completas em 10 -->
                    <button onclick="window.location.href='/incrementar_flexao_10'">+10 Flexões Completas</button>
                    <button onclick="window.location.href='/decrementar_flexao_10'">-10 Flexões Completas</button>
                </div>

                <!-- Contador de Abdominais -->
                <div class="contador">
                    <h2>Abdominais</h2>
                    <p>Abdominais completos: {{ ex2 }}</p>
                    <p>Repetições: {{ rep2 }}/5</p>
                    <button onclick="window.location.href='/incrementar_repeticoes_2'">+1</button>
                    <button onclick="window.location.href='/decrementar_repeticoes_2'">-1</button>
                    <input type="number" id="num2" placeholder="Qtd" min="1">
                    <button onclick="adicionarRepeticoes(2)">Adicionar</button>

                    <br><br>

                    <!-- Botões para incrementar e decrementar os abdominais completos -->
                    <button onclick="window.location.href='/incrementar_abdominais'">+1 Abdominal Completo</button>
                    <button onclick="window.location.href='/decrementar_abdominais'">-1 Abdominal Completo</button>

                    <br><br>

                    <!-- Botões para incrementar e decrementar os abdominais completos em 10 -->
                    <button onclick="window.location.href='/incrementar_abdominais_10'">+10 Abdominais Completos</button>
                    <button onclick="window.location.href='/decrementar_abdominais_10'">-10 Abdominais Completos</button>
                </div>

                <!-- Contador de Agachamentos -->
                <div class="contador">
                    <h2>Agachamentos</h2>
                    <p>Agachamentos completos: {{ ex3 }}</p>
                    <p>Repetições: {{ rep3 }}/5</p>
                    <button onclick="window.location.href='/incrementar_repeticoes_3'">+1</button>
                    <button onclick="window.location.href='/decrementar_repeticoes_3'">-1</button>
                    <input type="number" id="num3" placeholder="Qtd" min="1">
                    <button onclick="adicionarRepeticoes(3)">Adicionar</button>

                    <br><br>

                    <!-- Botões para incrementar e decrementar os agachamentos completos -->
                    <button onclick="window.location.href='/incrementar_agachamento'">+1 Agachamento Completo</button>
                    <button onclick="window.location.href='/decrementar_agachamento'">-1 Agachamento Completo</button>

                    <br><br>

                    <!-- Botões para incrementar e decrementar os agachamentos completos em 10 -->
                    <button onclick="window.location.href='/incrementar_agachamento_10'">+10 Agachamentos Completos</button>
                    <button onclick="window.location.href='/decrementar_agachamento_10'">-10 Agachamentos Completos</button>
                </div>

                <!-- Contador de Barras -->
                <div class="contador">
                    <h2>Barras</h2>
                    <p>Barras completas: {{ ex4 }}</p>
                    <p>Repetições: {{ rep4 }}/5</p>
                    <button onclick="window.location.href='/incrementar_repeticoes_4'">+1</button>
                    <button onclick="window.location.href='/decrementar_repeticoes_4'">-1</button>
                    <input type="number" id="num4" placeholder="Qtd" min="1">
                    <button onclick="adicionarRepeticoes(4)">Adicionar</button>

                    <br><br>

                    <!-- Botões para incrementar e decrementar as barras completas -->
                    <button onclick="window.location.href='/incrementar_barras'">+1 Barra Completa</button>
                    <button onclick="window.location.href='/decrementar_barras'">-1 Barra Completa</button>

                    <br><br>

                    <!-- Botões para incrementar e decrementar as barras completas em 10 -->
                    <button onclick="window.location.href='/incrementar_barras_10'">+10 Barras Completas</button>
                    <button onclick="window.location.href='/decrementar_barras_10'">-10 Barras Completas</button>
                </div>
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

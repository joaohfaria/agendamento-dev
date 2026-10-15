#Rotas
from main import app
from flask import render_template, request

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agendar', methods=['POST'])
def agendar():
    # Lógica para processar o agendamento
    nome = request.form['nome']
    data = request.form['data']
    hora = request.form['hora']
    telefone = request.form['telefone']
    placa = request.form['placa']
    servico = request.form['servico']

    return f"Agendamento realizado com sucesso {nome}, {data} às {hora}"
#Rotas
from main import app
from flask import render_template, request
import sqlite3

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agendar', methods=['POST'])
def agendar():

    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    placa = request.form['placa']
    data = request.form['data']
    hora = request.form['hora']
    servico = request.form['servico']

    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    cursor.execute("INSERT INTO agendamentos (nome, email, telefone, placa, data, hora, servico) VALUES (?, ?, ?, ?, ?, ?, ?)", (nome, email, telefone, placa, data, hora, servico))
    db.commit()
    db.close()
    return f"Agendamento realizado com sucesso {nome}, {data} às {hora}"
#Rotas
from main import app
from flask import render_template, request 
from validacoes import validar_data
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
    
    if not validar_data(data, hora):
        return "Data e hora inválidas. Por favor, selecione uma data e hora futura."

    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    cursor.execute("INSERT INTO agendamentos (nome, email, telefone, placa, data, hora, servico) VALUES (?, ?, ?, ?, ?, ?, ?)", (nome, email, telefone, placa, data, hora, servico))
    db.commit()
    db.close()
    return f"Agendamento realizado com sucesso {nome}, {data} às {hora}"

@app.route('/agendamentos')
def agendamentos():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM agendamentos ORDER BY data, hora")
    
    servico = cursor.fetchall()
    
    db.close()
    return render_template('agendamentos.html', agendamentos=servico )           
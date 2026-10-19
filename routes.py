#Rotas
from main import app
from flask import render_template, request, redirect, url_for
from validacoes import data_valida
from flask import session as sessao
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
    
    if not data_valida(data, hora):
        return "Data e hora inválidas. Por favor, selecione uma data e hora futura."

    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    cursor.execute("SELECT * FROM agendamentos WHERE data = ? AND hora = ?", (data, hora))
    agendamento_existente = cursor.fetchone()

    if agendamento_existente:
        db.close()
        return "Já existe um agendamento para essa data e hora. Por favor, escolha outro horário."

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

@app.route('/entrar', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        if usuario == app.config.get('USUARIO_CORRETO') and senha == app.config.get('SENHA_CORRETA'):
            sessao['usuario'] = usuario
            return redirect(url_for('sucesso'))
        else:
            return "Usuário ou senha incorretos. Tente novamente."

    return render_template('login.html')          

if __name__ == '__main__':
    app.run(debug=True)


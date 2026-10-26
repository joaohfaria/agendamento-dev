#Rotas
from main import app
from flask import render_template, request, redirect, url_for
from flask import session as sessao
from werkzeug.security import check_password_hash
from datetime import datetime
from validacoes import validar_agendamento
import sqlite3


@app.route('/')
def index():
    connection = None
    servicos = []

    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT nome FROM servicos")

        resultado = cursor.fetchall()
        servicos = [[linha[0]] for linha in resultado]

    except Exception as e:
        print(f"Erro ao buscar serviços: {e}")

    finally:
        if connection:
            connection.close()

    return render_template('index.html', servicos=servicos)
    

      

@app.route('/agendar', methods=['POST'])
def agendar():

    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    placa = request.form.get('placa')
    data = request.form.get('data')
    hora = request.form.get('hora')
    servico = request.form.get('servico')

    erro = validar_agendamento(data, hora)
    if erro:
        return erro

    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    cursor.execute("SELECT id FROM agendamentos WHERE data = ? AND hora = ?", (data, hora))
    agendamento_existente = cursor.fetchone()

    if agendamento_existente:
        db.close()
        return "Já existe um agendamento para essa data e hora. Por favor, escolha outro horário."

    cursor.execute("SELECT id FROM servicos WHERE nome = ?", (servico,))
    servico_encontrado = cursor.fetchone()

    if not servico_encontrado:
        db.close()
        return "Serviço inválido."

    cursor.execute(
        "INSERT INTO agendamentos (nome, email, telefone, placa, data, hora, servico) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (nome, email, telefone, placa, data, hora, servico)
    )
    db.commit()
    db.close()

    return f"Agendamento realizado com sucesso {nome}, {data} às {hora}"


@app.route('/agendamentos')
def agendamentos():
    if 'usuario' not in sessao:
        return redirect(url_for('login'))

    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    cursor.execute("SELECT nome, email, telefone, placa, data, hora, servico FROM agendamentos ORDER BY data, hora")
    lista = cursor.fetchall()

    db.close()

    return render_template('agendamentos.html', agendamentos=lista)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        db = sqlite3.connect('database.db')
        cursor = db.cursor()

        cursor.execute("SELECT senha_hash FROM usuarios WHERE usuario = ?", (usuario,))
        encontrado = cursor.fetchone()

        db.close()

        if not encontrado:
            return "Usuário ou senha inválidos."

        senha_hash = encontrado[0]

        if not check_password_hash(senha_hash, senha):
            return "Usuário ou senha inválidos."

        sessao['usuario'] = usuario
        return redirect(url_for('sucesso'))

    return render_template('login.html')


@app.route('/sucesso')
def sucesso():
    if 'usuario' not in sessao:
        return redirect(url_for('login'))

    return render_template('sucesso.html', usuario=sessao['usuario'])

@app.route('/logout')
def logout():
    sessao.clear()
    return redirect(url_for('login'))


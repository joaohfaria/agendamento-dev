#Rotas
from main import app
from flask import render_template, request, redirect, url_for
from flask import session as sessao
from werkzeug.security import check_password_hash
from datetime import datetime
from validacoes import validar_agendamento, HORARIOS_PERMITIDOS
import sqlite3

def buscar_servicos():
    connection = None
    servicos = []
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT nome FROM servicos")
        servicos = cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar serviços: {e}")
    finally:
        if connection:
            connection.close()
    return servicos


def pagina_inicial(erro=None, dados=None):
    return render_template(
        'index.html',
        servicos=buscar_servicos(),
        horarios=HORARIOS_PERMITIDOS,
        erro=erro,
        dados=dados
    )


@app.route('/')
def index():
    return pagina_inicial()


@app.route('/agendar', methods=['POST'])
def agendar():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    placa = request.form.get('placa')
    data = request.form.get('data')
    hora = request.form.get('hora')
    servico = request.form.get('servico')

    dados_preenchidos = {
        'nome': nome, 'email': email, 'telefone': telefone,
        'placa': placa, 'data': data, 'hora': hora, 'servico': servico
    }

    if not all([nome, email, telefone, placa, data, hora, servico]):
        return pagina_inicial("Todos os campos são obrigatórios.", dados_preenchidos)

    erro = validar_agendamento(data, hora)
    if erro:
        return pagina_inicial(erro, dados_preenchidos)

    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    cursor.execute("SELECT id FROM agendamentos WHERE data = ? AND hora = ?", (data, hora))
    agendamento_existente = cursor.fetchone()

    if agendamento_existente:
        db.close()
        return pagina_inicial("Já existe um agendamento para essa data e hora. Escolha outro horário.", dados_preenchidos)

    cursor.execute("SELECT id FROM servicos WHERE nome = ?", (servico,))
    servico_encontrado = cursor.fetchone()

    if not servico_encontrado:
        db.close()
        return pagina_inicial("Serviço inválido.", dados_preenchidos)

    cursor.execute(
        "INSERT INTO agendamentos (nome, email, telefone, placa, data, hora, servico) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (nome, email, telefone, placa, data, hora, servico)
    )
    db.commit()
    db.close()

    return f"Agendamento realizado com sucesso {nome}, {data} às {hora}"

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
        return redirect(url_for('agendamentos'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    sessao.clear()
    return redirect(url_for('login'))


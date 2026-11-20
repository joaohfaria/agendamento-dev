#Rotas
from main import app
from flask import render_template, request, redirect, url_for, flash
from flask import session as sessao
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from validacoes import validar_agendamento, data_disponivel, HORARIOS_PERMITIDOS, STATUS_PERMITIDOS
from conexao import conectar

@app.route('/horarios_livres/<data>')
def horarios_livres(data):

    try:
        datetime.strptime(data, '%Y-%m-%d')
    except ValueError:
        return {"erro": "Formato de data inválido. Use AAAA-MM-DD."}, 400

    erro = data_disponivel(data)
    if erro:
        return {"horarios_livres": []}
    
    db = None
    try:
        db = conectar()
        cursor = db.cursor()

        cursor.execute("SELECT hora FROM agendamentos WHERE data = %s", (data,))
        horarios_ocupados = [row[0] for row in cursor.fetchall()]

        horarios_livres = [hora for hora in HORARIOS_PERMITIDOS if hora not in horarios_ocupados]
    finally:
        if db:
            db.close()

    return {"horarios_livres": horarios_livres}

def buscar_servicos():
    connection = None
    servicos = []
    try:
        connection = conectar()
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

    db = None
    try:
        db = conectar()
        cursor = db.cursor()

        cursor.execute("SELECT id FROM agendamentos WHERE data = %s AND hora = %s", (data, hora))
        agendamento_existente = cursor.fetchone()

        if agendamento_existente:
            return pagina_inicial("Já existe um agendamento para essa data e hora. Escolha outro horário.", dados_preenchidos)

        cursor.execute("SELECT id FROM servicos WHERE nome = %s", (servico,))
        servico_encontrado = cursor.fetchone()

        if not servico_encontrado:
            return pagina_inicial("Serviço inválido.", dados_preenchidos)

        cursor.execute(
            "INSERT INTO agendamentos (nome, email, telefone, placa, data, hora, servico) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nome, email, telefone, placa, data, hora, servico)
        )
        db.commit()

        flash(f"Seu agendamento foi realizado com sucesso {nome} para {data} às {hora}.")
        return redirect(url_for('agendamento_confirmado'))

    finally:
        if db:
            db.close()


@app.route('/agendamentos')
def agendamentos():
    if 'usuario' not in sessao:
        return redirect(url_for('login'))

    db = conectar()
    cursor = db.cursor()

    cursor.execute("SELECT id, nome, email, telefone, placa, data, hora, servico, status FROM agendamentos ORDER BY data, hora")
    lista = cursor.fetchall()

    db.close()

    return render_template('agendamentos.html', agendamentos=lista)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        db = conectar()
        cursor = db.cursor()

        cursor.execute("SELECT senha_hash FROM usuarios WHERE usuario = %s", (usuario,))
        encontrado = cursor.fetchone()

        db.close()

        if not encontrado:
            return render_template('login.html', erro="Usuário ou senha inválidos.")

        senha_hash = encontrado[0]

        if not check_password_hash(senha_hash, senha):
            return render_template('login.html', erro="Usuário ou senha inválidos.")

        sessao['usuario'] = usuario
        return redirect(url_for('agendamentos'))

    return render_template('login.html')


@app.route('/atualizar_status/<int:agendamento_id>', methods=['POST'])
def atualizar_status(agendamento_id):
    if 'usuario' not in sessao:
        return redirect(url_for('login'))

    novo_status = request.form.get('status')

    if novo_status not in STATUS_PERMITIDOS:
        permitidos = ", ".join(STATUS_PERMITIDOS)
        return f"Status invalido. Apenas {permitidos} sao aceitos.", 400

    db = conectar()
    cursor = db.cursor()

    cursor.execute("UPDATE agendamentos SET status = %s WHERE id = %s", (novo_status, agendamento_id))
    db.commit()
    db.close()

    return redirect(url_for('agendamentos'))


@app.route('/agendamento_confirmado')
def agendamento_confirmado():
    return render_template('agendamento_confirmado.html')


@app.route('/logout')
def logout():
    sessao.clear()
    return redirect(url_for('login'))

@app.route('/trocar_senha', methods=['GET', 'POST'])
def trocar_senha():
    if 'usuario' not in sessao:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('trocar_senha.html')

    senha_atual = request.form.get('senha_atual')
    senha_nova = request.form.get('senha_nova')
    confirmacao = request.form.get('confirmacao')

    if not all([senha_atual, senha_nova, confirmacao]):
        return render_template('trocar_senha.html', erro="Preencha todos os campos.")

    if senha_nova != confirmacao:
        return render_template('trocar_senha.html', erro="As senhas novas não conferem.")

    if len(senha_nova) < 8:
        return render_template('trocar_senha.html', erro="A senha nova precisa ter pelo menos 8 caracteres.")

    usuario = sessao['usuario']

    db = None
    try:
        db = conectar()
        cursor = db.cursor()

        cursor.execute("SELECT senha_hash FROM usuarios WHERE usuario = %s", (usuario,))
        encontrado = cursor.fetchone()

        if not encontrado or not check_password_hash(encontrado[0], senha_atual):
            return render_template('trocar_senha.html', erro="Senha atual incorreta.")

        novo_hash = generate_password_hash(senha_nova)
        cursor.execute("UPDATE usuarios SET senha_hash = %s WHERE usuario = %s", (novo_hash, usuario))
        db.commit()
    finally:
        if db:
            db.close()

    flash("Senha alterada com sucesso.")
    return redirect(url_for('agendamentos'))

        

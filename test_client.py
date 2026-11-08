from main import app

client = app.test_client()

def test_index():
    response = client.get('/')
    assert response.status_code == 200
    assert b'Nome' in response.data
    assert b'email' in response.data
    assert b'telefone' in response.data
    assert b'placa' in response.data
    assert b'data' in response.data
    assert b'hora' in response.data
    assert b'servico' in response.data

def test_agendamento_sem_login():
    response = client.get('/agendamentos')
    assert response.status_code == 302  # Redireciona para a página de login
    assert b'login' in response.data or b'Login' in response.data

def test_login(usuario_teste):
    response = client.post(
        '/login',
        data={'usuario': usuario_teste['usuario'], 'senha': usuario_teste['senha']},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Agendamentos' in response.data

def test_agendamentos_com_login(usuario_teste):
    client.post(
        '/login',
        data={'usuario': usuario_teste['usuario'], 'senha': usuario_teste['senha']},
        follow_redirects=True
    )
    
    response = client.get('/agendamentos')
    assert response.status_code == 200
    assert b'Agendamentos' in response.data

def test_status_invalido(usuario_teste):

    client.post(
        '/login',
        data={'usuario': usuario_teste['usuario'], 'senha': usuario_teste['senha']},
        follow_redirects=True
    )
    
    response = client.post('/atualizar_status/1', data={'status': 'Pago'})
    assert response.status_code == 400

def test_senha_invalida(usuario_teste):
    response = client.post(
        '/login',
        data={'usuario': usuario_teste['usuario'], 'senha': 'senha_incorreta'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert 'Usuário ou senha inválidos.' in response.data.decode('utf-8')

def test_agendamento_valido(agendamento_teste):
    response = client.post('/agendar', data=agendamento_teste, follow_redirects=True)
    assert response.status_code == 200
    assert 'sucesso' in response.data.decode('utf-8')


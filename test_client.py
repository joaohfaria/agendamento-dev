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
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

USUARIO_CORRETO = 'admin'
SENHA_CORRETA = 'senha123'

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
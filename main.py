from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')    

USUARIO_CORRETO = 'admin'
SENHA_CORRETA = 'senha123'

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
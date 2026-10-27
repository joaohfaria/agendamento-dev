from flask import Flask, render_template
import os
from dotenv import load_dotenv
from database import criar_tabelas

load_dotenv()
FLASK_DEBUG = os.getenv('FLASK_DEBUG') == '1'

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

if not app.secret_key:
    raise RuntimeError("SECRET_KEY nao definido. Por favor, defina a variável de ambiente SECRET_KEY.")

criar_tabelas()

from routes import *

if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host='0.0.0.0')


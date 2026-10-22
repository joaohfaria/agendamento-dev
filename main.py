from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()
FLASK_DEBUG = os.getenv('FLASK_DEBUG') == '1'

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')    

from routes import *

if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host='0.0.0.0')


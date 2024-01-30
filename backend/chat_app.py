import os
from app import create_app
from flask_cors import CORS

config_name = os.getenv('CONFIG') or 'default'
app = create_app(config_name)
CORS(app, origins=['*'])
# @app.route('/')
# def index():
#     return 'hello'
import os
from app import create_app

config_name = os.getenv('CONFIG') or 'default'
app = create_app(config_name)
# @app.route('/')
# def index():
#     return 'hello'
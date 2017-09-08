from flask_script import Manager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
manager = Manager(app)

from ColorApp import colorApp
app.register_blueprint(colorApp, url_prefix='/colors')

if __name__ == "__main__":
	manager.run()
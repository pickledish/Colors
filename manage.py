from flask_script import Manager
from flask import Flask

from ColorApp import colorAppBlueprint

app = Flask(__name__)
app.register_blueprint(colorAppBlueprint, url_prefix='/colors')

manager = Manager(app)

if __name__ == "__main__":
	manager.run()
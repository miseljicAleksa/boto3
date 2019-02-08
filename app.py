from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "files.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'

db = SQLAlchemy(app)
Bootstrap(app)
ma = Marshmallow(app)

import routes, api

if __name__ == "__main__":
    app.run(port=1312)
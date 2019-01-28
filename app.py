from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from filters import datetimeformat, file_type
from flask_marshmallow import Marshmallow

import os

app = Flask(__name__)
db = SQLAlchemy(app)
Bootstrap(app)
ma = Marshmallow(app)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "files.db"))
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'
SQLALCHEMY_TRACK_MODIFICATIONS = False





import routes

if __name__ == "__main__":
    app.run(port=1312)
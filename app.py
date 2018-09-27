from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/short_shared_stories'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'not_truly_secret'

db = SQLAlchemy(app)

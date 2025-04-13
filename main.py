from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy



# mydbconnection
local_server = True
app = Flask(__name__)
app.secret_key = 'sunvi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/etech'
db = SQLAlchemy(app)


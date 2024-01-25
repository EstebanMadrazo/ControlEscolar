from flask import Flask, jsonify, request, json
from routes.alumnos import alumnos
from routes.profesores import profesores
from routes.sesiones_alumnos import sesiones_alumnos
from utils.db import db
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:contraseñasegura@127.0.0.1:5432'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(alumnos)
app.register_blueprint(profesores)
app.register_blueprint(sesiones_alumnos)
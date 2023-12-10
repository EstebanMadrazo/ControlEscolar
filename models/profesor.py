from utils.db import db

class Profesor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    numeroEmpleado = db.Column(db.Integer)
    horasClase = db.Column(db.Integer)

    def __init__(self, nombres, apellidos, numeroEmpleado, horasClase):
        self.nombres = nombres
        self.apellidos = apellidos
        self.numeroEmpleado = numeroEmpleado
        self.horasClase = horasClase


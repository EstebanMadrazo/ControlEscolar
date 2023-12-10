from utils.db import db

class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    matricula = db.Column(db.String(8))
    promedio = db.Column(db.Double)
    fotoPerfilUrl = db.Column(db.String(255))
    password = db.Column(db.String(255)) 
    
    def __init__(self, nombres, apellidos, matricula, promedio, password):
        self.nombres = nombres
        self.apellidos = apellidos
        self.matricula = matricula
        self.promedio = promedio
        self.fotoPerfilUrl = None
        self.password = password
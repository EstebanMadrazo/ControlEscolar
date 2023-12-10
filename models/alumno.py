from utils.db import db

class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    matricula = db.Column(db.String(8))
    promedio = db.Column(db.Integer)
    foto_perfil_url = db.Column(db.String(255))  # Nuevo campo para almacenar la URL de la foto de perfil

    def __init__(self, nombres, apellidos, matricula, promedio):
        self.nombres = nombres
        self.apellidos = apellidos
        self.matricula = matricula
        self.promedio = promedio
        self.foto_perfil_url = None  # Inicializamos la URL de la foto de perfil como None por defecto
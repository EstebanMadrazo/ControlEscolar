from flask import Blueprint, Flask, jsonify, request, json, current_app
from models.alumno import Alumno
from utils.db import db
import bcrypt
import boto3
import botocore.exceptions
from werkzeug.utils import secure_filename

# Terminan credenciales

alumnos = Blueprint('alumnos', __name__)

@alumnos.route("/alumnos")
def getAlumnos():
        # Consultar todos los alumnos en la base de datos
        lista_alumnos = Alumno.query.all()

        # Convertir la lista de objetos Alumno a una lista de diccionarios
        alumnos_list = [{
            'id': alumno.id,
            'nombres': alumno.nombres,
            'apellidos': alumno.apellidos,
            'matricula': alumno.matricula,
            'promedio': alumno.promedio
        } for alumno in lista_alumnos]

        return jsonify(alumnos_list)

@alumnos.route('/alumnos/<int:id>', methods=['GET'])
def getAlumno(id):
    # Buscar el alumno en la base de datos por ID
    alumno = Alumno.query.get(id)

    if alumno:
        # Convertir el objeto Alumno a un diccionario antes de devolverlo como JSON
        alumno_dict = {
            'id': alumno.id,
            'nombres': alumno.nombres,
            'apellidos': alumno.apellidos,
            'matricula': alumno.matricula,
            'promedio': alumno.promedio,
            'fotoPerfilUrl': alumno.fotoPerfilUrl  # Agregar la URL de la foto de perfil
        }
        return jsonify(alumno_dict)
    else:
        return jsonify({'error': 'Alumno no encontrado'}), 404

@alumnos.route('/alumnos', methods=['POST'])
def addAlumno():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.json

        # Validar campos no nulos
        if None in [data.get('nombres'), data.get('apellidos'), data.get('matricula'), data.get('password')]:
            return jsonify({"error": "Los campos de nombres, apellidos, matricula y password no pueden ser nulos"}), 400

        # Validar promedio no negativo
        if data.get('promedio', 0) < 0:
            return jsonify({"error": "El promedio no puede ser negativo"}), 400

        # Encriptar la contraseña
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        # Crear un nuevo objeto Alumno
        nuevo_alumno = Alumno(
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            matricula=data['matricula'],
            promedio=data.get('promedio', 0),
            password=hashed_password
        )

        # Agregar el nuevo alumno a la sesión de la base de datos
        db.session.add(nuevo_alumno)

        # Intentar guardar el nuevo alumno en la base de datos
        db.session.commit()

        return jsonify({
            "id": nuevo_alumno.id,
            "nombres": nuevo_alumno.nombres,
            "apellidos": nuevo_alumno.apellidos,
            "matricula": nuevo_alumno.matricula,
            "promedio": nuevo_alumno.promedio,
            "password": nuevo_alumno.password
        }), 201

    except ValueError:
        return jsonify({"error": "El promedio debe ser un número entero"}), 400
    except Exception as e:
        # Manejar otros errores de base de datos u otras excepciones
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # Cerrar la sesión de la base de datos
        db.session.close()

@alumnos.route('/alumnos/<int:id>', methods=['PUT'])
def updateAlumno(id):
    try:
        # Obtener el objeto Alumno de la base de datos por ID
        alumno = Alumno.query.get(id)

        if alumno:
            # Validar campos no nulos
            data = request.json
            if None in [data.get('nombres'), data.get('apellidos'), data.get('matricula')]:
                return jsonify({"error": "Los campos de nombres, apellidos y matricula no pueden ser nulos"}), 400

            # Actualizar los campos del alumno con los valores proporcionados
            if 'nombres' in data:
                alumno.nombres = str(data['nombres'])
            if 'apellidos' in data:
                alumno.apellidos = str(data['apellidos'])
            if 'matricula' in data:
                alumno.matricula = str(data['matricula'])
            if 'promedio' in data:
                alumno.promedio = int(data['promedio'])

            # Guardar los cambios en la base de datos
            db.session.commit()

            # Convertir el objeto Alumno a un diccionario antes de devolverlo como JSON
            alumno_dict = {
                'id': alumno.id,
                'nombres': alumno.nombres,
                'apellidos': alumno.apellidos,
                'matricula': alumno.matricula,
                'promedio': alumno.promedio
            }

            return jsonify({"message": "Alumno modificado correctamente", "alumno": alumno_dict})
        else:
            return jsonify({"error": "Alumno no encontrado"}), 404

    except ValueError:
        return jsonify({"error": "El id y el promedio deben ser números enteros"}), 400
    except Exception as e:
        # Manejar otros errores de base de datos u otras excepciones
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # Cerrar la sesión de la base de datos
        db.session.close()

@alumnos.route('/alumnos/<int:id>', methods=['DELETE'])
def deleteAlumno(id):
    try:
        # Obtener el objeto Alumno de la base de datos por ID
        alumno = Alumno.query.get(id)

        if alumno:
            # Eliminar el alumno de la base de datos
            db.session.delete(alumno)
            db.session.commit()

            # Convertir el objeto Alumno a un diccionario antes de devolverlo como JSON
            alumno_dict = {
                'id': alumno.id,
                'nombres': alumno.nombres,
                'apellidos': alumno.apellidos,
                'matricula': alumno.matricula,
                'promedio': alumno.promedio
            }

            return jsonify({"message": "Alumno eliminado correctamente", "alumno_eliminado": alumno_dict})
        else:
            return jsonify({"error": "Alumno no encontrado"}), 404

    except Exception as e:
        # Manejar otros errores de base de datos u otras excepciones
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # Cerrar la sesión de la base de datos
        db.session.close()

@alumnos.route('/alumnos/<int:id>/fotoPerfil', methods=['POST'])
def uploadFotoPerfil(id):
    try:
        # Verificar si se incluyó un archivo en la solicitud
        if 'foto' not in request.files:
            return jsonify({"error": "No se incluyó ningún archivo"}), 405

        file = request.files['foto']

        # Verificar si el archivo tiene un nombre
        if file.filename == '':
            return jsonify({"error": "Nombre de archivo no válido"}), 400

        # Verificar si el alumno existe en la base de datos
        alumno = Alumno.query.get(id)
        if not alumno:
            return jsonify({"error": "Alumno no encontrado"}), 404

        # Subir la imagen a S3
        filename = secure_filename(file.filename)
        s3.upload_fileobj(file, S3_BUCKET, filename)

        # Actualizar la URL de la foto de perfil en la base de datos
        alumno.fotoPerfilUrl = f'https://{S3_BUCKET}.s3.amazonaws.com/{filename}'
        db.session.commit()

        return jsonify({"fotoPerfilUrl": alumno.fotoPerfilUrl}), 200

    except Exception as e:
        # Manejar otros errores
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # Cerrar la sesión de la base de datos
        db.session.close()
    
"""@alumnos.route('/alumnos/<int:id>/email', methods=['POST'])
def sendEmail(id):
    try:
        # Buscar el alumno en la base de datos por ID
        alumno = Alumno.query.get(id)

        if not alumno:
            return jsonify({"error": "Alumno no encontrado"}), 404

        # Construir el mensaje para la alerta de SNS
        mensaje = f"Promedio: {alumno.promedio}\nNombres: {alumno.nombres}\nApellidos: {alumno.apellidos}"

        # Enviar la alerta de SNS
        response = sns.publish(
            TopicArn=TOPIC_ARN,
            Subject=f"Datos del alumno {alumno.nombres}",
            Message=mensaje,
            MessageStructure='string',
        )

        return jsonify({"message": "Alerta de SNS enviada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Cerrar la sesión de la base de datos
        db.session.close()
"""
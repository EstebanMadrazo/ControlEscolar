from flask import Blueprint, Flask, jsonify, request, json
from models.alumno import Alumno
from utils.db import db
import boto3
import botocore.exceptions
from werkzeug.utils import secure_filename

aws_access_key_id = 'ASIA34DVVZVVAP4C6Y3K'
aws_secret_access_key = 'uhahySFfg4UGCcSZb4e8KuTa4uKNwDRHoQJwUEdQ'
aws_session_token = 'FwoGZXIvYXdzEIn//////////wEaDBEFNmgaZWh+1p/9fSLLAbdadhjQeT48gV+myxqegPbclAGqmfDEVrM1FSoc2ArE8QK0rZQD05lRYVfGBS79LgIc9tF3bZO0uK5QSfzHi1GEFeHl0hEkypwDSv6JRtpGCNjAe9U0FyxKCc/D+rflN/LetANEspjsVpbDSu+fSmkpDcrxtkdtHEjgsotEJbGOg3qpO//ATiOaRXkepCoFKsOj3h4y6XzlWHRODF6TpX3uReRCUHfIu6s+Cu/ATjzzgHSK0aYnXsV463LgXEoaN7lN9BpQMhxofW8WKMjr06sGMi1wOf1B3Eqch3Aq+o1MdTazSeth9I0y7rGMp3r016IePJuUzfIwUCH3ZkwS41A='
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
S3_BUCKET = 'proyectoaws-s3'


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

@alumnos.route('/alumnos/<int:id>')
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
                'promedio': alumno.promedio
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
        if None in [data.get('nombres'), data.get('apellidos'), data.get('matricula')]:
            return jsonify({"error": "Los campos de nombres, apellidos y matricula no pueden ser nulos"}), 400

        # Validar promedio no negativo
        if data.get('promedio', 0) < 0:
            return jsonify({"error": "El promedio no puede ser negativo"}), 400

        # Crear un nuevo objeto Alumno
        nuevo_alumno = Alumno(
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            matricula=data['matricula'],
            promedio=data.get('promedio', 0)  # Valor predeterminado de 0 si no se proporciona el promedio
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
            "promedio": nuevo_alumno.promedio
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
    return "hello"
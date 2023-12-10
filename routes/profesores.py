from flask import Blueprint, Flask, jsonify, request, json
from utils.db import db
from models.profesor import Profesor

profesores = Blueprint('profesores', __name__)

@profesores.route('/profesores')
def getProfesores():
    try:
        # Consultar todos los profesores en la base de datos
        lista_profesores = Profesor.query.all()

        # Convertir la lista de objetos Profesor a una lista de diccionarios
        profesores_list = [{
            'id': profesor.id,
            'nombres': profesor.nombres,
            'apellidos': profesor.apellidos,
            'numeroEmpleado': profesor.numeroEmpleado,
            'horasClase': profesor.horasClase
        } for profesor in lista_profesores]

        return jsonify(profesores_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@profesores.route('/profesores/<int:id>')
def getProfesor(id):
    try:
        # Buscar el profesor en la base de datos por ID
        profesor = Profesor.query.get(id)

        if profesor:
            # Convertir el objeto Profesor a un diccionario antes de devolverlo como JSON
            profesor_dict = {
                'id': profesor.id,
                'nombres': profesor.nombres,
                'apellidos': profesor.apellidos,
                'numeroEmpleado': profesor.numeroEmpleado,
                'horasClase': profesor.horasClase
            }
            return jsonify(profesor_dict)
        else:
            return jsonify({'error': 'Profesor no encontrado'}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@profesores.route('/profesores', methods=['POST'])
def addProfesor():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.json

        # Validar campos no nulos
        if None in [data.get('nombres'), data.get('apellidos'), data.get('numeroEmpleado')]:
            return jsonify({"error": "Los campos de nombres, apellidos y número de empleado no pueden ser nulos"}), 400

        # Validar horasClase no negativo
        if data.get('horasClase', 0) < 0:
            return jsonify({"error": "Las horas de clase no pueden ser negativas"}), 400

        # Crear un nuevo objeto Profesor
        nuevo_profesor = Profesor(
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            numeroEmpleado=data.get('numeroEmpleado', 0),
            horasClase=data.get('horasClase', 0)  # Valor predeterminado de 0 si no se proporciona horasClase
        )

        # Agregar el nuevo profesor a la sesión de la base de datos
        db.session.add(nuevo_profesor)

        # Intentar guardar el nuevo profesor en la base de datos
        db.session.commit()

        # Convertir el objeto Profesor a un diccionario antes de devolverlo como JSON
        profesor_dict = {
            'id': nuevo_profesor.id,
            'nombres': nuevo_profesor.nombres,
            'apellidos': nuevo_profesor.apellidos,
            'numeroEmpleado': nuevo_profesor.numeroEmpleado,
            'horasClase': nuevo_profesor.horasClase
        }

        return jsonify(profesor_dict), 201

    except ValueError:
        return jsonify({"error": "El id y las horas de clase deben ser números enteros"}), 400
    finally:
        # Cerrar la sesión de la base de datos
        db.session.close()

@profesores.route('/profesores/<int:id>', methods=['DELETE'])
def deleteProfesor(id):
    try:
        # Obtener el objeto Profesor de la base de datos por ID
        profesor = Profesor.query.get(id)

        if profesor:
            # Eliminar el profesor de la base de datos
            db.session.delete(profesor)
            db.session.commit()

            # Convertir el objeto Profesor a un diccionario antes de devolverlo como JSON
            profesor_dict = {
                'id': profesor.id,
                'nombres': profesor.nombres,
                'apellidos': profesor.apellidos,
                'numeroEmpleado': profesor.numeroEmpleado,
                'horasClase': profesor.horasClase
            }

            return jsonify({"message": "Profesor eliminado correctamente", "profesor_eliminado": profesor_dict})
        else:
            return jsonify({"error": "Profesor no encontrado"}), 404

    except Exception as e:
        # Manejar otros errores de base de datos u otras excepciones
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # Cerrar la sesión de la base de datos
        db.session.close()
    
@profesores.route('/profesores/<int:id>', methods=['PUT'])
def updateProfesores(id):
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.json

        # Validar campos no nulos
        if None in [data.get('nombres'), data.get('apellidos'), data.get('numeroEmpleado')]:
            return jsonify({"error": "Los campos de nombres, apellidos y número de empleado no pueden ser nulos"}), 400

        # Validar horasClase no negativo
        if data.get('horasClase', 0) < 0:
            return jsonify({"error": "Las horas de clase no pueden ser negativas"}), 400

        # Buscar el profesor en la base de datos por ID
        profesor = Profesor.query.get(id)

        if profesor:
            # Actualizar los campos del profesor con los nuevos valores
            profesor.nombres = data.get('nombres', profesor.nombres)
            profesor.apellidos = data.get('apellidos', profesor.apellidos)
            profesor.numeroEmpleado = data.get('numeroEmpleado', profesor.numeroEmpleado)
            profesor.horasClase = data.get('horasClase', profesor.horasClase)

            # Guardar los cambios en la base de datos
            db.session.commit()

            # Convertir el objeto Profesor a un diccionario antes de devolverlo como JSON
            profesor_dict = {
                'id': profesor.id,
                'nombres': profesor.nombres,
                'apellidos': profesor.apellidos,
                'numeroEmpleado': profesor.numeroEmpleado,
                'horasClase': profesor.horasClase
            }

            return jsonify({"message": "Profesor modificado correctamente", "profesor": profesor_dict})
        else:
            return jsonify({'error': 'Profesor no encontrado'}), 404

    except ValueError:
        return jsonify({"error": "El id y las horas de clase deben ser números enteros"}), 400
    except Exception as e:
        # Manejar otros errores de base de datos u otras excepciones
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        # Cerrar la sesión de la base de datos
        db.session.close()
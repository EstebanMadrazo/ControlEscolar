from flask import Flask, jsonify, request

app = Flask(__name__)

from alumnos import alumnos
from profesores import profesores

@app.route('/alumnos')
def getAlumnos():
    return jsonify(alumnos)

@app.route('/alumnos/<int:id>')
def getAlumno(id):
        alumnoFound = next((alumno for alumno in alumnos if alumno['id'] == id), None)
        if alumnoFound:
            return jsonify(alumnoFound)
        else:
            return jsonify({'error': 'Alumno no encontrado'}), 404

@app.route('/alumnos', methods=['POST'])
def addAlumno():
    try:
        new_id = int(request.json['id'])
        if any(alumno['id'] == new_id for alumno in alumnos):
            return jsonify({"error": "El ID ya está en uso"}), 400

        new_alumno = {
            "id": int(request.json['id']),
            "nombres": str(request.json['nombres']),
            "apellidos": str(request.json['apellidos']),
            "matricula": str(request.json['matricula']),
            "promedio": int(request.json['promedio'])
        }
        alumnos.append(new_alumno)
        return jsonify({"message": "Alumno añadido correctamente", "alumnos": alumnos}), 201
    # Excepción id y promedio deben ser int
    except ValueError:    
        return jsonify({"error": "El ID y el promedio deben ser números enteros"}), 400
    # Excepcion por si falta un campo
    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400
    #Excepcion para Internal Server Error
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/alumnos/<int:id>', methods=['PUT'])
def updateAlumno(id):
    try:
        new_id = int(request.json['id'])

        #Verificar que el id no este en uso
        if any(alumno['id'] == new_id for alumno in alumnos):
            return jsonify({"error": "El ID ya está en uso"}), 400

        alumno = next((alumno for alumno in alumnos if alumno['id'] == id), None)

        if alumno:
            if 'id' in request.json:
                alumno['id'] = int(request.json['id'])
            if 'nombres' in request.json:
                alumno['nombres'] = str(request.json['nombres'])
            if 'apellidos' in request.json:
                alumno['apellidos'] = str(request.json['apellidos'])
            if 'matricula' in request.json:
                alumno['matricula'] = str(request.json['matricula'])
            if 'promedio' in request.json:
                alumno['promedio'] = int(request.json['promedio'])
            return jsonify({"message": "Alumno modificado correctamente", "alumno": alumno})
        else:
            return jsonify({"error": "Alumno no encontrado"}), 404
    
    #Excepcion para que el id y el promedio sean int
    except ValueError:
        return jsonify({"error": "El id y el promedio debe ser un número entero"}), 400
    #Excepcion por si falta algún campo
    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400
    #Excepcion para Internal Server Error
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/alumnos/<int:id>', methods=['DELETE'])
def deleteAlumno(id):
    try:
        alumno = next((alumno for alumno in alumnos if alumno['id'] == id), None)
        
        if alumno:
            alumnos.remove(alumno)
            return jsonify({"message": "Alumno eliminado correctamente", "alumno_eliminado": alumno})
        else:
            return jsonify({"error": "Alumno no encontrado"}), 404
    
    #Excepcion para Internal Server Error
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/profesores')
def getProfesores():
    return jsonify(profesores)

@app.route('/profesores/<int:id>')
def getProfesor(id):
        profesorFound = next((profesor for profesor in profesores if profesor['id'] == id), None)
        if profesorFound:
            return jsonify(profesorFound)
        else:
            return jsonify({'error': 'Profesor no encontrado'}), 404

@app.route('/profesores', methods=['POST'])
def addProfesor():
    try:
        new_id = int(request.json['id'])
        if any(profesor['id'] == new_id for profesor in profesores):
            return jsonify({"error": "El ID ya está en uso"}), 400

        new_profesor = {
            "id": int(request.json['id']),
            "nombres": str(request.json['nombres']),
            "apellidos": str(request.json['apellidos']),
            "numeroEmpleado": str(request.json['numeroEmpleado']),
            "horasClase": int(request.json['horasClase'])
        }
        profesores.append(new_profesor)
        return jsonify({"message": "Profesor añadido correctamente", "profesores": profesores})
    # Excepción id y promedio deben ser int
    except ValueError:    
        return jsonify({"error": "El ID y las horas de clase deben ser números enteros"}), 400
    # Excepcion por si falta un campo
    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400
    #Excepcion para Internal Server Error
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/profesores/<int:id>', methods=['PUT'])
def updateProfesor(id):
    try:
        new_id = int(request.json['id'])

        #Verificar que el id no este en uso
        if any(profesor['id'] == new_id for profesor in profesores):
            return jsonify({"error": "El ID ya está en uso"}), 400

        profesor = next((profesor for profesor in profesores if profesor['id'] == id), None)

        if profesor:
            if 'id' in request.json:
                profesor['id'] = int(request.json['id'])
            if 'nombres' in request.json:
                profesor['nombres'] = str(request.json['nombres'])
            if 'apellidos' in request.json:
                profesor['apellidos'] = str(request.json['apellidos'])
            if 'numeroEmpleado' in request.json:
                profesor['numeroEmpleado'] = str(request.json['numeroEmpleado'])
            if 'horasClase' in request.json:
                profesor['horasClase'] = int(request.json['horasClase'])
            return jsonify({"message": "Profesor modificado correctamente", "alumno": profesor})
        else:
            return jsonify({"error": "Profesor no encontrado"}), 404
    
    #Excepcion para que el id y el promedio sean int
    except ValueError:
        return jsonify({"error": "El id y las horas de clase debe ser un número entero"}), 400
    #Excepcion por si falta algún campo
    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400
    #Excepcion para Internal Server Error
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/profesores/<int:id>', methods=['DELETE'])
def deleteProfesor(id):
    try:
        profesor = next((profesor for profesor in profesores if profesor['id'] == id), None)
        
        if profesor:
            profesores.remove(profesor)
            return jsonify({"message": "Profesor eliminado correctamente", "Profesor eliminado": profesor})
        else:
            return jsonify({"error": "Profesor no encontrado"}), 404
    
    #Excepcion para Internal Server Error
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify, request, json

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
        id = int(request.json['id'])
        nombres = request.json['nombres']
        apellidos = request.json['apellidos']
        matricula = request.json['matricula']
        promedio = int(request.json['promedio'])

        # Validar campos no nulos
        if None in [nombres, apellidos, matricula]:
            return jsonify({"error": "Los campos de nombres, apellidos y matricula no pueden ser nulos"}), 400

        # Validar promedio no negativo
        if promedio < 0:
            return jsonify({"error": "El promedio no puede ser negativo"}), 400

        new_alumno = {
            "id": id,
            "nombres": nombres,
            "apellidos": apellidos,
            "matricula": matricula,
            "promedio": promedio
        }
        alumnos.append(new_alumno)
        return jsonify({"message": "Alumno añadido correctamente", "alumnos": alumnos}), 201
    except ValueError:
        return jsonify({"error": "El ID y el promedio deben ser números enteros"}), 400
    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400


@app.route('/alumnos/<int:id>', methods=['PUT'])
def updateAlumno(id):
    try:
        
        # Validar campos no nulos
        nombres = request.json['nombres']
        apellidos = request.json['apellidos']
        matricula = request.json['matricula']
        if None in [nombres, apellidos, matricula]:
            return jsonify({"error": "Los campos de nombres, apellidos y matricula no pueden ser nulos"}), 400
        
        alumnoFound = next((alumno for alumno in alumnos if alumno['id'] == id), None)
        if alumnoFound:
            if 'id' in request.json:
                alumnoFound['id'] = int(request.json['id'])
            if 'nombres' in request.json:
                alumnoFound['nombres'] = str(request.json['nombres'])
            if 'apellidos' in request.json:
                alumnoFound['apellidos'] = str(request.json['apellidos'])
            if 'matricula' in request.json:
                alumnoFound['matricula'] = str(request.json['matricula'])
            if 'promedio' in request.json:
                alumnoFound['promedio'] = int(request.json['promedio'])
            return jsonify({"message": "Alumno modificado correctamente", "alumno": alumnoFound})
        else:
            return jsonify({"error": "Alumno no encontrado"}), 404
    
    #Excepcion para que el id y el promedio sean int
    except ValueError:
        return jsonify({"error": "El id y el promedio debe ser un número entero"}), 400
    #Excepcion por si falta algún campo
    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400

@app.route('/alumnos/<int:id>', methods=['DELETE'])
def deleteAlumno(id):
        alumno = next((alumno for alumno in alumnos if alumno['id'] == id), None)
        
        if alumno:
            alumnos.remove(alumno)
            return jsonify({"message": "Alumno eliminado correctamente", "alumno_eliminado": alumno})
        else:
            return jsonify({"error": "Alumno no encontrado"}), 404

@app.route('/profesores')
def getProfesores():
    return jsonify(profesores)

@app.route('/profesores/<int:id>')
def getProfesor(id):
        profesorFound = next((profesor for profesor in profesores if profesor['id'] == id), None)
        if profesorFound:
            return jsonify(profesorFound)
        else:
            return jsonify({'error': 'Alumno no encontrado'}), 404

@app.route('/profesores', methods=['POST'])
def addProfesor():
    try:
        id = int(request.json['id'])
        nombres = str(request.json['nombres'])
        apellidos = str(request.json['apellidos'])
        numeroEmpleado = str(request.json['numeroEmpleado'])
        horasClase = int(request.json['horasClase'])

        # Validar campos no nulos
        if None in [nombres, apellidos, numeroEmpleado]:
            return jsonify({"error": "Los campos de nombres, apellidos y numero de empleado no pueden ser nulos"}), 400

        # Validar promedio no negativo
        if horasClase < 0:
            return jsonify({"error": "las horas de clase no puede ser negativo"}), 400

        new_profesor = {
            "id": id,
            "nombres": nombres,
            "apellidos": apellidos,
            "numeroEmpleado": numeroEmpleado,
            "horasClase": horasClase
        }
        profesores.append(new_profesor)
        return jsonify({"message": "Alumno añadido correctamente", "alumnos": profesores}), 201
    except ValueError:
        return jsonify({"error": "El id y las horas de clase deben ser números enteros"}), 400
    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400

@app.route('/profesores/<int:id>', methods=['PUT'])
def updateProfesores(id):
    try:

        nombres = str(request.json['nombres'])
        apellidos = str(request.json['apellidos'])
        numeroEmpleado = str(request.json['numeroEmpleado'])
        horasClase = int(request.json['horasClase'])
        
        # Validar campos no nulos
        if None in [nombres, apellidos, numeroEmpleado]:
            return jsonify({"error": "Los campos de nombres, apellidos y numero de empleado no pueden ser nulos"}), 400

        # Validar promedio no negativo
        if horasClase < 0:
            return jsonify({"error": "las horas de clase no puede ser negativo"}), 400


        profesorFound = next((profesor for profesor in profesores if profesor['id'] == id), None)
        if profesorFound:
            if 'id' in request.json:
                profesorFound['id'] = int(request.json['id'])
            if 'nombres' in request.json:
                profesorFound['nombres'] = str(request.json['nombres'])
            if 'apellidos' in request.json:
                profesorFound['apellidos'] = str(request.json['apellidos'])
            if 'numeroEmpleado' in request.json:
                profesorFound['numeroEmpleado'] = str(request.json['numeroEmpleado'])
            if 'horasClase' in request.json:
                profesorFound['horasClase'] = int(request.json['horasClase'])
            return jsonify({"message": "profesor modificado correctamente", "profesor": profesorFound})
        else:
            return jsonify({"error": "profesor no encontrado"}), 404
    
    #Excepcion para que el id y el promedio sean int
    except ValueError:
        return jsonify({"error": "El id y el horas de clase deben ser un número entero"}), 400
    #Excepcion por si falta algún campo
    except KeyError as e:
        return jsonify({"error": f"Campo faltante: {str(e)}"}), 400

@app.route('/profesores/<int:id>', methods=['DELETE'])
def deleteProfesor(id):
        profesor = next((profesor for profesor in profesores if profesor['id'] == id), None)
        
        if profesor:
            profesores.remove(profesor)
            return jsonify({"message": "profesor eliminado correctamente", "profesor_eliminado": profesor})
        else:
            return jsonify({"error": "profesor no encontrado"}), 404
    

if __name__ == '__main__':
    app.run(debug=True)
from flask import Blueprint, jsonify, request
from models.alumno import Alumno
import uuid
import time
import string
import random
from boto3.dynamodb.conditions import Key
import boto3
from botocore.exceptions import ClientError


sesiones_alumnos = Blueprint('sesiones_alumnos', __name__)

#Deharcodear las credenciales en el futuro
aws_access_key_id="ASIA34DVVZVVIEHVFQAT"
aws_secret_access_key="dOx3MUp8KhDMaWxJAA2Kv/zpPOViCpvGdANArxuL"
aws_session_token="FwoGZXIvYXdzENL//////////wEaDJHOrI9lcaLlBVU91CLLAexygg3RMaoLoYmx7TPPefrpgA9Gv9f4PEr2WXTwq7TEtYndaHtYkUoS8eSqCb45odvb97i1dCHVV5tjy5gYwX45e+UZcyayqaXp8xfallzdzgmkV8gulm25WJ6YyhGfVVJGidRKX666FlFwXY6CG4Vgkg233nIBE1V+KpoxUM98AACfiHrkcsgnALi75SBNsxqRcXZK7SYcnhNncm2F9fymwmRDXdNZa9V3+7hPvY0D1Npz/v56w41I/RSQ+BD00DSd1InR/i3EHwGyKND846sGMi3At4MVeHML5Ccu0NfaAVbQusm53lFM1OWvtUi9QZeMKkgCXhY+T5xyVy+OpRs="


dynamodb = boto3.resource('dynamodb', 
region_name='us-east-1', 
aws_access_key_id=aws_access_key_id, 
aws_secret_access_key=aws_secret_access_key,
aws_session_token=aws_session_token)

sesiones_alumnos_table = dynamodb.Table('sesiones-alumnos')  

def generate_session_string(length=128):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@sesiones_alumnos.route('/alumnos/<int:id>/session/login', methods=['POST'])
def login_alumno(id):
    try:
        password = request.json.get('password')

        alumno = Alumno.query.get(id)

        if not alumno:
            return jsonify({"error": "Alumno no encontrado"}), 404

        if alumno.password != password:
            return jsonify({"error": "Contraseña incorrecta"}), 400

        session_string = generate_session_string()

        sesion_item = {
            'id': str(uuid.uuid4()),  
            'fecha': int(time.time()),  
            'alumnoId': id,
            'active': True,
            'sessionString': session_string
        }

        sesiones_alumnos_table.put_item(Item=sesion_item)

        return jsonify({"sessionString": session_string}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        pass

@sesiones_alumnos.route('/alumnos/<int:id>/session/verify', methods=['POST'])
def verify_session(id):
    try:
        # Obtener el sessionString del cuerpo de la solicitud
        session_string = request.json.get('sessionString')

        # Realizar una operación query en DynamoDB utilizando el id del alumno
        response = sesiones_alumnos_table.query(
            IndexName='alumnoId-sessionString-index',
            KeyConditionExpression=Key('alumnoId').eq(id)
        )

        # Verificar si se encontró una entrada válida y si active es True
        if 'Items' in response and len(response['Items']) > 0:
            session_entry = response['Items'][0]
            if session_entry['sessionString'] == session_string and session_entry['active']:
                return jsonify({"status": 200}), 200
            else:
                return jsonify({"status": 400, "error": "Sesión no activa o no válida"}), 400
        else:
            return jsonify({"status": 400, "error": "Sesión no encontrada"}), 400

    except Exception as e:
        return jsonify({"status": 500, "error": str(e)}), 500

@sesiones_alumnos.route('/alumnos/<int:id>/session/logout', methods=['POST'])
def logout_alumno(id):
    try:
        # Obtener el id del alumno de la URL
        id_alumno = id

        # Realizar una operación query en DynamoDB utilizando el id del alumno
        response = sesiones_alumnos_table.query(
            IndexName='alumnoId-sessionString-index',
            KeyConditionExpression=Key('alumnoId').eq(id_alumno)
        )

        # Verificar si se encontró una entrada válida
        if 'Items' in response and len(response['Items']) > 0:
            session_entry = response['Items'][0]

            # Actualizar el valor de active a False
            sesiones_alumnos_table.update_item(
                Key={
                    'id': session_entry['id']
                },
                UpdateExpression="SET active = :active",
                ExpressionAttributeValues={
                    ':active': False
                }
            )

            return jsonify({"status": 200}), 200
        else:
            return jsonify({"status": 400, "error": "Sesión no encontrada"}), 400

    except Exception as e:
        return jsonify({"status": 500, "error": str(e)}), 500

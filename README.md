# ProyectoAWSAcademy

## Arquitectura del sistema
![Alt text](DiagramasDiseno/Arquitectura.jpg?raw=true "Arquitectura")
![Alt text](DiagramasDiseno/ServiceArchitecture.jpg?raw=true "Servicio")


## Ejecución del proyecto

**Para descargar el proyecto usa**

>git clone https://github.com/JulianChan123/ProyectoAWSAcademy

**Para ejecutar el proyecto primero crea un entorno virtual e instala las dependencias necesarias en requirements.txt**

>python -m venv venv<br />
>source venv/bin/activate<br />
>pip install -r requirements.txt

**Despues de ajustar el uri a tu base de datos debes realizar las migraciones para que se creen las tablas**

>flask db init<br />
>flask db migrate<br />
>flask db upgrade

**Para ejecutar el proyecto, debes estar dentro del venv y usar:**

>flask run


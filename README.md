[![codecov](https://codecov.io/gh/Taller-de-programacion-2-Grupo-14/ubademy-exams/branch/master/graph/badge.svg?token=OX6SAEP6S3)](https://codecov.io/gh/Taller-de-programacion-2-Grupo-14/ubademy-exams)
![linter](https://github.com/Taller-de-programacion-2-Grupo-14/ubademy-exams/actions/workflows/linters.yml/badge.svg)
# Exams
---
Repositorio encargado de contener todos los procesos asociados a los examenes, tales como crearlos, visualizarlos, completarlos y corregirlos.  
Además, contiene toda la información de los examenes y su relacion con cursos y usuarios.
## Instalacion y despliegue productivo:
### Sin Docker
Primero, es necesario crear el virtual environment
```console
$ python3 -m pip install --user virtualenv
$ python3 -m venv env
$ source env/bin/activate
```
Una vez levantado el virtual environment, es necesario instalar las dependencias indicadas en requirements.txt de la siguiente manera
```console
$ pip install -r requirements.txt
```
Luego, para correr la aplicación:
```console
$ hypercorn main:app --reload
```
De esta forma, la aplicacion estará corriendo en http://127.0.0.1:8000
### Con Docker
Para el despliegue productivo de la aplicación se provee un archivo `Dockerfile`. El mismo permitirá construir una imagen productiva de Docker del servidor de aplicación. Para construit la imagen, se utiliza el archivo MakeFile. Para compilar la imagen primero es necesario correr:
```console
$ make buildDC
```
y luego
```console
$ make runDC
```
Para levantar la aplicacion, la cual se encontrará corriendo en http://127.0.0.1:8080
## Tests
Los tests se corren en codecov por lo que de tener acceso se pueden ver los resultados ahi. En caso de querer correrlos de forma local, una vez levantado el virtual environment basta con ejecutar:
```console
$ pytest
```
## Variables de entorno necesarias para un uso completo:
- `COURSES_HOSTNAME`: URL de donde se va a interactuar con la api de cursos
- `UBADEMY_PASSWORD`: Contraseña para poder conectarse a la base de datos Mongo.

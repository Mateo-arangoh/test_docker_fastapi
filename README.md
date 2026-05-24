\# Taller AWS - FastAPI, S3, RDS, Docker, ECR y Lambda



\## Descripción

Proyecto desarrollado para el Taller AWS de Sistemas Operativos.



La aplicación permite:

\- Subir imágenes PNG/JPG/JPEG asociadas a un usuario.

\- Almacenar las imágenes en Amazon S3.

\- Registrar los datos en Amazon RDS MySQL.

\- Consultar una imagen y obtener una URL prefirmada.

\- Ejecutar la aplicación con Docker.

\- Publicar la imagen en Amazon ECR.

\- Desplegar la aplicación en AWS Lambda mediante imagen de contenedor.



\## Tecnologías usadas

\- Python

\- FastAPI

\- Boto3

\- SQLAlchemy

\- PyMySQL

\- Amazon S3

\- Amazon RDS MySQL

\- Docker

\- Amazon ECR

\- AWS Lambda



\## Endpoints



\### GET /

Verifica que la API esté funcionando.



\### POST /subir-imagen

Recibe:

\- usuario

\- imagen PNG/JPG/JPEG



Guarda la imagen en S3 y registra la información en RDS.



\### GET /consultar-imagen

Recibe:

\- usuario

\- nombre\_imagen



Consulta la base de datos y retorna una URL prefirmada para acceder a la imagen.



\## Ejecución local



```bash

pip install -r requirements.txt

uvicorn main:app --reload


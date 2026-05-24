from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import boto3
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from mangum import Mangum


app = FastAPI()

BUCKET_NAME = "user-1034986560-ueia-so"
DB_USER = "admin"
DB_PASSWORD = "Moncho007"
DB_HOST = "imagenesdb.c2z4esis67c5.us-east-1.rds.amazonaws.com"
DB_NAME = "imagenes"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

s3 = boto3.client("s3")

class Imagen(Base):
    __tablename__ = "imagenes"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(100), nullable=False)
    nombre_imagen = Column(String(255), nullable=False)
    ruta_s3 = Column(String(500), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

@app.get("/")
def inicio():
    return {"mensaje": "API de imagenes funcionando"}

@app.post("/subir-imagen")
async def subir_imagen(
    usuario: str = Form(...),
    imagen: UploadFile = File(...)
):
    formatos_permitidos = ["image/png", "image/jpeg", "image/jpg"]

    if imagen.content_type not in formatos_permitidos:
        raise HTTPException(
            status_code=415,
            detail="Formato inválido. Solo se permiten PNG, JPG o JPEG."
        )

    ruta_s3 = f"{usuario}/{imagen.filename}"

    s3.upload_fileobj(
        imagen.file,
        BUCKET_NAME,
        ruta_s3,
        ExtraArgs={"ContentType": imagen.content_type}
    )

    db = SessionLocal()
    nueva_imagen = Imagen(
        usuario=usuario,
        nombre_imagen=imagen.filename,
        ruta_s3=ruta_s3
    )
    db.add(nueva_imagen)
    db.commit()
    db.refresh(nueva_imagen)
    db.close()

    return {
        "mensaje": "Imagen cargada correctamente",
        "usuario": usuario,
        "nombre_imagen": imagen.filename,
        "ruta_s3": ruta_s3,
        "fecha_creacion": nueva_imagen.fecha_creacion
    }

@app.get("/consultar-imagen")
def consultar_imagen(usuario: str, nombre_imagen: str):
    db = SessionLocal()
    imagen = db.query(Imagen).filter(
        Imagen.usuario == usuario,
        Imagen.nombre_imagen == nombre_imagen
    ).first()
    db.close()

    if not imagen:
        raise HTTPException(
            status_code=404,
            detail="No se encontró una imagen para ese usuario y nombre."
        )

    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": imagen.ruta_s3},
        ExpiresIn=3600
    )

    return {
        "usuario": usuario,
        "nombre_imagen": nombre_imagen,
        "url": url,
        "fecha_creacion": imagen.fecha_creacion
    }
handler = Mangum(app)
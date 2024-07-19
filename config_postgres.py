from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(120), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    proyectos = db.relationship('Proyecto', backref='usuario', lazy=True)

class Proyecto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(500))
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    videos = db.relationship('Video', backref='proyecto', lazy=True)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ruta = db.Column(db.String(200), nullable=False)
    fecha_subida = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyecto.id'), nullable=False)
    analisis = db.relationship('Analisis', backref='video', uselist=False)

class Analisis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    configuracion_id = db.Column(db.Integer, db.ForeignKey('configuracion.id'), nullable=False)
    resultado = db.relationship('Resultado', backref='analisis', uselist=False)
    reportes = db.relationship('Reporte', backref='analisis', lazy=True)

class Resultado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    analisis_id = db.Column(db.Integer, db.ForeignKey('analisis.id'), nullable=False)
    indice_ocra = db.Column(db.Float, nullable=False)
    detalles = db.Column(db.Text)

class Configuracion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parametros = db.Column(db.Text, nullable=False)

class Reporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    analisis_id = db.Column(db.Integer, db.ForeignKey('analisis.id'), nullable=False)
    ruta = db.Column(db.String(200), nullable=False)
    fecha_generacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

VIDEO_DIR = 'C:\\Tesis\\TestErgo\\muestra'
OUTPUT_FOLDER = 'C:\\Tesis\\TestErgo\\resultados'
OUTPUT_VIDEO_FOLDER = 'C:\\Tesis\\TestErgo\\videoMarcado'
JSON_FOLDER = 'C:\\Tesis\\TestErgo\\archivos_json'

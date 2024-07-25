from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
app.config.from_object('config_postgres.Config')

# Configuración de conexión a la base de datos
def get_db_connection():
    conn = psycopg2.connect(
        dbname='tesis-checklist-ocra',
        user='postgres',
        password='12345',
        host='localhost',
        port='5432'
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    # Llamar al procedimiento almacenado para obtener todos los usuarios
    cur.callproc('public.get_all_users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index_prueba_conexion.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    created_by = 'admin'  # Cambia según sea necesario
    updated_by = 'admin'  # Cambia según sea necesario

    conn = get_db_connection()
    cur = conn.cursor()
    # Llamar al procedimiento almacenado para agregar un nuevo usuario
    cur.execute('CALL public.create_user(%s, %s, %s, %s, %s);',
                (username, email, password, created_by, updated_by))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

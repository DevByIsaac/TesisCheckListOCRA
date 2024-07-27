from flask import Blueprint, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2 import sql
from ..database import get_db_connection

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.callproc('public.authenticate_user', [email, password])
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result and result[0] == 'success':  # Cambia esto según el resultado esperado
            return redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')

    return render_template('login.html')

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        created_by = 'admin'  # Ajusta esto según sea necesario
        updated_by = 'admin'  # Ajusta esto según sea necesario

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.callproc('public.create_user', [username, email, password, created_by, updated_by])
            conn.commit()
            flash('Usuario registrado con éxito.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error al registrar el usuario: {e}', 'danger')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('auth.login'))

    return render_template('registro.html')

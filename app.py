#--------------------------------------------------------------------------------IMPORTS----------------------------------
from flask import Flask, render_template, Response, request, jsonify, send_file, redirect, url_for, flash, session
from functools import wraps
import datetime
from datetime import timedelta
import cv2
import json
import time
import modules.evaluacionReba as evareba
import modules.evaluacionRula as evarula
import modules.poseModule as pm
import pandas as pd
import os
import io
import numpy as np
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from firebase_admin import credentials, db, storage, auth
from config_firebase import config
import pyrebase
import firebase_admin 

app = Flask(__name__)
app.secret_key = 'Landacay05'

#--------------------------------------------------------------------------------CONEXION A LA BASE DE DATOS--------------------
cred = credentials.Certificate('admin_sdk.json')

firebase_admin.initialize_app(cred,{'databaseURL':'https://app-detecciones-default-rtdb.europe-west1.firebasedatabase.app/',
                                    'storageBucket': "app-detecciones.appspot.com"})
bucket = storage.bucket()
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

#--------------------------------------------------------------------------------VAIABLES GLOBALES--------------------
global stop_processing, df, image_directory
stop_processing = False
df = pd.DataFrame()
eva_reba = evareba.evaluacion_reba()
eva_rula = evarula.evaluacion_rula()
detector = pm.pose_detector()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

#--------------------------------------------------------------------------GESTIÓN PARA LA CARGA DE ARCHIVOS----------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_uploaded_file(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return file_path

#----------------------------------------------------------------------FUNCION PARA VERIFICAR SI TIENE SESION INICIADA--------
def requiere_user(f):
    @wraps(f)
    def decor_funcion(*args, **kwargs):
        if session.get('user') is None:
            print(session)            
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decor_funcion
#----------------------------------------------------------------------FUNCION OBTENER DATOS DEL USUARIO ACTUAL--------
def obtener_dato_user():
    dato_user = None
    if 'user' in session:
        id_user = session['user']  # Obtener el id del usuario actual desde la sesión

        ref_user = db.reference('/db_usuarios')
        # Consultar el usuario asociado al usuario actual
        usuario = ref_user.order_by_child('id_user').equal_to(id_user).get()
        
        # Verificar si se encuentra
        if usuario:
            # Convertir a una lista para iterar
            dato_user = list(usuario.values())
            return dato_user
        else:
            dato_user = None
            return dato_user            
    else:
        dato_user = None
        return dato_user
#----------------------------------------------------------------------FUNCION OBTENER SOLO NOMBRES DEL USUARIO ACTUAL--------    
def obtener_nom_user():
    dato_user = None
    
    if 'user' in session:
        id_user = session['user']  # Obtener el id del usuario actual desde la sesión
        ref_user = db.reference('/db_usuarios')  # Consultar el usuario asociado al usuario actual
        usuario = ref_user.order_by_child('id_user').equal_to(id_user).get()  # Verificar si se encuentra
        
        if usuario:
            # Convertir a una lista para iterar
            dato_user = list(usuario.values())
            
            # Obtener el nombre y apellido del primer usuario (suponiendo que solo hay uno)
            nombre = dato_user[0]['nombres']
            apellido = dato_user[0]['apellidos']
            
            # Concatenar nombre y apellido en una sola variable
            nombre_apellido = f"{nombre} {apellido}"
            
            return nombre_apellido
        else:
            dato_user = None
            return dato_user
    else:
        dato_user = None
        return dato_user

#----------------------------------------------------------------------FUNCION OBTENER LOS PUESTOS DE TRABAJO--------
def obtener_puestos_trabajo():
    puestos_trabajo = None

    ref_puesto = db.reference('/db_puesto')

    # Consultar todos los puestos de trabajo
    puesto_trabajo = ref_puesto.get()
    puestos_trabajo = list(puesto_trabajo.values())

    return puestos_trabajo
#----------------------------------------------------------------------FUNCION OBTENER DATOS DEL TRABAJADOR SEGUN EL NÚMERO DE CEDULA--------
def obtener_trabajador_actual(cedula):
    trabajador_actual = None
    if 'user' in session:
        id_user = session['user']  # Obtener el id del usuario actual desde la sesión

        ref_trab = db.reference('/db_trabajadores')
        # Consultar los trabajadores asociados al usuario actual
        trabajadores_usuario = ref_trab.order_by_child('id_user').equal_to(id_user).get()
        # Filtrar los trabajadores por el puesto especificado
        # Iterar sobre los trabajadores para buscar el que coincide con la cédula proporcionada
        for trabajador_id, trabajador_data in trabajadores_usuario.items():
            if trabajador_data.get('cedula') == cedula:
                nombre_tra = f"{trabajador_data.get('nombres')} {trabajador_data.get('apellidos')}"
                trabajador_actual = nombre_tra
                session['id_trabajador'] = trabajador_id                
                break
        
        # Verificar si se encontraron trabajadores asociados al usuario
        if nombre_tra:            
            return trabajador_actual
        else:
            trabajador_actual = None
            return trabajador_actual            
    else:
        trabajador_actual = None
        return trabajador_actual
#----------------------------------------------------------------------FUNCION OBTENER DATOS DE LOS TRABAJADORES SEGÚN EL PUESTO DE TRABAJO-------- 
def obtener_trabajadores_por_puesto(npuesto):
    lista_trabajadores = None
    if 'user' in session:
        id_user = session['user']  # Obtener el id del usuario actual desde la sesión

        ref_trab = db.reference('/db_trabajadores')
        # Consultar los trabajadores asociados al usuario actual y al puesto especificado
        trabajadores_usuario = ref_trab.order_by_child('id_user').equal_to(id_user).get()
        
        # Filtrar los trabajadores por el puesto especificado
        trabajadores_filtrados = [trab for trab in trabajadores_usuario.values() if trab.get('npuesto') == npuesto]

        # Verificar si se encontraron trabajadores asociados al usuario y al puesto especificado
        if trabajadores_filtrados:
            lista_trabajadores = trabajadores_filtrados
            return lista_trabajadores
        else:
            lista_trabajadores = None
            return lista_trabajadores            
    else:
        lista_trabajadores = None
        return lista_trabajadores
#----------------------------------------------------------------------FUNCION OBTENER ID DE EVALUACIÓN ACTUAL--------
def obtener_id_evaluacion(fecha, hora):
    eval_actual = None
    if 'user' in session:
        id_trabajador = session['id_trabajador']  # Obtener el id del usuario actual desde la sesión

        ref_eval = db.reference('/db_evaluacion')
        # Consultar los trabajadores asociados al usuario actual
        evaluaciones = ref_eval.order_by_child('id_trabajador').equal_to(id_trabajador).get()
        # Filtrar los trabajadores por el puesto especificado
        # Iterar sobre los trabajadores para buscar el que coincide con la cédula proporcionada
        for eval_id, eval_data in evaluaciones.items():
            #print(eval_id)
            if (eval_data.get('fecha') == fecha) and (eval_data.get('hora') == hora):                
                eval_actual = eval_id                                
                break
        
        # Verificar si se encontraron trabajadores asociados al usuario
        if eval_actual:                        
            return eval_actual
        else:
            eval_actual = None
            return eval_actual            
    else:
        eval_actual = None
        return eval_actual
#----------------------------------------------------------------------VERIFICA CONTROL DE CACHE--------------------------------------------
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
#----------------------------------------------------------------------CERRAR SESION Y MOSTRAR INDEX-----------------------------
@app.route('/cerrar_sesion', methods=['POST', 'GET'])
def cerrar_sesion():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('index2'))
#----------------------------------------------------------------------RUTA PRINCIPAL-----------------
@app.route('/')
def index():
    return render_template("index.html")
#----------------------------------------------------------------------RUTA LOGIN-----------------
@app.route('/login')
def login():
    return render_template("login.html")
#----------------------------------------------------------------------RUTA MANUAL-----------------
@app.route('/manual')
def manual():
    return render_template("manual.html")
#----------------------------------------------------------------------RUTA EJEMPLOS-----------------
@app.route('/ejemplos')
def ejemplos():
    return render_template("ejemplos.html")
#----------------------------------------------------------------------RUTA INFORMACION REBA-----------------
@app.route('/info_reba')
def info_reba():
    return render_template("info_reba.html")
#----------------------------------------------------------------------RUTA INFORMACION RULA-----------------
@app.route('/info_rula')
def info_rula():
    return render_template("info_rula.html")
#----------------------------------------------------------------------RUTA INFORMACION OCRA-----------------
@app.route('/info_ocra')
def info_ocra():
    return render_template("info_ocra.html")    
#----------------------------------------------------------------------RUTA REGISTRAR TRABAJADOR-----------------
@app.route('/registro_trabajador')
@requiere_user
def registro_trabajador():
    return render_template("registrar_trabajador.html")
#----------------------------------------------------------------------RUTA REGISTRAR PUESTO DE TRABAJO-----------------
@app.route('/registrar_puesto')
@requiere_user
def registrar_puesto():
    return render_template("registrar_puesto.html")
#----------------------------------------------------------------------RUTA REGISTRO USUARIO-----------------
@app.route('/registro')
def registro():
    return render_template("registro.html")

#--------------------------------------------------------------------------------RUTA BTN DETENER VIDEO-----------------
@app.route('/stop_video_processing', methods=['GET', 'POST'])
def stop_video_processing():
    global stop_processing        
    stop_processing = True
    # Devuelve una respuesta exitosa al cliente
    return jsonify({'success': True})
#----------------------------------------------------------------------RUTA VALIDAR LOGIN-----------------
@app.route('/validar_login', methods=['POST', 'GET'])
def validar_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            flash('Por favor, ingresa tu correo electrónico.', 'error')
            return redirect(url_for('login'))

        if not password:
            flash('Por favor, ingresa tu contraseña.', 'error')
            return redirect(url_for('login'))                

        try:
            user = auth.sign_in_with_email_and_password(email, password)        
            user_info = auth.get_account_info(user['idToken'])
            local_id = user_info['users'][0]['localId']        
            session['user'] = local_id                                
            return redirect(url_for('home'))
                            
        except Exception as e:
            flash('Datos erroneos. Verifica la información e intentalo de nuevo.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

#----------------------------------------------------------------------RUTA REGISTRO USUARIO-----------------
@app.route('/registrar_usuario', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        cedula = request.form['cedula']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        sexo = request.form['sexo']
        edad = request.form['edad']

        ref = db.reference('/db_usuarios')

        hay_cedula = ref.order_by_child('cedula').equal_to(cedula).get()
        hay_correo = ref.order_by_child('email').equal_to(email).get()

        if hay_cedula:
            flash('El número de cédula ya se encuentra registrado.', 'error')
            return redirect(url_for('registro'))
        
        if hay_correo:
            flash('El correo electrónico ya se encuentra registrado.', 'error')
            return redirect(url_for('registro'))

        if not email or not password or not confirm_password:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('registro'))
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'error')
            return redirect(url_for('registro'))

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return redirect(url_for('registro'))        
        
        id_user = auth.create_user_with_email_and_password(email=email, password=password)
        auth.send_email_verification(id_user['idToken'])
        if id_user:                                   
            nuevo_user = {
                'email': email,
                'password': password,
                'cedula': cedula,
                'nombres': nombres,
                'apellidos': apellidos,
                'sexo': sexo,
                'edad': edad,
                'id_user': id_user['localId']
            }
            ref.child(id_user['localId']).set(nuevo_user)
            flash('¡Registro exitoso! Puedes iniciar sesión. Click aqui', 'success')
            return render_template('registro.html')

        else:
            flash('Error al registrar usuario. Verifica la información e intentalo de nuevo.', 'error')
            return redirect(url_for('registro'))

    return render_template('registro.html')

#----------------------------------------------------------------------RUTA REGISTRO PUESTO DE TRABAJO-----------------
@app.route('/registrar_puesto_trabajo', methods=['GET', 'POST'])
@requiere_user
def registrar_puesto_trabajo():
    if request.method == 'POST':
        # Obtener el user_id del usuario actual desde la sesión
        if 'user' in session:                                        
            npuesto = request.form['npuesto']            

            ref_puesto = db.reference('/db_puesto')

            hay_puesto = ref_puesto.order_by_child('npuesto').equal_to(npuesto).get()        

            if hay_puesto:
                flash('El puesto de trabajo ya se encuentra registrado.', 'error')
                return redirect(url_for('registrar_puesto'))                

            if not npuesto:
                flash('Llenar el campo.', 'error')
                return redirect(url_for('registrar_puesto'))               
                                    
            nuevo_puesto_trabajo = {                
                'npuesto': npuesto,                
            }
            # Guardar información del trabajador en la base de datos
            ref_puesto.push(nuevo_puesto_trabajo)
            
            flash('Puesto de trabajo registrado exitosamente. Click aqui para continuar', 'success')
            return redirect(url_for('registrar_puesto'))      
        else:
            flash('Inicia sesión para registrar un puesto.', 'error')
            return redirect(url_for('login'))  

    return redirect(url_for('registrar_puesto'))
#----------------------------------------------------------------------RUTA REGISTRO TRABAJADOR-----------------
@app.route('/registrar_trabajador', methods=['GET', 'POST'])
@requiere_user
def registrar_trabajador():
    if request.method == 'POST':
        # Obtener el user_id del usuario actual desde la sesión
        if 'user' in session:                
            id_user = session['user']
            npuesto = session['npuesto']
            cedula = request.form['tcedula']
            nombres = request.form['tnombres']
            apellidos = request.form['tapellidos']
            sexo = request.form['tsexo']
            edad = request.form['tedad']

            ref_trab = db.reference('/db_trabajadores')
            print(ref_trab)

            hay_cedula = ref_trab.order_by_child('cedula').equal_to(cedula).get()        

            if hay_cedula:
                flash('El número de cédula ya se encuentra registrado.', 'error')
                return redirect(url_for('registro_trabajador'))                

            if not cedula or not nombres or not apellidos or not sexo or not edad:
                flash('Todos los campos son obligatorios.', 'error')
                return redirect(url_for('registro_trabajador'))               
                                    
            nuevo_trabajador = {                
                'cedula': cedula,
                'nombres': nombres,
                'apellidos': apellidos,
                'sexo': sexo,
                'edad': edad,
                'id_user': id_user,
                'npuesto': npuesto
            }
            # Guardar información del trabajador en la base de datos
            ref_trab.push(nuevo_trabajador)
            
            flash('Trabajador registrado exitosamente. Click aqui para continuar', 'success')
            return redirect(url_for('registro_trabajador'))      
        else:
            flash('Inicia sesión para registrar un trabajador.', 'error')
            return redirect(url_for('login'))  

    return redirect(url_for('registro_trabajador'))

#----------------------------------------------------------------------RUTA OBTENER CONSULTAR PUESTOS DE TRABAJO--------
@app.route('/puesto_tra', methods=['GET'])
def puesto_tra(): 
    usuario = obtener_dato_user()                
    npuesto = request.args.get('puesto')
    puestos_trabajo = obtener_puestos_trabajo()
    print(npuesto)
    session['npuesto'] = npuesto
    print(session)     
    lis_trabajadores = obtener_trabajadores_por_puesto(npuesto)                                   
                                            
    return render_template('home.html',npuesto=npuesto, puestos_trabajo=puestos_trabajo, lis_trabajadores=lis_trabajadores, usuario=usuario)

#----------------------------------------------------------------------RUTA HOME-----------------
@app.route('/home', methods=['GET', 'POST'])
def home():
    error=None    
    usuario = obtener_dato_user()
    puestos_trabajo = obtener_puestos_trabajo()
    if request.method == 'POST':        

        file = request.files['file']
        metodo_evaluacion = request.form['metodo']
        npuesto = request.form['puesto_trabajo']
        nom_trab = request.form['trabajador']
        lis_trabajadores = obtener_trabajadores_por_puesto(npuesto)
        tra_actual = obtener_trabajador_actual(nom_trab)
        session['nom_trabajador'] = tra_actual
        session['metodo_evaluacion'] = metodo_evaluacion        

        # Verifica si el archivo es válido
        if 'file' not in request.files:
            error='No se seleccionó ningún archivo.'

        if file.filename == '':
            error='No se seleccionó ningún archivo.'

        if nom_trab == 'Selecciona un trabajador':
            error='Seleccione un trabajador o registre uno.'

        if metodo_evaluacion == 'Seleccione metodo':
            error='Seleccione un metodo de evaluación.'
        
        # Referencia a la base de datos de trabajadores
        ref_trab = db.reference('/db_trabajadores')
        trabajadores =  ref_trab.get()         
        
        if error:
            return render_template('home.html', puestos_trabajo=puestos_trabajo, enpuesto=npuesto, lis_trabajadores=lis_trabajadores, usuario=usuario, metodo_evaluacion=metodo_evaluacion, error=error)                        

        if file and allowed_file(file.filename):
            
            if trabajadores:
                # Iterar sobre los trabajadores y actualizar sus documentos
                for key, trabajador in trabajadores.items():
                    if trabajador.get('cedula') == nom_trab:
                        registrar_evaluacion()                        
                        # Verificar si el nuevo campo ya existe en el trabajador
                        if 'npuesto' not in trabajador:
                            # Agregar el nuevo campo al trabajador
                            trabajador['npuesto'] = npuesto
                            # Actualizar el documento del trabajador en la base de datos
                            ref_trab.child(key).update(trabajador)
                            mensaje='Puesto de trabajo asignado correctamente'
                            print(mensaje)                            
                            video_path = process_uploaded_file(file)
                            break
                        elif trabajador.get('npuesto') == npuesto:                            
                            video_path = process_uploaded_file(file)
                            mensaje=None
                            break                            
                        else:
                            mensaje=f"El trabajador {trabajador['nombres']} con cédula {nom_trab} ya tiene asignado el puesto {trabajador['npuesto']}."
                            video_path =None
                            break

            return render_template('home.html', video_path=video_path, metodo_evaluacion=metodo_evaluacion, mensaje=mensaje, enpuesto=npuesto, lis_trabajadores=lis_trabajadores, usuario=usuario, puestos_trabajo=puestos_trabajo)                        
        return render_template('home.html', puestos_trabajo=puestos_trabajo, enpuesto=npuesto, lis_trabajadores=lis_trabajadores, usuario=usuario, error='Formato de archivo no válido. Use mp4, avi o mov.')
        
    return render_template('home.html', usuario=usuario, puestos_trabajo=puestos_trabajo)

#-------------------------------------------------------------------------FUNCION SUBIR ARCHIVOS EXCEL Y PDF--------------------------
def subir_archivos(nom_archivo, archivo):
    # Subir el archivo PDF generado a Firebase Storage
    blob = bucket.blob(f'archivos_datos/{nom_archivo}')
    blob.upload_from_file(archivo)

    # Obtener la URL del archivo recién subido
    url = blob.generate_signed_url(expiration=timedelta(days=7), method='GET')
    session['url'] = url
#----------------------------------------------------------------------FUNCION REGISTRAR TABLA EVALUACIÓN-----------------
def registrar_evaluacion():
    if request.method == 'POST':
        # Obtener el user_id del usuario actual desde la sesión
        if 'user' in session:                                        
            metodo_evaluacion = session['metodo_evaluacion']
            id_trabajador = session['id_trabajador']            

            ref_evaluacion = db.reference('/db_evaluacion')
            # Obtener la fecha actual (día, mes y año)
            fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y")
            session['fecha_actual'] = fecha_actual

            # Obtener la hora actual (hora, minutos y segundos)
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
            session['hora_actual'] = hora_actual                           
                                    
            nueva_evaluacion = {                
                'metodo_evaluacion': metodo_evaluacion,
                'fecha': fecha_actual,
                'hora': hora_actual,
                'id_trabajador': id_trabajador                
            }
            # Guardar información en la base de datos
            ref_evaluacion.push(nueva_evaluacion)                           

#----------------------------------------------------------------------FUNCION REGISTRAR TABLA RESULTADO EVALUACIÓN-----------------
def registrar_resultado_evaluacion():        
    # Obtener el user_id del usuario actual desde la sesión
    if 'user' in session:
        url = session['url']                                        
        id_evaluacion = obtener_id_evaluacion(session['fecha_actual'], session['hora_actual'])                    

        ref_resultado_evaluacion = db.reference('/db_resultado_evaluacion')                                   
                                
        nuevo_reul_evaluacion = {                            
            'url': url,            
            'id_evaluacion': id_evaluacion                
        }
        # Guardar información en la base de datos
        ref_resultado_evaluacion.push(nuevo_reul_evaluacion)
#--------------------------------------------------------------------------------RUTA BTN VER ÁNGULOS-----------------
@app.route('/get_angulos', methods=['GET'])
@requiere_user
def get_angulos():
    global df                                                  
    data = df.to_dict(orient='records')    
    return render_template('angulos.html', data=data)

#---------------------------------------------------------------------TODA LAS RUTAS PARA REBA--------------------------
#REBA:
@app.route('/reba_guardar_cambios', methods=['POST'])
def reba_guardar_cambios():
    datos = request.get_json()

    # Extrae los nuevos valores de T.REBA GA y T.REBA GB
    nuevoGA = datos.get('nuevoGA', {})
    nuevoGB = datos.get('nuevoGB', {})

    # Itera sobre los segundos y actualiza los valores correspondientes en el DataFrame
    for segundo, valor_ga in nuevoGA.items():
        df.loc[df['Segundo'] == int(segundo), 'T.REBA GA'] = int(valor_ga)

    for segundo, valor_gb in nuevoGB.items():
        df.loc[df['Segundo'] == int(segundo), 'T.REBA GB'] = int(valor_gb)

    # Realiza la lógica necesaria para actualizar los resultados
    actualizar_TC(df)

    # Devuelve una respuesta exitosa al cliente (puede ser un mensaje JSON)
    return jsonify({'success': True})

def actualizar_TC(df):            
    for index, fila in df.iterrows():
        colmna_ga = fila['T.REBA GA']
        colmna_gb = fila['T.REBA GB']
        
        df.at[index, 'T.REBA GA'] = colmna_ga
        df.at[index, 'T.REBA GB'] = colmna_gb
        puntuacion_tc = eva_reba.obtener_puntuacion_tc(colmna_ga, colmna_gb)
        # Asigna la puntuación calculada a la fila específica y columna 'T.REBA TC'
        df.at[index, 'T.REBA TC'] = puntuacion_tc

    # Se puede guardar el DataFrame actualizado en un archivo Excel
    #df.to_excel("path/del/archivo.xlsx", index=False)

@app.route('/guardar_cambios_tc', methods=['POST'])
def guardar_cambios_tc():
    datos = request.get_json()

    nuevoTC = datos.get('nuevoTC', {})    

    for segundo, valor_tc in nuevoTC.items():
        df.loc[df['Segundo'] == int(segundo), 'T.REBA TC'] = int(valor_tc)    

    # Realiza la lógica para actualizar los resultados
    actualizar_resultados(df)
    return jsonify({'success': True})

def actualizar_resultados(df):        
    for index, fila in df.iterrows():
        colmna_tc = fila['T.REBA TC']        
        
        df.at[index, 'T.REBA TC'] = colmna_tc        
        puntuacion_tc = eva_reba.obtener_resultado(colmna_tc)
        # Asigna la puntuación calculada a la fila específica y columna 'T.REBA RESULTADOS'
        df.at[index, 'T.REBA RESULTADOS'] = puntuacion_tc
    
@app.route('/resultados_reba', methods=['GET', 'POST'])
@requiere_user
def resultados_reba():
    usuario = obtener_dato_user()
    session
    global df, image_directory        
    # Filtra el DataFrame para obtener ciertas columnas
    resultados_df = df[['Segundo', 'P.REBA GA', 'P.REBA GB', 'T.REBA GA', 'T.REBA GB', 'T.REBA TC', 'T.REBA RESULTADOS', 'Fotogramas']]
    # Convierte los datos del DataFrame a un diccionario
    resultados_data = resultados_df.to_dict(orient='records')
    for row in resultados_data:
        row['Fotogramas'] = f"/static/imagenes_fotogramas/{row['Fotogramas'][len(image_directory)+1:]}"
    # Renderiza la plantilla resultados.html con los datos
    return render_template('result_reba.html', data=resultados_data, session=session, usuario=usuario)

#-------------------------------------------------------------------------DESCARGAR EXCEL Y PDF REBA--------------------------
@app.route('/descargar_excel_reba', methods=['GET'])
def descargar_excel_reba():
    global df
    print(df.head())
    var1 = obtener_nom_user()
    var2 = session['metodo_evaluacion']
    var3 = session['npuesto']
    var4 = session['nom_trabajador']
    var5 = f"Evaluador: {var1} / Método: {var2} / Trabajador: {var4} / Área: {var3}"
    #Verifica que df esté disponible y tenga datos
    if df.empty:
        return jsonify({'error': 'No hay datos para descargar'})

    df_reba = df[['Segundo', 'P.REBA GA', 'P.REBA GB', 'T.REBA GA', 'T.REBA GB', 'T.REBA TC', 'T.REBA RESULTADOS', 'Fotogramas']]

    # Crear la lista de datos con var1 y var2
    datos = [var5]
    # Asegurar que 'datos' tenga la misma longitud que el DataFrame
    if len(datos) < len(df_reba):
        datos += [' '] * (len(df_reba) - len(datos))
    elif len(df_reba) < len(datos):
        datos = datos[:len(df_reba)]

    df_reba['Datos'] = datos
    # Reordenar las columnas para que 'Datos' esté antes que 'Segundo'
    df_reba = df_reba[['Datos', 'Segundo', 'P.REBA GA', 'P.REBA GB', 'T.REBA GA', 'T.REBA GB', 'T.REBA TC', 'T.REBA RESULTADOS', 'Fotogramas']]

    # Crea un objeto BytesIO para almacenar el archivo Excel
    output = io.BytesIO()

    # Utiliza el escritor de Pandas para escribir el DataFrame en BytesIO
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_reba.to_excel(writer, sheet_name='Resultados_REBA', index=False)
    
    output.seek(0)

    hora_actual = session['hora_actual'] 
    fecha_actual = session['fecha_actual']
    nom_archivo = f'datos_reba_{var4}_{fecha_actual}_{hora_actual}.xlsx'
    subir_archivos(nom_archivo, output)
    registrar_resultado_evaluacion()    

    # Devuelve el archivo Excel al cliente
    return send_file(output, download_name=nom_archivo, as_attachment=True)


@app.route('/descargar_pdf_reba', methods=['GET'])
def descargar_pdf_reba():
    global df    
    var1 = obtener_nom_user()
    var2 = session['metodo_evaluacion']
    var3 = session['npuesto']
    var4 = session['nom_trabajador']
    var5 = f"{var1}  Método: {var2}"
    var6 = f"{var4}  Área: {var3}"
    if df.empty:
        return jsonify({'error': 'No hay datos para descargar'})

    df_reba = df[['Segundo', 'T.REBA GA', 'T.REBA GB', 'T.REBA TC', 'T.REBA RESULTADOS', 'Fotogramas']]
    # Crear un objeto BytesIO para almacenar el archivo Excel
    output = io.BytesIO()
    # Crear un documento PDF
    pdf = canvas.Canvas(output, pagesize=letter)
    # Configurar el formato del texto en el PDF
    pdf.setFont("Helvetica-Bold", 8)

    # Configuración de las dimensiones de la página
    page_width, page_height = letter
    # Configurar posición y formato para el encabezado de la tabla
    col_width = 50
    row_height = 20
    x_position = 50
    y_position = page_height - 50
    # Número máximo de filas por página
    max_rows_per_page = 7

    # Agregar datos adicionales centrados en la parte superior del PDF
    additional_data = {
        'Evaluador': var5,        
        'Trabajador': var6
    }
    # Calcular la posición central horizontal
    center_x = page_width / 2    

    # Dibujar datos adicionales centrados
    for label, value in additional_data.items():
        pdf.drawString(center_x - pdf.stringWidth(value, "Helvetica", 8) / 2, y_position, f"{label}: {value}")
        pdf.setFont("Helvetica-Bold", 8)
        y_position -= row_height

    # Ajustar la posición vertical para las columnas
    y_position -= row_height

    # Procesar el encabezado de la tabla (columnas)
    header_row = df_reba.columns.values.astype(str)
    for col_index, col_name in enumerate(header_row):
        if col_name == 'T.REBA RESULTADOS':
            col_width = 130  # Ajusta el ancho de la columna 'T.REBA RESULTADOS'
        else:
            col_width = 50  # Ancho predeterminado para otras columnas
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(x_position, y_position, col_name)
        x_position += col_width

    # Restablecer la posición vertical y horizontal
    y_position -= row_height
    x_position = 50
    pdf.setFont("Helvetica", 8)
    # Iterar sobre las filas y agregar páginas según sea necesario
    for index, row in enumerate(df_reba.values):
        if index % max_rows_per_page == 0 and index != 0:
            # Agregar una nueva página al PDF
            pdf.showPage()
            # Restablecer la posición vertical y horizontal para la próxima página
            y_position = page_height - 50
            x_position = 50
            pdf.setFont("Helvetica", 8)
        # Procesar las filas de datos        
        for index, item in enumerate(row):
            if df_reba.columns[index] == 'Fotogramas':
                # Obtener el valor de la columna 'Fotogramas'
                image_value = item
                # Asegurar que la ruta apunte a un archivo, no a un directorio
                if os.path.isfile(image_value):                    
                    # Usar PIL para cargar la imagen
                    img = Image.open(image_value)
                    # Volver al principio del búfer de la imagen
                    img.seek(0)
                    # Ajustar la posición vertical para la próxima imagen
                    y_position -= 75
                    # Dibujar la imagen en el PDF
                    pdf.drawInlineImage(img, (x_position + 80), (y_position), width=67, height=85)                    
                else:
                    # Manejar el caso en que la ruta no sea un archivo válido
                    print(f"La ruta {image_value} no es un archivo válido.")
            elif df_reba.columns[index] == 'T.REBA RESULTADOS':
                # Convertir la lista de tuplas a una cadena
                text_value = ', '.join(', '.join(str(val) for val in tupla) for tupla in item) if isinstance(item, list) else str(item)
                # Dividir el texto en varias líneas
                max_line_length = 30  # Ajusta la longitud máxima de la línea
                lines = [text_value[i:i+max_line_length] for i in range(0, len(text_value), max_line_length)]                
                #col_width = 120
                line_position = y_position                            
                # Dibujar las líneas de texto en posiciones separadas
                for line_index, line in enumerate(lines):
                    pdf.drawString(x_position, line_position, line)                
                    line_position -= (row_height-7)                    
            else:
                pdf.drawString(x_position, y_position, str(item))
            x_position += col_width

        # Restablecer la posición vertical y horizontal para la próxima fila
        y_position -= row_height
        x_position = 50
    # Guardar el PDF
    pdf.save()
    # Comprimir el PDF generado
    output_compressed = io.BytesIO()
    compress_pdf(output, output_compressed)
    # Devolver el archivo PDF al cliente
    output_compressed.seek(0)

    hora_actual = session['hora_actual'] 
    fecha_actual = session['fecha_actual']
    nom_archivo = f'datos_reba_{var4}_{fecha_actual}_{hora_actual}.pdf'
    subir_archivos(nom_archivo, output_compressed)
    registrar_resultado_evaluacion()
    
    return send_file(output_compressed, download_name=nom_archivo, as_attachment=True)

def compress_pdf(input_pdf, output_pdf):
    import PyPDF2

    # Lee el archivo PDF original
    pdf_reader = PyPDF2.PdfReader(input_pdf)
    
    # Crea un objeto PdfFileWriter para escribir el PDF comprimido
    pdf_writer = PyPDF2.PdfWriter()
    
    # Agrega cada página del PDF original al objeto PdfFileWriter
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_writer.add_page(page)
    
    # Escribe el PDF comprimido en el archivo de salida
    pdf_writer.write(output_pdf)
#-----------------------------------------------------------------------TODAS LAS RUTAS PARA RULA-------------------------
#RULA:
@app.route('/rula_guardar_cambios', methods=['POST'])
def rula_guardar_cambios():
    datos = request.get_json()
    # Extrae los nuevos valores de T.RULA GA y T.RULA GB
    nuevoGA = datos.get('nuevoGA', {})
    nuevoGB = datos.get('nuevoGB', {})

    for segundo, valor_ga in nuevoGA.items():
        df.loc[df['Segundo'] == int(segundo), 'T.RULA GA'] = int(valor_ga)

    for segundo, valor_gb in nuevoGB.items():
        df.loc[df['Segundo'] == int(segundo), 'T.RULA GB'] = int(valor_gb)

    rula_actualizar_TC(df)
    return jsonify({'success': True})

def rula_actualizar_TC(df):            
    for index, fila in df.iterrows():
        colmna_ga = fila['T.RULA GA']
        colmna_gb = fila['T.RULA GB']
        
        df.at[index, 'T.RULA GA'] = colmna_ga
        df.at[index, 'T.RULA GB'] = colmna_gb
        puntuacion_tc = eva_rula.rula_puntuacion_tabla_C(colmna_ga, colmna_gb)
        # Asigna la puntuación calculada a la fila específica y columna 'T.RULA TC'
        df.at[index, 'T.RULA TC'] = puntuacion_tc

@app.route('/rula_guardar_cambios_tc', methods=['POST'])
def rula_guardar_cambios_tc():
    datos = request.get_json()
    nuevoTC = datos.get('nuevoTC', {})    

    for segundo, valor_tc in nuevoTC.items():
        df.loc[df['Segundo'] == int(segundo), 'T.RULA TC'] = int(valor_tc)    

    rula_actualizar_resultados(df)
    return jsonify({'success': True})

def rula_actualizar_resultados(df):        
    for index, fila in df.iterrows():
        colmna_tc = fila['T.RULA TC']        
        
        df.at[index, 'T.RULA TC'] = colmna_tc        
        puntuacion_tc = eva_rula.rula_resultado(colmna_tc)

        df.at[index, 'T.RULA RESULTADOS'] = puntuacion_tc


@app.route('/resultados_rula', methods=['GET', 'POST'])
@requiere_user
def resultados_rula():    
    usuario = obtener_dato_user()
    session
    global df, image_directory        
    #bucket = storage.bucket()

    # Obtener los datos del DataFrame
    resultados_df = df[['Segundo', 'P.RULA GA', 'P.RULA GB', 'T.RULA GA', 'T.RULA GB', 'T.RULA TC', 'T.RULA RESULTADOS', 'Fotogramas']]
    
    # Convierte los datos del DataFrame a un diccionario
    resultados_data = resultados_df.to_dict(orient='records')
    for row in resultados_data:
        row['Fotogramas'] = f"/static/imagenes_fotogramas/{row['Fotogramas'][len(image_directory)+1:]}"

    return render_template('result_rula.html', data=resultados_data, session=session, usuario=usuario)
#--------------------------------------------------------------------------------DESCARGAS EXCEL Y PDF RULA---------------------------
@app.route('/descargar_excel_rula', methods=['GET'])
def descargar_excel_rula():
    global df
    var1 = obtener_nom_user()
    var2 = session['metodo_evaluacion']
    var3 = session['npuesto']
    var4 = session['nom_trabajador']
    var5 = f"Evaluador: {var1} / Método: {var2} / Trabajador: {var4} / Área: {var3}"
    print(df.head())
    #Verifica que df esté disponible y tenga datos
    if df.empty:
        return jsonify({'error': 'No hay datos para descargar'})

    df_rula = df[['Segundo', 'P.RULA GA', 'P.RULA GB', 'T.RULA GA', 'T.RULA GB', 'T.RULA TC', 'T.RULA RESULTADOS', 'Fotogramas']]
    
    # Crear la lista de datos
    datos = [var5]
    # Asegurar que 'datos' tenga la misma longitud que el DataFrame
    if len(datos) < len(df_rula):
        datos += [' '] * (len(df_rula) - len(datos))
    elif len(df_rula) < len(datos):
        datos = datos[:len(df_rula)]

    df_rula['Datos'] = datos
    # Reordenar las columnas para que 'Datos' esté antes que 'Segundo'
    df_rula = df_rula[['Datos', 'Segundo', 'P.RULA GA', 'P.RULA GB', 'T.RULA GA', 'T.RULA GB', 'T.RULA TC', 'T.RULA RESULTADOS', 'Fotogramas']]

    # Crea un objeto BytesIO para almacenar el archivo Excel
    output = io.BytesIO()

    # Utiliza el escritor de Pandas para escribir el DataFrame en BytesIO
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_rula.to_excel(writer, sheet_name='Resultados_RULA', index=False)

    output.seek(0)

    hora_actual = session['hora_actual'] 
    fecha_actual = session['fecha_actual']
    nom_archivo = f'datos_rula_{var4}_{fecha_actual}_{hora_actual}.xlsx'
    subir_archivos(nom_archivo, output)
    registrar_resultado_evaluacion()

    # Devuelve el archivo Excel al cliente
    return send_file(output, download_name=nom_archivo, as_attachment=True)

@app.route('/descargar_pdf_rula', methods=['GET'])
def descargar_pdf_rula():
    global df
    var1 = obtener_nom_user()
    var2 = session['metodo_evaluacion']
    var3 = session['npuesto']
    var4 = session['nom_trabajador']
    var5 = f"{var1}  Método: {var2}"
    var6 = f"{var4}  Área: {var3}"
    if df.empty:
        return jsonify({'error': 'No hay datos para descargar'})

    df_rula = df[['Segundo', 'P.RULA GA', 'P.RULA GB', 'T.RULA GA', 'T.RULA GB', 'T.RULA TC', 'T.RULA RESULTADOS', 'Fotogramas']]
    # Crear un objeto BytesIO para almacenar el archivo Excel
    output = io.BytesIO()
    # Crear un documento PDF
    pdf = canvas.Canvas(output, pagesize=letter)
    # Configurar el formato del texto en el PDF
    pdf.setFont("Helvetica-Bold", 8)

    # Configuración de las dimensiones de la página
    page_width, page_height = letter
    # Configurar posición y formato para el encabezado de la tabla
    col_width = 50
    row_height = 20
    x_position = 50
    y_position = page_height - 50
    # Número máximo de filas por página
    max_rows_per_page = 7

    # Agregar datos adicionales centrados en la parte superior del PDF
    additional_data = {
        'Evaluador': var5,        
        'Trabajador': var6
    }
    # Calcular la posición central horizontal
    center_x = page_width / 2    

    # Dibujar datos adicionales centrados
    for label, value in additional_data.items():
        pdf.drawString(center_x - pdf.stringWidth(value, "Helvetica", 8) / 2, y_position, f"{label}: {value}")
        pdf.setFont("Helvetica-Bold", 8)
        y_position -= row_height

    # Ajustar la posición vertical para las columnas
    y_position -= row_height

    # Procesar el encabezado de la tabla (columnas)
    header_row = df_rula.columns.values.astype(str)
    for col_index, col_name in enumerate(header_row):
        if col_name == 'T.RULA RESULTADOS':
            col_width = 130  # Ajusta el ancho de la columna 'T.RULA RESULTADOS'
        else:
            col_width = 50  # Ancho predeterminado para otras columnas
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(x_position, y_position, col_name)
        x_position += col_width

    # Restablecer la posición vertical y horizontal
    y_position -= row_height
    x_position = 50
    pdf.setFont("Helvetica", 8)
    # Iterar sobre las filas y agregar páginas según sea necesario
    for index, row in enumerate(df_rula.values):
        if index % max_rows_per_page == 0 and index != 0:
            # Agregar una nueva página al PDF
            pdf.showPage()
            # Restablecer la posición vertical y horizontal para la próxima página
            y_position = page_height - 50
            x_position = 50
            pdf.setFont("Helvetica", 8)
        # Procesar las filas de datos        
        for index, item in enumerate(row):
            if df_rula.columns[index] == 'Fotogramas':
                # Obtener el valor de la columna 'Fotogramas'
                image_value = item
                # Asegurar que la ruta apunte a un archivo, no a un directorio
                if os.path.isfile(image_value):                    
                    # Usar PIL para cargar la imagen
                    img = Image.open(image_value)
                    # Volver al principio del búfer de la imagen
                    img.seek(0)
                    # Ajustar la posición vertical para la próxima imagen
                    y_position -= 75
                    # Dibujar la imagen en el PDF
                    pdf.drawInlineImage(img, (x_position + 80), (y_position), width=67, height=85)                    
                else:
                    # Manejar el caso en que la ruta no sea un archivo válido
                    print(f"La ruta {image_value} no es un archivo válido.")
            elif df_rula.columns[index] == 'T.RULA RESULTADOS':
                # Convertir la lista de tuplas a una cadena
                text_value = ', '.join(', '.join(str(val) for val in tupla) for tupla in item) if isinstance(item, list) else str(item)
                # Dividir el texto en varias líneas
                max_line_length = 30  # Ajusta la longitud máxima de la línea
                lines = [text_value[i:i+max_line_length] for i in range(0, len(text_value), max_line_length)]                
                #col_width = 120
                line_position = y_position                            
                # Dibujar las líneas de texto en posiciones separadas
                for line_index, line in enumerate(lines):
                    pdf.drawString(x_position, line_position, line)                
                    line_position -= (row_height-7)                    
            else:
                pdf.drawString(x_position, y_position, str(item))
            x_position += col_width

        # Restablecer la posición vertical y horizontal para la próxima fila
        y_position -= row_height
        x_position = 50
    # Guardar el PDF
    pdf.save()
    # Comprimir el PDF generado
    output_compressed = io.BytesIO()
    compress_pdf(output, output_compressed)
    # Devolver el archivo PDF al cliente
    output_compressed.seek(0)

    hora_actual = session['hora_actual'] 
    fecha_actual = session['fecha_actual']
    nom_archivo = f'datos_rula_{var4}_{fecha_actual}_{hora_actual}.pdf'
    subir_archivos(nom_archivo, output_compressed)
    registrar_resultado_evaluacion()
    
    return send_file(output_compressed, download_name=nom_archivo, as_attachment=True)

#-----------------------------------------------------------------LÓGICA PARA EL PROCESAMIENTO DE VIDEO---------------------
def generate_frames(video_path):
    #cap = cv2.VideoCapture(0) En el caso de usar la camara
    global stop_processing, df, image_directory
    cap = cv2.VideoCapture(video_path)
    eva_reba = evareba.evaluacion_reba()
    eva_rula = evarula.evaluacion_rula()
    detector = pm.pose_detector()
    count = 0

    # Directorio para almacenar las imágenes
    image_directory = os.path.join(app.root_path, 'static', 'imagenes_fotogramas')
    os.makedirs(image_directory, exist_ok=True)        

    # Colores.
    blue = (255, 127, 0)
    red = (50, 50, 255)
    green = (127, 255, 0)
    dark_blue = (127, 20, 0)
    light_green = (127, 233, 100)
    yellow = (0, 255, 255)
    pink = (255, 0, 255)

    #Escribir el video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #con detecciones
    video_output = cv2.VideoWriter('Videos-Detecciones/Salida-Video_prueba.mp4', fourcc, 1, frame_size)
    #sin detecciones
    video_output_nd = cv2.VideoWriter('Videos-Detecciones/Salida-Video_pruebasd.mp4', fourcc, 1, frame_size)

    # Inicializa el tiempo actual
    start_time = time.time()    
    current_second = 0
    # Crea una lista para almacenar todos los ángulos
    all_detected_angles = []   

    while True:    
        success, img = cap.read() #img con detecciones
        success1, img1 = cap.read() #img sin detecciones
        if (not success) or (not success1) :
            # Si no se puede leer más imágenes, sale del bucle
            break

        #Implementacion de Mediapipe y Opencv       
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, draw=False)
        
        #Valida que solo detecte los puntos claves visibles
        if lmList is not None and len(lmList) > max(16, 14, 12, 24, 23, 11, 25, 26, 28):  # Verifica si lmList no es None y contiene suficientes puntos clave
            #Dicionario y listas para almacenar
            detected_angles = {"Segundo": current_second}
            comparacion = []
            modi_antebra = {}
            
            # Left elbow
            detected_angles["Codo Izquierdo"] = detector.findAngle(img, 11, 13, 15)

            # Right elbow
            detected_angles["Codo Derecho"] = detector.findAngle(img, 12, 14, 16)

            # Left shoulder
            detected_angles["Hombro Izquierdo"] = detector.findAngle(img, 13, 11, 23)

            # Right shoulder
            detected_angles["Hombro Derecho"] = detector.findAngle(img, 14, 12, 24)
            rs = detector.findAngle(img, 14, 12, 24)

            # Left hip
            detected_angles["Cadera Izquierda"] = detector.findAngle(img, 11, 23, 25)

            # Right hip
            detected_angles["Cadera Derecha"] = detector.findAngle(img, 12, 24, 26)
            fdj = detector.findAngle(img, 12, 24, 26)

            # Left knee
            detected_angles["Rodilla Izquierda"] = detector.findAngle(img, 23, 25, 27)

            # Right knee
            detected_angles["Rodilla Derecha"] = detector.findAngle(img, 24, 26, 28)

            # Left wrist
            detected_angles["Muñeca Izquierda"] = detector.findAngle(img, 13, 15, 19)

            # Right wrist
            detected_angles["Muñeca Derecha"] = detector.findAngle(img, 14, 16, 20)

            #antebrazo - angulo line media, a un lado del cuerpo - derecho
            modi_antebra["Modiantebrazo Derecho"] = detector.findAngle(img, 16, 12, 11, False)
            
            #antebrazo - angulo line media, a un lado del cuerpo - izquierdo
            modi_antebra["Modiantebrazo Izquierdo"] = detector.findAngle(img, 15, 11, 12, False)
            
            # cuello
            #Cordenadas izquierda
            shoulder_left_coords = lmList[11][1:3]  # [1:3] obtiene las coordenadas x e y        
            shoulder_left_x, shoulder_left_y = shoulder_left_coords
            
            ear_left_coords = lmList[7][1:3]  # [1:3] obtiene las coordenadas x e y       
            ear_left_x, ear_left_y = ear_left_coords

            hip_left_coords = lmList[23][1:3]  # [1:3] obtiene las coordenadas x e y       
            hip_left_x, hip_left_y = hip_left_coords
            
            #Cordenadas Derecha
            shoulder_right_coords = lmList[12][1:3]  # [1:3] obtiene las coordenadas x e y        
            shoulder_right_x, shoulder_right_y = shoulder_right_coords
            
            ear_right_coords = lmList[8][1:3]  # [1:3] obtiene las coordenadas x e y       
            ear_right_x, ear_right_y = ear_right_coords

            hip_right_coords = lmList[24][1:3]  # [1:3] obtiene las coordenadas x e y       
            hip_right_x, hip_right_y = hip_right_coords

            # Calculate angles.        
            if (fdj is None) and (rs is None):
                neck_inclination = detector.findAngle3(shoulder_left_x, shoulder_left_y, ear_left_x, ear_left_y)            
                torso_inclination = detector.findAngle3(hip_left_x, hip_left_y, shoulder_left_x, shoulder_left_y)
                if neck_inclination is not None and torso_inclination is not None:
                    cv2.putText(img, str(int(neck_inclination)), (shoulder_left_x-30, shoulder_left_y-30), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 127, 0), 2)            
                    cv2.putText(img, str(int(torso_inclination)), (hip_left_x-30, hip_left_y-30), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 127, 0), 2)
                    if neck_inclination < 40 and torso_inclination < 10:                       
                        # Join landmarks.
                        cv2.line(img, (shoulder_left_x, shoulder_left_y), (ear_left_x, ear_left_y), green, 4)
                        cv2.line(img, (shoulder_left_x, shoulder_left_y), (shoulder_left_x, shoulder_left_y - 50), green, 4)
                        cv2.line(img, (hip_left_x, hip_left_y), (shoulder_left_x, shoulder_left_y), green, 4)
                        cv2.line(img, (hip_left_x, hip_left_y), (hip_left_x, hip_left_y - 50), green, 4)

                    else:                        
                        # Join landmarks.
                        cv2.line(img, (shoulder_left_x, shoulder_left_y), (ear_left_x, ear_left_y), red, 4)
                        cv2.line(img, (shoulder_left_x, shoulder_left_y), (shoulder_left_x, shoulder_left_y - 50), red, 4)
                        cv2.line(img, (hip_left_x, hip_left_y), (shoulder_left_x, shoulder_left_y), red, 4)
                        cv2.line(img, (hip_left_x, hip_left_y), (hip_left_x, hip_left_y - 50), red, 4)
            else:
                neck_inclination = detector.findAngle3(shoulder_right_x, shoulder_right_y, ear_right_x, ear_right_y)
                torso_inclination = detector.findAngle3(hip_right_x, hip_right_y, shoulder_right_x, shoulder_right_y)
                if neck_inclination is not None and torso_inclination is not None:
                    cv2.putText(img, str(int(neck_inclination)), (shoulder_right_x + 10, shoulder_right_y), cv2.FONT_HERSHEY_PLAIN, 0.9, (0, 255, 255), 2)
                    cv2.putText(img, str(int(torso_inclination)), (hip_right_x-30, hip_right_y-30), cv2.FONT_HERSHEY_PLAIN, 0.9, (0, 255, 255), 2)
                    if neck_inclination < 40 and torso_inclination < 10:               
                        # Join landmarks.
                        cv2.line(img, (shoulder_right_x, shoulder_right_y), (ear_right_x, ear_right_y), green, 4)
                        cv2.line(img, (shoulder_right_x, shoulder_right_y), (shoulder_right_x, shoulder_right_y - 50), green, 4)
                        cv2.line(img, (hip_right_x, hip_right_y), (shoulder_right_x, shoulder_right_y), green, 4)
                        cv2.line(img, (hip_right_x, hip_right_y), (hip_right_x, hip_right_y - 50), green, 4)

                    else:                        
                        # Join landmarks.
                        cv2.line(img, (shoulder_right_x, shoulder_right_y), (ear_right_x, ear_right_y), red, 4)
                        cv2.line(img, (shoulder_right_x, shoulder_right_y), (shoulder_right_x, shoulder_right_y - 50), red, 4)
                        cv2.line(img, (hip_right_x, hip_right_y), (shoulder_right_x, shoulder_right_y), red, 4)
                        cv2.line(img, (hip_right_x, hip_right_y), (hip_right_x, hip_right_y - 50), red, 4)
            
            detected_angles["Inclinacion del cuello"] = neck_inclination
            detected_angles["Inclinacion del torso"] = torso_inclination

            #Añade más ángulos de ser necesario

            comparacion = eva_reba.diferencia_dist(lmList)

            # Verifica si ha pasado un segundo      
            current_time = time.time()
            elapsed_time = current_time - start_time
            #count += 1
            im1 = cv2.resize(img1, frame_size)
            im = cv2.resize(img, frame_size)
            
            #Lógica para guardar las detecciones y calculos cada segundo
            if elapsed_time >= 1.0:
                count += 1
                # Almacena las evaluaciones REBA segun los ángulos detectados en la lista            
                detected_angles["P.REBA GA"] = eva_reba.evaluar_postura_REBA(detected_angles, comparacion)
                detected_angles["P.REBA GB"] = eva_reba.evaluar_postura_REBAB(detected_angles)
                detected_angles["T.REBA GA"] = eva_reba.obtener_puntuacion_ga(detected_angles["P.REBA GA"])
                detected_angles["T.REBA GB"] = eva_reba.obtener_puntuacion_gb(detected_angles["P.REBA GB"])
                detected_angles["T.REBA TC"] = eva_reba.obtener_puntuacion_tc(detected_angles["T.REBA GA"], detected_angles["T.REBA GB"])
                detected_angles["T.REBA RESULTADOS"] = eva_reba.obtener_resultado(detected_angles["T.REBA TC"])
                # Almacena las evaluaciones RULA segun los ángulos detectados en la lista            
                detected_angles["P.RULA GA"] = eva_rula.rula_grupo_A(detected_angles, modi_antebra)
                detected_angles["P.RULA GB"] = eva_rula.rula_grupo_B(detected_angles, comparacion)
                detected_angles["T.RULA GA"] = eva_rula.rula_puntuacion_gA(detected_angles["P.RULA GA"])
                detected_angles["T.RULA GB"] = eva_rula.rula_puntuacion_gB(detected_angles["P.RULA GB"])
                detected_angles["T.RULA TC"] = eva_rula.rula_puntuacion_tabla_C(detected_angles["T.RULA GA"], detected_angles["T.RULA GB"])
                detected_angles["T.RULA RESULTADOS"] = eva_rula.rula_resultado(detected_angles["T.RULA TC"])
                
                # Guarda la imagen en un archivo en el directorio                
                img_filename = f"{image_directory}/frame_{count}.png"
                cv2.imwrite(img_filename, img)
                
                # Almacena la ruta del archivo de imagen en el diccionario
                detected_angles["Fotogramas"] = img_filename
                all_detected_angles.append(detected_angles.copy())
                # Incrementa el contador de segundos            
                current_second += 1
                # Reinicia el temporizador
                start_time = current_time
                video_output.write(im)
                video_output_nd.write(im1)
                            
        cv2.waitKey(1) # Press 'ESC' for exiting video        
            #if k == 27:
             #   break
        
        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        #Lógica para finalizar el bucle si presionan Detener video
        if stop_processing:
            break

    cap.release()   
                
    # Reordena las columnas para tener "Segundo" al principio, seguido de los ángulos
    column_order = ["Segundo"] + [f"{angle_name}" for angle_name in all_detected_angles[0].keys() if angle_name != "Segundo"]
    df = pd.DataFrame(all_detected_angles, columns=column_order)    

    # Imprime el DataFrame en la terminal
    print(df)

    # Especifica la ruta de salida del archivo Excel
    excel_path = "Archivos-Excel/VIDEO_prueba.xlsx"

    # Guarda el DataFrame en un archivo Excel
    df.to_excel(excel_path, index=False)
    # Restablece la variable de control después de detener el procesamiento
    stop_processing = False

#Muestra el video
@app.route('/video_feed')
def video_feed():
    video_path = request.args.get('path', '')
    return Response(generate_frames(video_path),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#Corre la app
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)

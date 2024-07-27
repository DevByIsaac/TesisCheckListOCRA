'''from flask import request, jsonify
from analisis_video import draw_keypoints_and_angles
import os

def init_routes(app):
    @app.route('/upload', methods=['POST'])
    def upload_video():
        if 'video' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['video']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            video_path = os.path.join('uploaded_videos', file.filename)
            file.save(video_path)
            output_frame_folder, output_video_path, json_path = draw_keypoints_and_angles(video_path)
            return jsonify({
                'frames_path': output_frame_folder,
                'output_video_path': output_video_path,
                'json_path': json_path
            })
'''
from flask import render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app import app, db
from models import User
from flask import Flask, jsonify, send_from_directory
from analisis_video import draw_keypoints_and_angles
import os

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#----------------------------------------------------------------------RUTA DE LOGIN--------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#----------------------------------------------------------------------RUTA DE REGISTRO--------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully')
        return redirect(url_for('login'))
    return render_template('register.html')
#----------------------------------------------------------------------DESCARGAR VIDEO--------------------------------------------------------------------
@app.route('/subir_video', methods=['GET', 'POST'])
def subir_video():
    return render_template("subir_video.html")

#----------------------------------------------------------------------RUTA ANALISIS DE VIDEO--------------------------------------------------------------------
@app.route('/analyze_video', methods=['POST'])
def analyze_video():
    video_file = request.files['video']
    video_path = os.path.join('videos', video_file.filename)
    video_file.save(video_path)

    output_folder = 'output_frames'
    output_video_folder = 'output_videos'
    json_folder = 'json_results'

    draw_keypoints_and_angles(video_path, output_folder, output_video_folder, json_folder)

    return jsonify({"message": "Video analizado con éxito!"})

@app.route('/output_videos/<path:filename>')
def download_output_video(filename):
    return send_from_directory('output_videos', filename)

@app.route('/json_results/<path:filename>')
def download_json_result(filename):
    return send_from_directory('json_results', filename)

if __name__ == '__main__':
    app.run(debug=True)
#----------------------------------------------------------------------SUBIR VIDEO--------------------------------------------------------------------

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('upload.html')

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return render_template('upload.html', error='No se seleccionó ningún archivo.')

    file = request.files['video']
    if file.filename == '':
        return render_template('upload.html', error='No se seleccionó ningún archivo.')

    if file and file.filename.endswith('.mp4'):
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        return render_template('upload.html', success='Video subido exitosamente.')

    return render_template('upload.html', error='Solo se permiten archivos MP4.')
#----------------------------------------------------------------------DESCARGAR VIDEO--------------------------------------------------------------------

@bp.route('/download')
def download_file():
    video = request.args.get('video')
    if not video:
        return render_template('download.html', error='No se seleccionó ningún video.')

    # Verifica si el video y los archivos JSON y Excel existen
    video_path = os.path.join('uploads', video)
    json_path = os.path.join('static/resultados', video.replace('.mp4', '_data.json'))
    excel_path = os.path.join('static/resultados', video.replace('.mp4', '_results.xlsx'))

    if not os.path.isfile(video_path) and not os.path.isfile(json_path) and not os.path.isfile(excel_path):
        return render_template('download.html', error='El archivo no existe.')

    # Envía los archivos como una descarga en lugar de enviar un solo archivo.
    return render_template('download.html', success='Archivos disponibles para descargar.')
#----------------------------------------------------------------------DESCARGAR ARCHIVOS JSON--------------------------------------------------------------------

@bp.route('/download/<filename>')
def download(filename):
    return send_from_directory('static/resultados', filename, as_attachment=True)

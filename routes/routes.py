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

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

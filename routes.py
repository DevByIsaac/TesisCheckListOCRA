from flask import request, jsonify
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

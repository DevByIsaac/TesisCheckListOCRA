import cv2
import numpy as np

def calculate_angle(a, b, c):
    a = np.array(a)  # Primer punto
    b = np.array(b)  # Segundo punto (punto común)
    c = np.array(c)  # Tercer punto

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

def load_videos(video_folder):
    video_files = []
    for root, _, files in os.walk(video_folder):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mov')):
                video_files.append(os.path.join(root, file))
    return video_files

def extract_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error al abrir el video: {video_path}")
        return

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_path = os.path.join(output_folder, f'frame_{frame_count:04d}.jpg')
        cv2.imwrite(frame_path, frame)
        frame_count += 1

    cap.release()

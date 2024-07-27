import cv2
import numpy as np
import pandas as pd
import mediapipe as mp
import os
import datetime
import json

video_dir = 'C:\\Tesis\\TestErgo\\muestra'

def load_videos(video_dir):
    videos = []
    for filename in os.listdir(video_dir):
        if filename.endswith(".mp4"):
            videos.append(os.path.join(video_dir, filename))
    return videos
#----------------------------------------VALIDACION PARA SABER SI EL VIDEO ES DE UNA PERSONA CON HAAR CASCADES---------------------------------------
def detect_person(video_path):
    # Cargar el clasificador de cascada para la detección de personas
    person_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"No se puede abrir el video: {video_path}")

    detected_person = False
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bodies = person_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if len(bodies) > 0:
            detected_person = True
            break

    cap.release()
    return detected_person

def process_video(video_path):
    if not detect_person(video_path):
        # Aquí se levantaría la alerta
        print("Es posible que este video no sea de una persona haciendo trabajo repetitivo.")
        # Opcionalmente, puedes evitar que el video se procese y salir de la función
        return
#----------------------------------------------------------------------EXTRAER FRAMES--------------------------------------------------------------------
def extract_frames(video_path, interval=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % interval == 0:
            frames.append(frame)
        count += 1
    cap.release()
    return frames

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c, d=None):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    if d is not None:
        d = np.array(d)
        radians = np.arctan2(d[1] - c[1], d[0] - c[0]) - np.arctan2(b[1] - a[1], b[0] - a[0])
    else:
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360.0 - angle
    return angle

def detect_keypoints(video_path):
    cap = cv2.VideoCapture(video_path)
    pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
    keypoints_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        if results.pose_landmarks:
            keypoints = [(lm.x, lm.y, lm.z) for lm in results.pose_landmarks.landmark]
            keypoints_list.append(keypoints)
        else:
            keypoints_list.append([])
    cap.release()
    pose.close()
    return keypoints_list

def analyze_keypoints(video_path):
    keypoints_list = detect_keypoints(video_path)
    fps = None
    analysis_results = []
    for frame_idx, keypoints in enumerate(keypoints_list):
        second = frame_idx // fps if fps else 0
        if not keypoints:
            analysis_results.append({
                'segundo': second,
                'frame': frame_idx,
                'video_name': None,
                'angulo_hombro_izquierdo': None,
                'angulo_del_hombro_derecho': None,
                'angulo_codo_izquierdo': None,
                'angulo_codo_derecho': None,
                'angulo_de_muneca_izquierda': None,
                'angulo_de_muneca_derecha': None,
                'angulo_mano_izquierdo': None,
                'angulo_mano_derecho': None,
                'posicion_hombro_izquierdo': None,
                'posicion_hombro_derecho': None,
                'posicion_codo_izquierdo': None,
                'posicion_codo_derecho': None,
                'posicion_muneca_izquierda': None,
                'posicion_muneca_derecha': None,
                'posicion_mano_izquierda': None,
                'posicion_mano_derecha': None,
                'keypoints': []
            })
            continue

        left_shoulder = keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        left_elbow = keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        left_wrist = keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value]
        left_hand = keypoints[mp_pose.PoseLandmark.LEFT_INDEX.value]
        right_shoulder = keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        right_elbow = keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        right_wrist = keypoints[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        right_hand = keypoints[mp_pose.PoseLandmark.RIGHT_INDEX.value]

        left_shoulder_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        left_elbow_angle = calculate_angle(left_elbow, left_wrist, left_hand)
        left_wrist_angle = calculate_angle(left_elbow, left_wrist, left_hand)
        left_hand_angle = calculate_angle(left_elbow, left_wrist, left_hand)

        right_shoulder_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        right_elbow_angle = calculate_angle(right_elbow, right_wrist, right_hand)
        right_wrist_angle = calculate_angle(right_elbow, right_wrist, right_hand)
        right_hand_angle = calculate_angle(right_elbow, right_wrist, right_hand)

        if fps is None:
            cap = cv2.VideoCapture(video_path)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            cap.release()

        analysis_results.append({
            'segundo': second,
            'frame': frame_idx,
            'analisis_video': video_path,
            'angulo_hombro_izquierdo': left_shoulder_angle,
            'angulo_del_hombro_derecho': right_shoulder_angle,
            'angulo_codo_izquierdo': left_elbow_angle,
            'angulo_codo_derecho': right_elbow_angle,
            'angulo_de_muneca_izquierda': left_wrist_angle,
            'angulo_de_muneca_derecha': right_wrist_angle,
            'angulo_mano_izquierdo': left_hand_angle,
            'angulo_mano_derecho': right_hand_angle,
            'posicion_hombro_izquierdo': left_shoulder,
            'posicion_hombro_derecho': right_shoulder,
            'posicion_codo_izquierdo': left_elbow,
            'posicion_codo_derecho': right_elbow,
            'posicion_muneca_izquierda': left_wrist,
            'posicion_muneca_derecha': right_wrist,
            'posicion_mano_izquierda': left_hand,
            'posicion_mano_derecha': right_hand,
            'keypoints': keypoints
        })

    return analysis_results, fps

def draw_keypoints_and_angles(video_path, output_folder, output_video_folder, json_folder):
    analysis_results, fps = analyze_keypoints(video_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error al abrir el video: {video_path}")
        return
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_frame_folder = os.path.join(output_folder, video_name)
    output_video_name = f"{video_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    output_video_path = os.path.join(output_video_folder, output_video_name)
    json_filename = f"{video_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    json_path = os.path.join(json_folder, json_filename)

    if not os.path.exists(video_frame_folder):
        os.makedirs(video_frame_folder)
    if not os.path.exists(output_video_folder):
        os.makedirs(output_video_folder)
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0
    for i in range(len(analysis_results)):
        ret, frame = cap.read()
        if not ret:
            break

        keypoints = analysis_results[i]['keypoints']
        left_shoulder_angle = analysis_results[i]['angulo_hombro_izquierdo']
        right_shoulder_angle = analysis_results[i]['angulo_del_hombro_derecho']
        left_elbow_angle = analysis_results[i]['angulo_codo_izquierdo']
        right_elbow_angle = analysis_results[i]['angulo_codo_derecho']
        left_wrist_angle = analysis_results[i]['angulo_de_muneca_izquierda']
        right_wrist_angle = analysis_results[i]['angulo_de_muneca_derecha']
        left_hand_angle = analysis_results[i]['angulo_mano_izquierdo']
        right_hand_angle = analysis_results[i]['angulo_mano_derecho']

        for i, keypoint in enumerate(keypoints):
            x, y, z = keypoint
            x, y = int(x * frame_width), int(y * frame_height)
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        
        for (lm1, lm2) in [((mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
                            (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW))]:
            x1, y1, _ = keypoints[lm1.value]
            x2, y2, _ = keypoints[lm2.value]
            x1, y1 = int(x1 * frame_width), int(y1 * frame_height)
            x2, y2 = int(x2 * frame_width), int(y2 * frame_height)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(frame, f'{left_shoulder_angle:.2f}' if lm1 == mp_pose.PoseLandmark.LEFT_SHOULDER else f'{right_shoulder_angle:.2f}',
                        (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)

        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()

    with open(json_path, 'w') as f:
        json.dump(analysis_results, f, indent=4)

    print(f"Video procesado guardado en: {output_video_path}")
    print(f"Datos analizados guardados en: {json_path}")
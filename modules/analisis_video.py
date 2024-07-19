import cv2
import numpy as np
import mediapipe as mp
import os
import datetime
import json
from config_postgres import OUTPUT_FOLDER, OUTPUT_VIDEO_FOLDER, JSON_FOLDER
from utils import load_videos, extract_frames, calculate_angle

# Inicializar MediaPipe para detección de puntos clave
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

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
            keypoints_list.append([])  # Agregar una lista vacía si no se detectan keypoints

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

        # Extraer puntos clave izquierdos
        left_shoulder = keypoints[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        left_elbow = keypoints[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        left_wrist = keypoints[mp_pose.PoseLandmark.LEFT_WRIST.value]
        left_hand = keypoints[mp_pose.PoseLandmark.LEFT_INDEX.value]

        # Extraer puntos clave derechos
        right_shoulder = keypoints[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        right_elbow = keypoints[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        right_wrist = keypoints[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        right_hand = keypoints[mp_pose.PoseLandmark.RIGHT_INDEX.value]

        # Calcular ángulos izquierdos
        left_shoulder_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        left_elbow_angle = calculate_angle(left_elbow, left_wrist, left_hand)
        left_wrist_angle = calculate_angle(left_elbow, left_wrist, left_hand)
        left_hand_angle = calculate_angle(left_elbow, left_wrist, left_hand)

        # Calcular ángulos derechos
        right_shoulder_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        right_elbow_angle = calculate_angle(right_elbow, right_wrist, right_hand)
        right_wrist_angle = calculate_angle(right_elbow, right_wrist, right_hand)
        right_hand_angle = calculate_angle(right_elbow, right_wrist, right_hand)

        # Si no se ha establecido aún el FPS, se establece ahora
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

def draw_keypoints_and_angles(video_path):
    analysis_results, fps = analyze_keypoints(video_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error al abrir el video: {video_path}")
        return
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_frame_folder = os.path.join(OUTPUT_FOLDER, video_name)
    output_video_name = f"{video_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    output_video_path = os.path.join(OUTPUT_VIDEO_FOLDER, output_video_name)
    json_filename = f"{video_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    json_path = os.path.join(JSON_FOLDER, json_filename)

    # Crear carpetas si no existen
    if not os.path.exists(video_frame_folder):
        os.makedirs(video_frame_folder)
    if not os.path.exists(OUTPUT_VIDEO_FOLDER):
        os.makedirs(OUTPUT_VIDEO_FOLDER)
    if not os.path.exists(JSON_FOLDER):
        os.makedirs(JSON_FOLDER)

    # Crear el video marcado
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

        if keypoints:
            for keypoint in keypoints:
                x, y, _ = int(keypoint[0] * frame.shape[1]), int(keypoint[1] * frame.shape[0]), keypoint[2]
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        
        # Mostrar los ángulos en el frame
        if left_shoulder_angle is not None:
            cv2.putText(frame, f'Angulo Hombro Izq: {left_shoulder_angle:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        if right_shoulder_angle is not None:
            cv2.putText(frame, f'Angulo Hombro Der: {right_shoulder_angle:.2f}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        if left_elbow_angle is not None:
            cv2.putText(frame, f'Angulo Codo Izq: {left_elbow_angle:.2f}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        if right_elbow_angle is not None:
            cv2.putText(frame, f'Angulo Codo Der: {right_elbow_angle:.2f}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        if left_wrist_angle is not None:
            cv2.putText(frame, f'Angulo Muneca Izq: {left_wrist_angle:.2f}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        if right_wrist_angle is not None:
            cv2.putText(frame, f'Angulo Muneca Der: {right_wrist_angle:.2f}', (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        if left_hand_angle is not None:
            cv2.putText(frame, f'Angulo Mano Izq: {left_hand_angle:.2f}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        if right_hand_angle is not None:
            cv2.putText(frame, f'Angulo Mano Der: {right_hand_angle:.2f}', (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        frame_path = os.path.join(video_frame_folder, f'frame_{frame_count:04d}.jpg')
        cv2.imwrite(frame_path, frame)
        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()

    with open(json_path, 'w') as json_file:
        json.dump(analysis_results, json_file, indent=4)

    return video_frame_folder, output_video_path, json_path

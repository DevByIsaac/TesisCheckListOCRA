import cv2
import mediapipe as mp
import math

class pose_detector():
    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        h, w, c = img.shape
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)                
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList    

    # Calcular angulo version3.
    def findAngle3(self, x1, y1, x2, y2):    
        # Verifica si el denominador es cero
        if y1 == 0 or (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1) == 0:            
            return None  # Puedes devolver un valor especial según tus necesidades
        else:
            theta = math.acos((y2 - y1) * (-y1) / (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
            degree = int(180 / math.pi) * theta
            return degree

    #Calcula y dibuja los angulos
    def findAngle(self, img, p1, p2, p3, draw=True):
    # Get the landmarks
        if self.results.pose_landmarks:
            lm_list = self.results.pose_landmarks.landmark

            if all(lm_list[i].visibility >= 0.4 for i in [p1, p2, p3]):
                points = [(int(lm_list[i].x * img.shape[1]), int(lm_list[i].y * img.shape[0])) for i in [p1, p2, p3]]                
                
                # Calculate vectors
                v1 = (points[0][0] - points[1][0], points[0][1] - points[1][1])
                v2 = (points[2][0] - points[1][0], points[2][1] - points[1][1])

                # Calculate dot product and magnitudes
                dot_product = v1[0] * v2[0] + v1[1] * v2[1]
                magnitude_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
                magnitude_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

                if magnitude_v1 != 0 and magnitude_v2 != 0:
                    # Verificar que el argumento esté dentro del rango válido
                    if -1 <= (dot_product / (magnitude_v1 * magnitude_v2)) <= 1:                
                        # Calculate angle in radians
                        theta = math.acos(dot_product / (magnitude_v1 * magnitude_v2))
                        # Convert angle to degrees
                        angle1 = math.degrees(theta)

                        # Calculate the Angle
                        angle = math.degrees(math.atan2(points[2][1] - points[1][1], points[2][0] - points[1][0]) -
                                            math.atan2(points[0][1] - points[1][1], points[0][0] - points[1][0]))

                        if draw:
                            cv2.line(img, points[0], points[1], (255, 255, 255), 2)
                            cv2.line(img, points[2], points[1], (255, 255, 255), 2)
                            cv2.circle(img, points[0], 5, (0, 0, 255), cv2.FILLED)                    
                            cv2.circle(img, points[1], 5, (0, 0, 255), cv2.FILLED)                    
                            cv2.circle(img, points[2], 5, (0, 0, 255), cv2.FILLED)                    
                            cv2.putText(img, str(int(angle1)), (points[1][0] + 10, points[1][1]), cv2.FONT_HERSHEY_PLAIN, 0.9,
                                        (0, 255, 0), 2)

                        return angle1
                    return None
                return None
        return None


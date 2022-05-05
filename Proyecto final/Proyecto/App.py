from datetime import datetime
from flask import render_template
from flask import Flask, render_template, Response, jsonify
import mediapipe as mp 
import cv2
import re

app = Flask(__name__)


camara = cv2.VideoCapture(0)
#Variables necesarias libreria mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

fourcc = cv2.VideoWriter_fourcc(*'XVID')
archivo_video = None
grabando = False 

def generador_frames():    
    while True:
        ok, imagen = obtener_frame_camara()
        if not ok:
            break
        else:            
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + imagen + b"\r\n"

def obtener_frame_camara():
    #Codigo de grabacion y hands que pone los puntos
    with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
        ok, frame = camara.read()        
        if not ok:
            return False, None          
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    #hand_landmarks son las coordenadas
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0,255,255), thickness=3, circle_radius=5),
                    mp_drawing.DrawingSpec(color=(255,0,255), thickness=4, circle_radius=5))
    if grabando and archivo_video is not None:
        archivo_video.write(frame)
    _, bufer = cv2.imencode(".jpg", frame)
    imagen = bufer.tobytes()
    
    return True, imagen

@app.route('/')
def index():
    return render_template("Home.html")

#Ruta que consulta la imagen en html
@app.route("/streaming_camara")
def streaming_camara():
    return Response(generador_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



  

if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)

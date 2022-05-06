import cv2
import mediapipe as mp
import os
#Creacion de la carpeta donde se guardaran las imagenes
letra ='A'
direccion ='C:/Users/edgar/source/repos/ProyectoPython/Proyecto final/Proyecto/res'
carpeta = direccion + '/' + letra
if not os.path.exists(carpeta):
    print('Carpeta creada: ',carpeta)
    os.makedirs(carpeta)
cont = 0 #contador para las imagenes que se van a tomar
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

class_hands = mp.solutions.hands
hands = class_hands.Hands() 
dibujo = mp.solutions.drawing_utils
#Se guardan las posiciones de cada punto
while (1):
    ret,frame = cap.read()
    color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    copia = frame.copy()
    resultado = hands.process(color)
    posiciones = []
#Empieza a detectar cuando hay una o dos manos en la imagen
    if resultado.multi_hand_landmarks: 
        for mano in resultado.multi_hand_landmarks: 
            for id, lm in enumerate(mano.landmark):
                alto, ancho, c = frame.shape 
                corx, cory = int(lm.x*ancho), int(lm.y*alto)
                posiciones.append([id,corx,cory])
                dibujo.draw_landmarks(
                    frame, mano, class_hands.HAND_CONNECTIONS,
                    dibujo.DrawingSpec(color=(0,255,255), thickness=3, circle_radius=5),
                    dibujo.DrawingSpec(color=(255,0,255), thickness=4, circle_radius=5))
            if len(posiciones) != 0:
                pto_i5 = posiciones[9]
                x1, y1 = (pto_i5[1]-100),(pto_i5[2]-100)
                ancho, alto = (x1+200),(y1+200)
                x2,y2 = x1 + ancho, y1 + alto
                dedos_reg = copia[y1:y2, x1:x2]
                #Al presionar enter empieza a tomar las fotos en este caso 20
                k = cv2.waitKey(1)
                if k == 13:
                    for cont in range(0,20):#Aqui cambiamos el rango por si queremos mas o menos fotos 
                        dedos_reg = cv2.resize(dedos_reg, (400,400), interpolation=cv2.INTER_CUBIC)#Cambiamos la dimension de las imagenes, esto estaba haceindo pruebas xd
                        cv2.imwrite(carpeta+'/'+letra+'_{}.jpg'.format(cont),dedos_reg)#Se guarda con el nombre de la letra y numero de imagen
                        cont += 1
    cv2.imshow("Video",frame)
    k = cv2.waitKey(1)
    if k == 27 or cont >= 20:#Cerramos con escape o cuando ya se hayan tomado las 20 fotos
        break
cap.release()
cv2.destroyAllWindows()
print('Letra "',letra,'" capturada') 

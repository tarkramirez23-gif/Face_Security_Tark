"""
Proyecto: Reconocimiento facial y de manos en tiempo real
Librerías: OpenCV + MediaPipe

Detecta:
  - Malla facial (FaceMesh) con ~468 puntos
  - Manos (Hands) con 21 puntos por mano
  - Gesto simple: mano abierta / puño cerrado
  - FPS en pantalla
"""

import cv2
import mediapipe as mp
import time

# ---------------------------------------------------------
# Inicialización de MediaPipe
# ---------------------------------------------------------
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
)

TIP_IDS = [4, 8, 12, 16, 20]


def contar_dedos_levantados(hand_landmarks, handedness_label):
    lm = hand_landmarks.landmark
    dedos = []

    if handedness_label == "Right":
        dedos.append(lm[TIP_IDS[0]].x < lm[TIP_IDS[0] - 1].x)
    else:
        dedos.append(lm[TIP_IDS[0]].x > lm[TIP_IDS[0] - 1].x)

    for id in TIP_IDS[1:]:
        dedos.append(lm[id].y < lm[id - 2].y)

    return dedos, sum(dedos)


def clasificar_gesto(dedos_arriba, total):
    if total == 0:
        return "Es puño"
    elif total == 5:
        return "Es mano Abierta"
    elif total == 2 and dedos_arriba[1] and dedos_arriba[2]:
        return "Es paz / victoria"
    elif total == 1 and dedos_arriba[1]:
        return "Es indice"
    else:
        return f"{total} dedo(s) arriba"


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo acceder a la cámara.")
        return

    prev_time = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            print("No se pudo leer el frame de la cámara.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_results = face_mesh.process(rgb_frame)
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style(),
                )
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style(),
                )

        hand_results = hands.process(rgb_frame)
        if hand_results.multi_hand_landmarks and hand_results.multi_handedness:
            for hand_landmarks, handedness in zip(
                hand_results.multi_hand_landmarks, hand_results.multi_handedness
            ):
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style(),
                )

                label = handedness.classification[0].label
                dedos, total = contar_dedos_levantados(hand_landmarks, label)
                gesto_texto = clasificar_gesto(dedos, total)

                h, w, _ = frame.shape
                cx = int(hand_landmarks.landmark[0].x * w)
                cy = int(hand_landmarks.landmark[0].y * h)
                cv2.putText(
                    frame, gesto_texto, (cx - 50, cy + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2,
                )

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time else 0
        prev_time = curr_time
        cv2.putText(
            frame, f"FPS: {int(fps)}", (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
        )

        cv2.imshow("Face security_Tark", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
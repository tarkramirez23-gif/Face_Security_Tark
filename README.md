# Face Security Tark - Reconocimiento facial por computador

Sistema de **reconocimiento facial y de manos en tiempo real** desarrollado en Python con **OpenCV** y **MediaPipe**. Detecta la malla facial (FaceMesh), el esqueleto de las manos (Hands) y clasifica gestos simples (mano abierta, puño cerrado, señal de paz, dedo índice), mostrando además los FPS en pantalla.

Este proyecto fue desarrollado como parte de un curso de **ethical hacking / visión por computador**, usando la cámara web como fuente de video.

---

## 📋 Tabla de contenidos

- [Características](#-características)
- [Demo / Funcionamiento](#-demo--funcionamiento)
- [Requisitos previos](#-requisitos-previos)
- [Instalación paso a paso](#-instalación-paso-a-paso)
- [Uso](#-uso)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Cómo funciona el código](#-cómo-funciona-el-código)
- [Solución de problemas](#-solución-de-problemas)
- [Posibles mejoras](#-posibles-mejoras)
- [Tecnologías utilizadas](#-tecnologías-utilizadas)
- [Autor](#-autor)

---

## ✨ Características

- **Detección facial (FaceMesh):** dibuja ~468 puntos de referencia del rostro, incluyendo la malla (tesselation) y los contornos (ojos, cejas, labios, óvalo facial).
- **Detección de manos (Hands):** identifica hasta 2 manos simultáneamente, con 21 puntos de referencia por mano.
- **Clasificación de gestos:** cuenta los dedos levantados y clasifica el gesto en:
  - ✊ Puño cerrado
  - ✋ Mano abierta
  - ✌️ Paz / victoria
  - ☝️ Índice
  - Otro número de dedos levantados
- **Contador de FPS en tiempo real** para monitorear el rendimiento.
- **Distinción mano izquierda / derecha** para un conteo de dedos preciso.

---

## 🎬 Funcionamiento.

Al ejecutar el script se abre una ventana con el video de tu cámara web. Sobre la imagen se dibujan:

1. La malla facial en verde/gris sobre tu rostro.
2. El esqueleto de tu(s) mano(s) con sus 21 puntos.
3. Un texto junto a cada mano indicando el gesto detectado.
4. El contador de FPS en la esquina superior izquierda.

Presiona **`q`** o **`Esc`** para cerrar la ventana y terminar el programa.

---

## 🧰 Requisitos previos

- **Python 3.9, 3.10 o 3.11** (MediaPipe aún no tiene soporte estable para todas las versiones más recientes de Python; se recomienda evitar 3.12+ si encuentras errores de instalación).
- Una **cámara web** funcional (integrada o USB).
- **pip** actualizado.
- Sistema operativo: Windows, macOS o Linux.

---

## 🚀 Instalación paso a paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/tarkramirez23-gif/Face_Security_Tark.git
cd Face_Security_Tark
```

### 2. Crear un entorno virtual (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Verás `(venv)` al inicio de tu línea de comandos si se activó correctamente.

### 3. Instalar las dependencias

El proyecto incluye un archivo `requirements.txt` con las librerías necesarias:

```txt
opencv-python==4.9.0.80
mediapipe==0.10.14
```

Instálalas con:

```bash
pip install -r requirements.txt
```

### 4. Verificar la instalación

```bash
python -c "import cv2, mediapipe; print('OpenCV:', cv2.__version__); print('MediaPipe:', mediapipe.__version__)"
```

Si ambos comandos imprimen la versión sin errores, ¡todo está listo!

---

## ▶️ Uso

Con el entorno virtual activado y las dependencias instaladas, ejecuta:

```bash
python main.py
```

- Se abrirá una ventana llamada **"Face security_Tark"** mostrando el video de tu cámara.
- Muestra tu rostro y tus manos frente a la cámara para ver la malla facial y el reconocimiento de gestos en acción.
- Para salir, presiona **`q`** o **`Esc`** con la ventana de video en foco.

---

## 📁 Estructura del proyecto

```
Face_Security_Tark/
├── main.py             # Script principal: captura de video, detección y clasificación de gestos
├── requirements.txt    # Dependencias del proyecto (OpenCV y MediaPipe)
└── .gitignore           # Archivos y carpetas ignorados por Git (venv, cache, etc.)
```

---

## 🔍 Cómo funciona el código

El script `main.py` se organiza en las siguientes partes:

1. **Inicialización de MediaPipe**
   - Se crean las instancias de `FaceMesh` (con `refine_landmarks=True` para mayor precisión en ojos e iris) y `Hands` (hasta 2 manos), junto con las utilidades de dibujo (`drawing_utils`, `drawing_styles`).

2. **`contar_dedos_levantados(hand_landmarks, handedness_label)`**
   - Recorre las puntas de los dedos (`TIP_IDS = [4, 8, 12, 16, 20]`, correspondientes a pulgar, índice, medio, anular y meñique).
   - Para el pulgar, compara la posición en el eje X (porque se mueve lateralmente), considerando si la mano es izquierda o derecha.
   - Para los demás dedos, compara la posición en el eje Y de la punta contra la articulación inferior para determinar si están extendidos.
   - Devuelve una lista booleana (`dedos`) y el total de dedos levantados.

3. **`clasificar_gesto(dedos_arriba, total)`**
   - Con base en el total de dedos levantados y cuáles están activos, devuelve una etiqueta de texto: puño, mano abierta, paz/victoria, índice, o el número de dedos detectados.

4. **`main()`**
   - Abre la cámara con `cv2.VideoCapture(0)`.
   - En cada frame:
     - Voltea la imagen horizontalmente (efecto espejo) y la convierte a RGB (formato que espera MediaPipe).
     - Procesa el frame con `face_mesh.process()` y dibuja la malla y los contornos faciales si se detecta un rostro.
     - Procesa el frame con `hands.process()`, dibuja el esqueleto de cada mano detectada y calcula/clasifica el gesto, mostrándolo como texto junto a la muñeca.
     - Calcula los FPS comparando el tiempo entre el frame actual y el anterior, y los muestra en pantalla.
   - El bucle se repite hasta que el usuario presiona `q` o `Esc`, momento en el cual se libera la cámara y se cierran las ventanas.

---

## 🛠️ Solución de problemas

| Problema | Posible causa / solución |
|---|---|
| `No se pudo acceder a la cámara.` | Otra aplicación está usando la cámara, o el índice `0` no corresponde a tu cámara. Prueba cambiar `cv2.VideoCapture(0)` por `1` o `2` en `main.py`. |
| Error al instalar `mediapipe` | Verifica que tu versión de Python sea compatible (3.9–3.11). MediaPipe no siempre soporta las versiones más nuevas de Python inmediatamente. |
| La ventana se congela o va muy lenta | Reduce la resolución de la cámara, cierra otras apps que usen CPU/GPU, o baja `min_detection_confidence` / `min_tracking_confidence`. |
| No detecta gestos correctamente | Asegúrate de tener buena iluminación y que la mano completa esté dentro del cuadro de la cámara. |
| En Linux no abre la cámara | Verifica permisos con `ls -l /dev/video0` y que tu usuario pertenezca al grupo `video`. |

---

## 💡 Posibles mejoras

- Agregar reconocimiento facial con identificación de personas (face recognition / embeddings) para fines de seguridad/control de acceso.
- Guardar registros (logs) de detecciones con marca de tiempo.
- Añadir alertas o notificaciones cuando se detecte un rostro no autorizado.
- Exportar los gestos detectados a un archivo o API externa.
- Crear una interfaz gráfica (GUI) en lugar de la ventana básica de OpenCV.

---

## 🧪 Tecnologías utilizadas

- [Python 3](https://www.python.org/)
- [OpenCV](https://opencv.org/) — captura y procesamiento de video.
- [MediaPipe](https://developers.google.com/mediapipe) — detección de malla facial y manos.

---

## 👤 Autor

**Theylor Ramírez** — Estudiante de Ingeniería de Sistemas, Universidad Nacional de Cajamarca.
Enfocado en ciberseguridad, desarrollo móvil y gestión de proyectos TI.

- GitHub: [@tarkramirez23-gif](https://github.com/tarkramirez23-gif)
- LinkedIn: [Theylor Ramírez Vásquez](https://www.linkedin.com/in/theylor-ramirez-vasquez-4799112a6)

---

## 📄 Licencia

Este proyecto no especifica actualmente una licencia. Si deseas que otras personas puedan usar, modificar o distribuir este código libremente, considera agregar un archivo `LICENSE` (por ejemplo, MIT).

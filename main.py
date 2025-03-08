from flask import Flask, Response, render_template
import cv2
import mediapipe as mp

app = Flask(__name__)

camera = cv2.VideoCapture(0)
def new_frame():
    while True:
        ret,frame = camera.read()
        if not ret:
            break
        else:
            # Convert image to bytes
            _,buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return "type /video"

@app.route('/video')
def video():
    return Response(new_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True,)
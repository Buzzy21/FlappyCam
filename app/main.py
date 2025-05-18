from flask import Flask, Response, render_template, url_for
import cv2
import mediapipe as mp
import camera, flappy

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

# This page will be embedded to display video camera
@app.route('/video/<type>')
def video(type):
    if type == 'regular':
        return Response(camera.generate_regular_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')
    elif type == 'flappy':
        return Response(camera.generate_flappy_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Invalid type",400
    
if __name__ == '__main__': 
    app.run(port=5002,debug=True)
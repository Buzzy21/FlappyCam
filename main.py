from flask import Flask
import cv2
import mediapipe as mp

app = Flask(__name__)

@app.route('/')
def home():
    return 'This is the homescreen'

@app.route('/tab1')
def tab1():
    return 'This is tab 1'

@app.route('/tab2')
def tab2():
    return 'This is tab 2'

app.run()
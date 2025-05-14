from flask import Flask, Response, render_template, url_for
import cv2
import mediapipe as mp
import flappy

capture = cv2.VideoCapture(0)

def process_frame(frame):
        # Convert image to bytes
        _,buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        return (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Generates a plain video camera frame
def generate_regular_frame():
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        else:
             yield process_frame(frame)


# Generates frames for the flappy bird game
def generate_flappy_frame():
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        else:
            frame = flappy.next_frame(frame)
            yield process_frame(frame)
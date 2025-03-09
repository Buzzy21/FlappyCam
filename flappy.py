from flask import Flask, Response, render_template, url_for
from collections import deque
import cv2
import mediapipe as mp
import camera, flappy
import random as rand

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5)

obstacles = deque()
def make_obstacles():
    pass # To be implemented

def next_frame(frame):
    # Process frame
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    
    # Draw andmarks
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
    return frame
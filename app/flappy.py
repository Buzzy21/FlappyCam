from flask import Flask, Response, render_template, url_for
from collections import deque
import cv2
import mediapipe as mp
import camera, flappy
import random as rand

class Player:
    def __init__(self):
        self.x = -1
        self.y = -1
    
    # Update according exactly to landmark position
    def update_position(self, landmark):
        self.x = landmark.x
        self.y = landmark.y

class Obstacle:
    def __init__(self, x, top, bottom, width):
        self.x = x
        self.top = top # Where the part extending from top ends 
        self.bottom = bottom # Where the part rooted from bottom reaches
        self.width = width

        self.color = (6,64,43)

    # Draw the obstacle as a rectangle
    def draw(self,frame):
       frame_height, frame_width = frame.shape[:2]

       # Draw the top part
       cv2.rectangle(frame, (self.x, 0), (self.x+self.width, self.top), self.color, -1)

       # Draw the bottom part
       cv2.rectangle(frame, (self.x,self.bottom), (self.x+self.width,frame_height), self.color, -1)


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5)

obstacle = Obstacle(100, 300, 600, 150) # def __init__(self, x, top, bottom, width)
player = Player()

def next_frame(frame):
    # Process frame
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    
    # Draw andmarks
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

    # Create a new obstacle
    obstacle.draw(frame)


    # KEEP THIS THE LAST LINE
    return frame
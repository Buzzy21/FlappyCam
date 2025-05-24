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
    def update_position(self, landmark, frame):
        h,w = frame.shape[:2]
        self.x = int(landmark.x * w)
        self.y = int(landmark.y * h)

    # Show the player on the screen
    def draw(self,frame): 
        cv2.rectangle(frame, (self.x,self.y), (self.x+50,self.y+50), (6,64,43), -1) 

class Obstacle:
    def __init__(self, x, top, bottom, width, speed):
        self.x = x
        self.top = top # Where the part extending from top ends 
        self.bottom = bottom # Where the part rooted from bottom reaches
        self.width = width
        self.speed = speed

        self.color = (6,64,43)

    # Draw the obstacle as a rectangle
    def draw(self,frame):
       frame_height, frame_width = frame.shape[:2]

       # Draw the top part
       cv2.rectangle(frame, (self.x, 0), (self.x+self.width, self.top), self.color, -1)

       # Draw the bottom part
       cv2.rectangle(frame, (self.x,self.bottom), (self.x+self.width,frame_height), self.color, -1)


class Game:
    def __init__(self):
        mp_hands = mp.solutions.hands
        #mp_drawing = mp.solutions.drawing_utils
        self.hands = mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5)

        self.obstacle = Obstacle(2000, 300, 600, 150, 15) # def __init__(self, x, top, bottom, width, speed)
        self.player = Player()

    def restart(self):
        self.__init__()
        print("RESTARTED")

    def regulate_game(self):
        # Time to determine whether the played evaded the obstacle
        if self.obstacle.x <= self.player.x:
            if self.player.y < self.obstacle.bottom and self.player.y > self.obstacle.top: # Player evaded
                pass
            else: # Player touched the obstacle
                self.restart()

game = Game()

def next_frame(frame):
    # Process frame
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = game.hands.process(rgb)
    
    game.regulate_game()

    # Player stuff
    if results.multi_hand_landmarks and results.multi_hand_landmarks[0].landmark:
        player_landmark = results.multi_hand_landmarks[0].landmark[0]
        game.player.update_position(player_landmark,frame) 
        game.player.draw(frame)

    # Obstacle stuff
    game.obstacle.draw(frame)
    game.obstacle.x -= game.obstacle.speed

    # KEEP THIS THE LAST LINE
    return frame
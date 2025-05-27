from flask import Flask, Response, render_template, url_for
from collections import deque
import cv2
import mediapipe as mp
import camera, flappy
import random as rand

class Player:
    def __init__(self, size):
        self.x = -1
        self.y = -1
        self.size = size

        # The actual value will be modified in update_transform()
        self.actualSize = -1 
    
    # Update player's state in terms of position-size-rotation-etc
    def update_transform(self, landmark, frame):
        h,w = frame.shape[:2]
        self.x = int(landmark.x * w)
        self.y = int(landmark.y * h)
    
    # Show the player on the screen
    def draw(self,frame): 
        h,w = frame.shape[:2]
        self.actualSize =  int(min(h,w) * self.size) # Scale fraction into actual integers
        cv2.rectangle(frame, (self.x,self.y), (self.x+self.actualSize,self.y+self.actualSize), (6,64,43), -1) 

class Obstacle:
    def __init__(self, x, top, bottom, width, speed):
        self.x = x
        self.top = top # Where the part extending from top ends (in fraction)
        self.bottom = bottom # Where the part rooted from bottom reaches (in fraction)
        self.width = width # in fraction
        self.speed = speed

        # The actual values will be modified in update_transform()
        self.actualWidth = -1;
        self.actualTop = -1;
        self.actualBottom = -1;

        self.color = (6,64,43)

    # Update obstacle's state in terms of position-size-rotation-etc
    def update_transform(self, frame):
        h,w = frame.shape[:2]

        game.obstacle.x -= game.obstacle.speed
        
        # Scale fraction into actual integers
        self.actualWidth = int(self.width*w)
        self.actualTop = int(self.top*h)
        self.actualBottom = int(self.bottom*h) 

    # Draw the obstacle as a rectangle
    def draw(self,frame):
       h,w = frame.shape[:2]

       # Draw the top part
       cv2.rectangle(frame, (self.x, 0), (self.x+self.actualWidth, self.actualTop), self.color, -1)

       # Draw the bottom part
       cv2.rectangle(frame, (self.x,self.actualBottom), (self.x+self.actualWidth,h), self.color, -1)


class Game:
    def __init__(self):
        mp_hands = mp.solutions.hands
        #mp_drawing = mp.solutions.drawing_utils
        self.hands = mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5)

        self.obstacle = Obstacle(1000, 2/5, 3.5/5, 1/15, 15) # def __init__(self, x, top, bottom, width, speed)
        self.player = Player(1/25)

    def restart(self):
        self.__init__()
        print("RESTARTED")

    def regulate_game(self):
        # Check whether player collided with obstacle
        if self.player.x > self.obstacle.x and self.player.x < self.obstacle.x+self.obstacle.actualWidth and (self.player.y > self.obstacle.actualBottom or self.player.y < self.obstacle.actualTop): # Player collided
            self.restart()
        

game = Game()

def next_frame(frame):
    # Process frame
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = game.hands.process(rgb)
    
    game.regulate_game()

    """
    # DRAWING THE LANDMARKS OUT CUZ THEY LOOK COOL:
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame,landmarks,mp.solutions.hands.HAND_CONNECTIONS)
    """

    # Player stuff
    if results.multi_hand_landmarks and results.multi_hand_landmarks[0].landmark:
        player_landmark = results.multi_hand_landmarks[0].landmark[0]
        game.player.update_transform(player_landmark,frame) 
        game.player.draw(frame)

    # Obstacle stuff
    game.obstacle.draw(frame)
    game.obstacle.update_transform(frame)

    # KEEP THIS THE LAST LINE
    return frame
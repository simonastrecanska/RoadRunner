from turtle import Turtle
import logging

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280

class Player(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.goto(STARTING_POSITION)
        self.setheading(90)
        logging.info("Player initialized at starting position")

    def move_turtle(self):
        self.forward(MOVE_DISTANCE)
        logging.info(f"Player moved to {self.position()}")

    def reset_turtle(self):
        self.goto(STARTING_POSITION)
        logging.info("Player reset to starting position")

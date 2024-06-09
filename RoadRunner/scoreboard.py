from turtle import Turtle
import time

FONT = ("Courier", 24, "normal")
LEVEL_POSITION = (-270, 250)
CENTER_POSITION = (0, 0)

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.hideturtle()
        self.penup()
        self.goto(LEVEL_POSITION)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(LEVEL_POSITION)
        self.write(f"Level: {self.level}", align="left", font=FONT)

    def increase_level(self):
        self.level += 1
        self.update_scoreboard()

    def game_over(self):
        self.goto(CENTER_POSITION)
        self.write("Game Over!!", align="center", font=FONT)

    def display_congratulations(self, screen, message_turtle, car_manager):
        car_manager.hide_cars()
        message_turtle.clear()
        message_turtle.goto(CENTER_POSITION)
        message_turtle.write("Congratulations!", align="center", font=FONT)
        screen.update()
        time.sleep(1)
        for i in range(3, 0, -1):
            message_turtle.clear()
            message_turtle.write(f"Next level in {i}...", align="center", font=FONT)
            screen.update()
            time.sleep(1)
        message_turtle.clear()
        car_manager.show_cars()
        self.update_scoreboard()

    def display_lose_message(self, screen, message_turtle, car_manager):
        car_manager.hide_cars()
        message_turtle.clear()
        message_turtle.goto(CENTER_POSITION)
        message_turtle.write("You Lose!", align="center", font=FONT)
        screen.update()
        time.sleep(2)
        message_turtle.clear()
        self.game_over()

    def hide_message(self, message_turtle):
        message_turtle.clear()
        message_turtle.hideturtle()

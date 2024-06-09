import time
from turtle import Screen, Turtle
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
import tkinter as tk
import logging
from game import read_existing_players, get_player_name, update_results_file
import os
from datetime import datetime

LOG_FILE = 'game.log'

def reset_log_file_if_new_day(log_file):
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            first_line = file.readline().strip()
            if first_line:
                log_date = first_line.split(' ')[0]
                current_date = datetime.now().strftime('%Y-%m-%d')
                if log_date != current_date:
                    with open(log_file, 'w') as file:
                        pass

def on_close():
    global game_is_on
    game_is_on = False
    root.destroy()

def toggle_pause():
    global game_is_paused
    game_is_paused = not game_is_paused
    logging.info(f"Pause state changed to: {game_is_paused}")
    if game_is_paused:
        pause_text.write("PAUSED", align="center", font=("Courier", 24, "normal"))
    else:
        pause_text.clear()

if __name__ == '__main__':
    # Reset log file if it's a new day
    reset_log_file_if_new_day(LOG_FILE)

    logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    screen = Screen()
    root = tk.Tk()
    root.withdraw()

    screen.setup(width=600, height=600)
    screen.tracer(0)

    unnamed_counter, existing_players = read_existing_players()
    player_name, unnamed_counter = get_player_name(screen, unnamed_counter, existing_players)

    logging.info(f"Game started by player: {player_name}")

    player = Player()
    car_manager = CarManager()
    scoreboard = Scoreboard()

    pause_text = Turtle()
    pause_text.hideturtle()
    pause_text.penup()
    pause_text.goto(0, 0)

    message_turtle = Turtle()
    message_turtle.hideturtle()
    message_turtle.penup()

    screen.listen()

    def log_player_move():
        logging.info(f"Player {player_name} moved.")

    screen.onkey(key="Up", fun=lambda: [player.move_turtle(), log_player_move()])
    screen.onkey(key="p", fun=toggle_pause)

    game_is_on = True
    game_is_paused = False

    root.protocol("WM_DELETE_WINDOW", on_close)
    screen._root.protocol("WM_DELETE_WINDOW", on_close)

    try:
        while game_is_on:
            screen.update()
            time.sleep(0.1)
            if not game_is_paused:
                car_manager.create_car()
                car_manager.move_car()

                for car in car_manager.all_cars:
                    if car.distance(player) < 22:
                        game_is_on = False
                        scoreboard.display_lose_message(screen, message_turtle, car_manager)
                        logging.info(f"Player {player_name} collided with a car and lost at level {scoreboard.level}.")
                        update_results_file(player_name, scoreboard.level)
                        break  

                if player.ycor() > 285:
                    scoreboard.display_congratulations(screen, message_turtle, car_manager)
                    player.reset_turtle()
                    car_manager.level_up_speed()
                    logging.info(f"Player {player_name} reached the wall and leveled up to level {scoreboard.level}.")

                    scoreboard.increase_level()
                    
    except tk.TclError:
        logging.info("Game window closed.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        logging.info(f"Game ended for player: {player_name}")
        screen.bye()

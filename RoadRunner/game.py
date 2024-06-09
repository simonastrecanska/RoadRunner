import os
from threading import Lock

RESULTS_FILE = 'results.txt'
DEFAULT_PLAYER_NAME = 'Unnamed Player'
file_lock = Lock()

def read_existing_players(results_file=RESULTS_FILE):
    unnamed_counter = 1
    existing_players = set()
    if os.path.exists(results_file):
        with open(results_file, "r") as file:
            for line in file:
                player_name = line.strip().split(": ")[0]
                existing_players.add(player_name)
                if player_name.startswith(DEFAULT_PLAYER_NAME):
                    number = int(player_name.split(" ")[-1])
                    if number >= unnamed_counter:
                        unnamed_counter = number + 1
    return unnamed_counter, existing_players

def get_player_name(screen, unnamed_counter, existing_players):
    player_name = screen.textinput("Player Name", "Enter your name:")
    if not player_name:
        player_name = f"{DEFAULT_PLAYER_NAME} {unnamed_counter}"
        while player_name in existing_players:
            unnamed_counter += 1
            player_name = f"{DEFAULT_PLAYER_NAME} {unnamed_counter}"
        unnamed_counter += 1
    return player_name, unnamed_counter

def update_results_file(name, score, results_file=RESULTS_FILE):
    with file_lock:
        results = []
        if os.path.exists(results_file):
            with open(results_file, "r") as file:
                for line in file:
                    line_name, line_score = line.strip().split(": ")
                    results.append((line_name, int(line_score)))
        updated = False
        for i, (line_name, line_score) in enumerate(results):
            if line_name == name:
                if score > line_score:
                    results[i] = (name, score)
                updated = True
                break
        if not updated:
            results.append((name, score))
        results.sort(key=lambda x: x[1], reverse=True)
        with open(results_file, "w") as file:
            for line_name, line_score in results:
                file.write(f"{line_name}: {line_score}\n")

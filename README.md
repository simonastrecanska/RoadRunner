# RoadRunner

RoadRunner is a fun and interactive game where you control a turtle character to avoid cars and reach the top of the screen to level up.

## How to Run the Game

1. **Clone the repository:**
   ```bash
   git clone https://github.com/simonastrecanska/RoadRunner.git
   ```
2. Navigate to the project directory:

   ```bash
   cd RoadRunner
   ```
   
4. Run the program:

   ```bash
   python3 main.py
   ```

Sure, here's the updated README with explanations on why to play the game and the purpose of the `test_game.py` and `test_playthrough.py` files:

### README.md

```markdown
# RoadRunner

RoadRunner is a fun and interactive game where you control a turtle character to avoid cars and reach the top of the screen to level up.

## How to Run the Game

1. **Clone the repository:**
   ```bash
   git clone https://github.com/simonastrecanska/RoadRunner.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd RoadRunner
   ```

3. **Install the required dependencies:**
   Ensure you have Python installed. You can create a virtual environment and install the required packages using:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

4. **Run the program:**
   ```bash
   python3 main.py
   ```
   
## Explanation of Test Files

### test_game.py
This file contains unit tests for various functions and components within the game. The purpose of these tests is to ensure that individual parts of the game logic work correctly in isolation. By running these tests, you can verify that the basic functionality of the game remains intact whenever changes are made.

### test_playthrough.py
This file contains integration tests that simulate complete playthroughs of the game. These tests check the interaction between different components and ensure that the game functions correctly as a whole. They include scenarios such as:
- Verifying that the player can level up.
- Ensuring that the game ends when the player collides with a car.
- Testing the pause and unpause functionality.


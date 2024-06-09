import unittest
from unittest.mock import Mock, patch
from turtle import Screen, Turtle
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
from game import read_existing_players, get_player_name, update_results_file
import time
import os

class TestPlaythrough(unittest.TestCase):

    def setUp(self):
        self.mock_screen = Mock(spec=Screen)
        self.mock_screen.textinput = Mock(return_value=None)
        self.mock_screen.update = Mock()
        self.mock_screen.listen = Mock()
        self.mock_screen.onkey = Mock()
        self.mock_screen.tracer = Mock()
        self.mock_screen.setup = Mock()
        
        self.test_results_file = 'test_results.txt'
        self.default_results_file = 'results.txt'
        if os.path.exists(self.default_results_file):
            os.rename(self.default_results_file, 'results_backup.txt')
        open(self.test_results_file, 'w').close()
        self.addCleanup(self.cleanup)
        
        self.player = Player()
        self.car_manager = CarManager()
        self.scoreboard = Scoreboard()

    def cleanup(self):
        if os.path.exists(self.test_results_file):
            os.remove(self.test_results_file)
        if os.path.exists('results_backup.txt'):
            os.rename('results_backup.txt', self.default_results_file)

    @patch('time.sleep', return_value=None)
    def test_simple_playthrough(self, _):
        player_name, _ = get_player_name(self.mock_screen, 1, set())
        
        for _ in range(1):
            self.player.goto(0, 290)
            if self.player.ycor() > 285:
                self.scoreboard.display_congratulations(self.mock_screen, Mock(), self.car_manager)
                self.player.reset_turtle()
                self.car_manager.level_up_speed()
                self.scoreboard.increase_level()
        
        self.assertEqual(self.scoreboard.level, 2)
        self.assertLess(self.player.ycor(), 0)
        
    @patch('time.sleep', return_value=None)
    @patch('random.randint', return_value=1)
    def test_playthrough_with_collision(self, _, __):
        player_name, _ = get_player_name(self.mock_screen, 1, set())
        
        self.car_manager.create_car()
        self.assertTrue(len(self.car_manager.all_cars) > 0, "No cars were created.")
        
        if len(self.car_manager.all_cars) > 0:
            self.car_manager.all_cars[0].goto(self.player.xcor(), self.player.ycor())
        
        game_is_on = True
        while game_is_on:
            self.car_manager.move_car()
            for car in self.car_manager.all_cars:
                if car.distance(self.player) < 22:
                    game_is_on = False
                    self.scoreboard.display_lose_message(self.mock_screen, Mock(), self.car_manager)
                    update_results_file(player_name, self.scoreboard.level, self.test_results_file)
                    break
        
        with open(self.test_results_file, 'r') as file:
            results = file.readlines()
        
        self.assertIn(f"{player_name}: 1", results[0].strip())
    
    @patch('time.sleep', return_value=None)
    def test_playthrough_with_multiple_levels(self, _):
        player_name, _ = get_player_name(self.mock_screen, 1, set())
        
        for _ in range(5):
            self.player.goto(0, 290)
            if self.player.ycor() > 285:
                self.scoreboard.display_congratulations(self.mock_screen, Mock(), self.car_manager)
                self.player.reset_turtle()
                self.car_manager.level_up_speed()
                self.scoreboard.increase_level()
        
        self.assertEqual(self.scoreboard.level, 6)
        self.assertLess(self.player.ycor(), 0)
        
    @patch('time.sleep', return_value=None)
    def test_playthrough_with_pause(self, _):
        player_name, _ = get_player_name(self.mock_screen, 1, set())
        
        game_is_paused = False
        def toggle_pause():
            nonlocal game_is_paused
            game_is_paused = not game_is_paused
        
        self.mock_screen.onkey.side_effect = toggle_pause
        
        toggle_pause()
        self.assertTrue(game_is_paused)
        
        toggle_pause()
        self.assertFalse(game_is_paused)
        
        for _ in range(3):
            self.player.goto(0, 290)
            if self.player.ycor() > 285:
                self.scoreboard.display_congratulations(self.mock_screen, Mock(), self.car_manager)
                self.player.reset_turtle()
                self.car_manager.level_up_speed()
                self.scoreboard.increase_level()
        
        self.assertEqual(self.scoreboard.level, 4)
        self.assertLess(self.player.ycor(), 0)

    @patch('time.sleep', return_value=None)
    def test_car_speed_increases_with_level(self, _):
        initial_speed = self.car_manager.car_speed
        
        for _ in range(5):
            self.player.goto(0, 290)
            if self.player.ycor() > 285:
                self.scoreboard.display_congratulations(self.mock_screen, Mock(), self.car_manager)
                self.player.reset_turtle()
                self.car_manager.level_up_speed()
                self.scoreboard.increase_level()
        
        self.assertGreater(self.car_manager.car_speed, initial_speed, "Car speed should increase with each level")

if __name__ == '__main__':
    unittest.main()

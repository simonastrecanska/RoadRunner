import unittest
from unittest.mock import Mock
from game import read_existing_players, get_player_name, update_results_file
import os

class TestGameFunctions(unittest.TestCase):

    def setUp(self):
        self.mock_screen = Mock()
        self.mock_screen.textinput = Mock(return_value=None)
        self.test_results_file = 'test_results.txt'
        self.default_results_file = 'results.txt'
        if os.path.exists(self.default_results_file):
            os.rename(self.default_results_file, 'results_backup.txt')
        open(self.test_results_file, 'w').close()
        self.addCleanup(self.cleanup)

    def cleanup(self):
        if os.path.exists(self.test_results_file):
            os.remove(self.test_results_file)
        if os.path.exists('results_backup.txt'):
            os.rename('results_backup.txt', self.default_results_file)

    def test_read_existing_players(self):
        with open(self.test_results_file, 'w') as file:
            file.write("Unnamed Player 1: 5\nUnnamed Player 2: 10\n")
        
        unnamed_counter, existing_players = read_existing_players(self.test_results_file)
        
        self.assertEqual(unnamed_counter, 3)
        self.assertIn("Unnamed Player 1", existing_players)
        self.assertIn("Unnamed Player 2", existing_players)

    def test_get_player_name(self):
        unnamed_counter = 1
        existing_players = {"Unnamed Player 1"}
        player_name, new_unnamed_counter = get_player_name(self.mock_screen, unnamed_counter, existing_players)
        
        self.assertEqual(player_name, "Unnamed Player 2")
        self.assertEqual(new_unnamed_counter, 3)

    def test_update_results_file(self):
        update_results_file("Player 1", 15, self.test_results_file)
        update_results_file("Player 2", 20, self.test_results_file)
        update_results_file("Player 1", 25, self.test_results_file)
        
        with open(self.test_results_file, 'r') as file:
            results = file.readlines()
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].strip(), "Player 1: 25")
        self.assertEqual(results[1].strip(), "Player 2: 20")

    def test_update_results_file_with_edge_cases(self):
        update_results_file("Player 1", -1, self.test_results_file)
        update_results_file("Player 2", 0, self.test_results_file)
        update_results_file("Player 3", 999999999, self.test_results_file)
        
        with open(self.test_results_file, 'r') as file:
            results = file.readlines()
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].strip(), "Player 3: 999999999")
        self.assertEqual(results[1].strip(), "Player 2: 0")
        self.assertEqual(results[2].strip(), "Player 1: -1")

    def test_read_existing_players_with_large_file(self):
        with open(self.test_results_file, 'w') as file:
            for i in range(10000):
                file.write(f"Unnamed Player {i+1}: {i}\n")
        
        unnamed_counter, existing_players = read_existing_players(self.test_results_file)
        
        self.assertEqual(unnamed_counter, 10001)
        self.assertIn("Unnamed Player 1", existing_players)
        self.assertIn("Unnamed Player 10000", existing_players)

    def test_get_player_name_with_edge_cases(self):
        unnamed_counter = 1
        existing_players = {f"Unnamed Player {i}" for i in range(1, 100)}
        
        player_name, new_unnamed_counter = get_player_name(self.mock_screen, unnamed_counter, existing_players)
        
        self.assertEqual(player_name, "Unnamed Player 100")
        self.assertEqual(new_unnamed_counter, 101)

    def test_update_results_file_concurrent(self):
        update_results_file("Player 1", 10, self.test_results_file)
        
        from concurrent.futures import ThreadPoolExecutor
        
        def update_file(player, score):
            update_results_file(player, score, self.test_results_file)
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.submit(update_file, "Player 2", 20)
            executor.submit(update_file, "Player 1", 15)
            executor.submit(update_file, "Player 3", 5)
            executor.submit(update_file, "Player 4", 50)
            executor.submit(update_file, "Player 2", 25)
        
        with open(self.test_results_file, 'r') as file:
            results = file.readlines()
        
        results = [result.strip() for result in results]
        self.assertEqual(len(results), 4)
        self.assertIn("Player 4: 50", results)
        self.assertIn("Player 2: 25", results)
        self.assertIn("Player 1: 15", results)
        self.assertIn("Player 3: 5", results)

if __name__ == '__main__':
    unittest.main()

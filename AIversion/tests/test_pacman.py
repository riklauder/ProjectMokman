"""Sometimes pacman will lose all games, so winRate == 0 or avgScore is really
low, and these tests fail. In that case, try running again.

Tests are run with the silent flag, '-s' to prevent polluting the console output.

Choose a benchmark 'expected_avg_score' value conservatively so the comparisons will
"always" pass, with as tight a margin as you're comfortable. As the performance
improves, you can increase the expected_avg_score.

"""


import unittest
import sys
import os
# from pacman import *
import pacman
# Add to system path to import from data module:
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')


class Tester(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """Called before tests in an individual class run."""
        pass

    @classmethod
    def tearDownClass(self):
        """Called after tests in an individual class have run."""
        pass

    def setUp(self):
        """Called before each test method."""
        pass

    def tearDown(self):
        """Called after each test method."""
        pass

    def test_ReflexAgent(self):
        expected_avg_score = 100
        s = "-p ReflexAgent -l testClassic --numGames 5 --quietTextGraphics -s"
        games = pacman.runGames(**pacman.readCommand(s.split()))
        output_dict = pacman.formatOutput(games)
        avg_score = output_dict['avg_score']
        output_string = output_dict['output_string']
        self.assertTrue(avg_score > expected_avg_score, 
                    '\n{} Expected Average Score: {}\n{}\n{}'
                    .format('Oops, avg_score too low!', expected_avg_score,
                    output_string, '..Maybe try running tests once more?'))

    def test_astar(self):
        expected_avg_score = -400
        s = "-p AStarAgent -l testClassicTight --numGames 10 --quietTextGraphics -s"
        games = pacman.runGames(**pacman.readCommand(s.split()))
        output_dict = pacman.formatOutput(games)
        # scores = output_dict['scores']
        # wins = output_dict['wins']
        # win_rate = output_dict['win_rate']
        avg_score = output_dict['avg_score']
        output_string = output_dict['output_string']
        # self.assertTrue(win_rate > 0.1, "Oops, win_rate too low!")  # percent
        self.assertTrue(avg_score > expected_avg_score, 
                    '\n{} Expected Average Score: {}\n{}\n{}'
                    .format('Oops, avg_score too low!', expected_avg_score,
                    output_string, '..Maybe try running tests once more?'))

    def test_MinimaxAgent(self):
        """Our MinimaxAgent will sometimes not finish
        because pacman doesnt move to the food. This only happens sometimes
        for some strange reason. So we have to rerun the tests if it takes too
        long.
        """
        expected_avg_score = 550
        s = "-p MinimaxAgent -l testClassic --numGames 3 --quietTextGraphics -s"
        games = pacman.runGames(**pacman.readCommand(s.split()))
        output_dict = pacman.formatOutput(games)
        avg_score = output_dict['avg_score']
        output_string = output_dict['output_string']
        self.assertTrue(avg_score > expected_avg_score, 
                    '\n{} Expected Average Score: {}\n{}\n{}'
                    .format('Oops, avg_score too low!', expected_avg_score,
                    output_string, '..Maybe try running tests once more?'))

    def test_ExpectimaxAgent(self):
        expected_avg_score = -1000
        s = "-p ExpectimaxAgent -l trappedClassic -a depth=3 --numGames 10 --quietTextGraphics -s"
        games = pacman.runGames(**pacman.readCommand(s.split()))
        output_dict = pacman.formatOutput(games)
        avg_score = output_dict['avg_score']
        output_string = output_dict['output_string']
        self.assertTrue(avg_score > expected_avg_score, 
                    '\n{} Expected Average Score: {}\n{}\n{}'
                    .format('Oops, avg_score too low!', expected_avg_score,
                    output_string, '..Maybe try running tests once more?'))


    def test_DStarLiteAgent(self):
        expected_avg_score = -200
        s = "-p DStarLiteAgent -l testClassicTight --numGames 10 --quietTextGraphics -s"
        games = pacman.runGames(**pacman.readCommand(s.split()))
        output_dict = pacman.formatOutput(games)
        # scores = output_dict['scores']
        # wins = output_dict['wins']
        # win_rate = output_dict['win_rate']
        avg_score = output_dict['avg_score']
        output_string = output_dict['output_string']
        # self.assertTrue(win_rate > 0.1, "Oops, win_rate too low!")  # percent
        self.assertTrue(avg_score > expected_avg_score, 
                    '\n{} Expected Average Score: {}\n{}\n{}'
                    .format('Oops, avg_score too low!', expected_avg_score,
                    output_string, '..Maybe try running tests once more?'))


if __name__ == '__main__':
    unittest.main()


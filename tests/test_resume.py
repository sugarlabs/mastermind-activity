"""Exercise restored games through real GTK canvas widgets."""
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from activity import Mastermind
from canvas import Canvas
from constants import BallType, Difficulty
from utils import get_columns_for_difficulty


class ResumeTest(unittest.TestCase):
    def make_target(self, difficulty, turn=0, won=False,
                    saved_difficulty=True):
        columns = get_columns_for_difficulty(difficulty)
        correct = list(range(columns))
        balls = {x: [0] * turn + [BallType.NULL] * (10 - turn)
                 for x in range(columns)}
        if won:
            for x in range(columns):
                balls[x][turn - 1] = correct[x]
        metadata = {'level': str(turn), 'correct': repr(correct),
                    'balls': repr(balls)}
        if saved_difficulty:
            metadata['difficulty'] = str(difficulty)
        canvas = Canvas(False)
        self.addCleanup(canvas.destroy)
        target = SimpleNamespace(metadata=metadata, canvas=canvas,
                                 ok_button=Mock(), label=Mock(),
                                 easy_button=Mock(), medium_button=Mock(),
                                 advanced_button=Mock(), expert_button=Mock())
        canvas.connect('win',
                       lambda unused: Mastermind._win_cb(target, canvas))
        canvas.connect('lose',
                       lambda unused: Mastermind._lose_cb(target, canvas))
        return target, balls

    def assert_locked(self, canvas):
        self.assertTrue(all(not ball.draggable
                            for ball in canvas.originbox.balls))
        self.assertTrue(all(not ball.draggable and not ball.drag_dest
                            for column in canvas.grid.balls.values()
                            for ball in column))

    def test_completed_loss_resumes_at_all_difficulties(self):
        for difficulty in range(4):
            with self.subTest(difficulty=difficulty):
                target, balls = self.make_target(difficulty, turn=10)
                Mastermind.read_file(target)
                self.assertEqual(target.canvas.grid.level, 10)
                self.assertEqual(target.canvas.get_game_data()['balls'], balls)
                target.ok_button.set_sensitive.assert_called_with(False)
                target.label.set_text.assert_called_with('You lost')
                self.assert_locked(target.canvas)

    def test_wins_on_early_and_last_turn_remain_finished(self):
        for turn in (1, 10):
            with self.subTest(turn=turn):
                target, balls = self.make_target(Difficulty.MEDIUM, turn, True)
                Mastermind.read_file(target)
                target.label.set_text.assert_called_with('You win')
                target.ok_button.set_sensitive.assert_called_with(False)
                self.assertEqual(target.canvas.get_game_data()['balls'], balls)
                self.assert_locked(target.canvas)

    def test_legacy_entries_infer_difficulty_from_saved_columns(self):
        for difficulty in range(4):
            with self.subTest(difficulty=difficulty):
                target, _ = self.make_target(
                    difficulty, saved_difficulty=False)
                Mastermind.read_file(target)
                self.assertEqual(target.canvas.difficulty, difficulty)

    def test_new_turns_still_finish_and_restart_works(self):
        for won in (False, True):
            with self.subTest(won=won):
                target, _ = self.make_target(Difficulty.MEDIUM)
                Mastermind.read_file(target)
                guess = target.canvas.level if won else [0, 0, 0]
                for unused in range(1 if won else 10):
                    row = target.canvas.grid.level
                    for column, ball in enumerate(guess):
                        target.canvas.grid.set_ball(column, row, ball)
                    target.canvas.end_turn()
                expected = 'You win' if won else 'You lost'
                target.label.set_text.assert_called_with(expected)
                self.assert_locked(target.canvas)
                Mastermind._restart_cb(target, None)
                self.assertEqual(target.canvas.grid.level, 0)
                self.assertTrue(target.canvas.originbox.balls[0].draggable)
                target.label.set_text.assert_called_with('')

    def test_unfinished_row_remains_playable(self):
        target, _ = self.make_target(Difficulty.MEDIUM, turn=4)
        Mastermind.read_file(target)
        self.assertEqual(target.canvas.grid.level, 4)
        target.ok_button.set_sensitive.assert_called_with(False)
        target.label.set_text.assert_not_called()
        self.assertTrue(target.canvas.grid.balls[0][4].drag_dest)
        self.assertTrue(target.canvas.originbox.balls[0].draggable)

    def test_byte_metadata_resumes_a_completed_game(self):
        target, balls = self.make_target(Difficulty.EXPERT, turn=10)
        target.metadata = {key: value.encode('utf-8')
                           for key, value in target.metadata.items()}
        Mastermind.read_file(target)
        self.assertEqual(target.canvas.difficulty, Difficulty.EXPERT)
        self.assertEqual(target.canvas.get_game_data()['balls'], balls)
        self.assert_locked(target.canvas)

    def test_round_trip_saves_difficulty_and_completed_board(self):
        for difficulty in range(4):
            with self.subTest(difficulty=difficulty):
                target, balls = self.make_target(difficulty, turn=10)
                Mastermind.read_file(target)
                Mastermind.write_file(target, '/unused')
                self.assertIsInstance(target.metadata['difficulty'], bytes)
                self.assertEqual(int(target.metadata['difficulty']),
                                 difficulty)
                Mastermind.read_file(target)
                self.assertEqual(target.canvas.get_game_data()['balls'], balls)
                self.assert_locked(target.canvas)


if __name__ == '__main__':
    unittest.main()

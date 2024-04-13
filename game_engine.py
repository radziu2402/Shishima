import json


class GameEngine:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.positions = [None] * 9
        self.positions[7], self.positions[0], self.positions[1] = 'X', 'X', 'X'
        self.positions[3], self.positions[4], self.positions[5] = 'O', 'O', 'O'
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def make_move(self, from_pos, to_pos):
        if self.positions[from_pos] == self.current_player and self.positions[to_pos] is None:
            self.positions[to_pos] = self.current_player
            self.positions[from_pos] = None
            if self.check_winner():
                self.game_over = True
                self.winner = self.current_player
            else:
                self.switch_player()
            return True
        return False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        winning_combinations = [
            (0, 8, 4), (1, 8, 5),
            (2, 8, 6), (3, 8, 7)
        ]
        for combo in winning_combinations:
            if all(self.positions[i] == self.current_player for i in combo):
                return True
        return False

    def get_game_state(self):
        return {
            'positions': self.positions,
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner
        }

    def load_game(self, filepath):
        try:
            with open(filepath, 'r') as f:
                game_state = json.load(f)
                self.positions = game_state['positions']
                self.current_player = game_state['current_player']
                self.game_over = game_state['game_over']
                self.winner = game_state.get('winner')
        except Exception as e:
            print(f"Error loading game: {e}")

    def save_game(self, filepath):
        game_state = self.get_game_state()
        try:
            with open(filepath, 'w') as f:
                json.dump(game_state, f)
        except Exception as e:
            print(f"Error saving game: {e}")

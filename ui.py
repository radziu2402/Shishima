import tkinter as tk
from math import cos, sin, pi
from tkinter import filedialog
from tkinter.messagebox import askyesno


class ShisimaUI(tk.Tk):
    def __init__(self, game_engine):
        super().__init__()
        self.game_engine = game_engine
        self.title('Shisima Game')
        self.canvas = tk.Canvas(self, width=300, height=300)
        self.canvas.pack()
        self.status_label = tk.Label(self, text="Ruch gracza X", font=("Helvetica", 16))
        self.status_label.pack()
        self.selected_piece = None
        self.create_board()
        self.redraw_pieces()
        self.canvas.bind("<Button-1>", self.click_event)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        answer = askyesno("Shisima", "Do you want to save your game?")
        if answer:
            file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                     filetypes=[("JSON files", "*.json")],
                                                     title="Save Game As")
            if file_path:
                self.game_engine.save_game(file_path)

        """Zamknij aplikację."""
        self.destroy()  # niszczy okno
        self.quit()  # kończy mainloop()

    def check_game_over(self):
        if self.game_engine.check_winner():
            winner = self.game_engine.current_player
            message = f"Wygrał gracz {winner}!" if winner != "Remis" else "Remis!"
            self.end_game(message)
        else:
            self.game_engine.switch_player()
            self.update_status_label()

    def create_board(self):
        self.canvas.create_oval(50, 50, 250, 250, outline='black')
        self.outer_positions = []
        for i in range(8):
            angle = 2 * pi * i / 8
            x = 150 + cos(angle) * 100
            y = 150 + sin(angle) * 100
            self.outer_positions.append((x, y))
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, outline='black')
        self.shisima_position = (150, 150)
        self.canvas.create_oval(130, 130, 170, 170, fill='blue', outline='black')

    def redraw_pieces(self):
        game_state = self.game_engine.get_game_state()  # Pobierz cały stan gry jako słownik
        positions = game_state['positions']
        current_player = game_state['current_player']
        game_over = game_state['game_over']

        self.canvas.delete('piece')
        for i, pos in enumerate(self.outer_positions + [self.shisima_position]):
            x, y = pos
            piece = positions[i]
            if piece:
                color = 'black' if piece == 'X' else 'green'
                self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color, outline='black', tags='piece')

        if game_over:
            winner_message = f"Wygrał gracz {current_player}!" if game_state['winner'] else "Remis!"
            self.status_label.config(text=winner_message)
        else:
            self.status_label.config(text=f"Ruch gracza {current_player}")

    def click_event(self, event):
        if self.game_engine.game_over:
            return
        clicked_index = self.get_clicked_index(event.x, event.y)
        if clicked_index is not None:
            if self.selected_piece is None:
                if self.game_engine.positions[clicked_index] == self.game_engine.current_player:
                    self.selected_piece = clicked_index
                    self.highlight_piece(clicked_index)  # Zaznacz nowy pionek
            else:
                # Jeśli gracz kliknął na ten sam pionek ponownie, odznacz go
                if clicked_index == self.selected_piece:
                    self.canvas.delete('highlight')  # Usuń zaznaczenie
                    self.selected_piece = None  # Resetuj wybrany pionek
                else:
                    if self.game_engine.make_move(self.selected_piece, clicked_index):
                        self.canvas.delete('highlight')  # Usuń zaznaczenie po wykonaniu ruchu
                        if self.game_engine.check_winner():
                            self.end_game(f"Wygrał gracz {self.game_engine.current_player}!")
                        self.redraw_pieces()
                    else:
                        self.canvas.delete('highlight')
                        self.selected_piece = None
                        if self.game_engine.positions[clicked_index] == self.game_engine.current_player:
                            self.selected_piece = clicked_index
                            self.highlight_piece(clicked_index)

    def get_clicked_index(self, x, y):
        for i, pos in enumerate(self.outer_positions + [self.shisima_position]):
            px, py = pos
            if (px - 20 < x < px + 20) and (py - 20 < y < py + 20):
                return i
        return None

    def highlight_piece(self, index):
        x, y = self.outer_positions[index] if index < 8 else self.shisima_position
        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill='grey', outline='red', tags='highlight')

    def end_game(self, message):
        self.game_engine.game_over = True
        self.update_status_label(message)

    def update_status_label(self, message=None):
        if message:
            self.status_label.config(text=message)
        else:
            text = "Ruch gracza X" if self.game_engine.current_player == 'X' else "Ruch gracza O"
            if self.game_engine.game_over:
                text = "Wygrał gracz X" if self.game_engine.current_player == 'X' else "Wygrał gracz O"
            self.status_label.config(text=text)

import tkinter as tk
import numpy as np

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return O if x_count > o_count else X

def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY}

def result(board, action):
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Invalid action")
    new_board = [row[:] for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    return None

def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    if terminal(board):
        return None
    current_player = player(board)
    if current_player == X:
        value, move = max_value(board)
    else:
        value, move = min_value(board)
    return move

def max_value(board):
    if terminal(board):
        return utility(board), None
    v = float('-inf')
    best_action = None
    for action in actions(board):
        min_val, _ = min_value(result(board, action))
        if min_val > v:
            v = min_val
            best_action = action
        if v == 1:
            break
    return v, best_action

def min_value(board):
    if terminal(board):
        return utility(board), None
    v = float('inf')
    best_action = None
    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < v:
            v = max_val
            best_action = action
        if v == -1:
            break
    return v, best_action

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = initial_state()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()

    def create_widgets(self):
        self.start_frame = tk.Frame(self.root)
        self.start_frame.pack()

        self.label = tk.Label(self.start_frame, text="Escoge tu símbolo", font="Helvetica 14")
        self.label.pack(pady=10)

        self.x_button = tk.Button(self.start_frame, text="X", font="Helvetica 14", command=lambda: self.start_game(X))
        self.x_button.pack(side=tk.LEFT, padx=20)

        self.o_button = tk.Button(self.start_frame, text="O", font="Helvetica 14", command=lambda: self.start_game(O))
        self.o_button.pack(side=tk.RIGHT, padx=20)

    def start_game(self, player_symbol):
        self.user_symbol = player_symbol
        self.ai_symbol = O if player_symbol == X else X
        self.current_player = X
        self.start_frame.destroy()
        self.create_board()

    def create_board(self):
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        for i in range(3):
            for j in range(3):
                button = tk.Button(self.board_frame, text="", font="Helvetica 20 bold", height=3, width=6, command=lambda i=i, j=j: self.on_button_click(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

        self.status_label = tk.Label(self.root, text=f"Turno del jugador: {self.current_player}", font="Helvetica 14")
        self.status_label.pack()

    def on_button_click(self, i, j):
        if self.board[i][j] is EMPTY and not terminal(self.board):
            self.board[i][j] = self.current_player
            self.buttons[i][j].config(text=self.current_player)
            if terminal(self.board):
                winner_player = winner(self.board)
                if winner_player:
                    self.status_label.config(text=f"Ganador: {winner_player}")
                else:
                    self.status_label.config(text="Empate")
            else:
                self.current_player = O if self.current_player == X else X
                self.status_label.config(text=f"Turno del jugador: {self.current_player}")
                if self.current_player == self.ai_symbol:
                    self.root.after(500, self.ai_move)

    def ai_move(self):
        if not terminal(self.board):
            action = minimax(self.board)
            if action:
                self.on_button_click(action[0], action[1])

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
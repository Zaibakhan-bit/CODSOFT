import math

# ----- Helpers -----
LINES = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]

def print_board(board):
    for i in range(0, 9, 3):
        row = [board[j] if board[j] else str(j+1) for j in range(i, i+3)]
        print(" | ".join(row))
        if i < 6:
            print("---------")

def get_winner(board):
    for a, b, c in LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_full(board):
    return all(c is not None for c in board)

def available_moves(board):
    return [i for i in range(9) if board[i] is None]

# Minimax algorithm with Alpha-Beta pruning
def minimax(board, ai, human, is_maximizing, alpha=-math.inf, beta=math.inf, depth=0):
    winner = get_winner(board)
    if winner == ai:
        return 10 - depth
    if winner == human:
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for move in available_moves(board):
            board[move] = ai
            eval = minimax(board, ai, human, False, alpha, beta, depth+1)
            board[move] = None
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in available_moves(board):
            board[move] = human
            eval = minimax(board, ai, human, True, alpha, beta, depth+1)
            board[move] = None
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(board, ai, human):
    best_score = -math.inf
    move = None
    for idx in available_moves(board):
        board[idx] = ai
        score = minimax(board, ai, human, False)
        board[idx] = None
        if score > best_score:
            best_score = score
            move = idx
    return move

# ----- Game Loop -----
def play():
    board = [None] * 9
    human = input("Choose your symbol (X or O): ").upper()
    while human not in ["X", "O"]:
        human = input("Invalid choice. Choose X or O: ").upper()
    ai = "O" if human == "X" else "X"
    turn = "X"  # X always goes first

    while True:
        print_board(board)
        winner = get_winner(board)
        if winner:
            if winner == human:
                print("You win!")
            elif winner == ai:
                print("AI wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break

        if turn == human:
            move = int(input("Enter your move (1-9): ")) - 1
            if move not in range(9) or board[move] is not None:
                print("Invalid move. Try again.")
                continue
            board[move] = human
        else:
            print("AI is thinking...")
            move = best_move(board, ai, human)
            board[move] = ai

        turn = ai if turn == human else human

if __name__ == "__main__":
    play()

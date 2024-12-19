import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, mark):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(cell == mark for cell in board[i]):  # Row
            return True
        if all(row[i] == mark for row in board):  # Column
            return True
    if all(board[i][i] == mark for i in range(3)):  # Diagonal
        return True
    if all(board[i][2 - i] == mark for i in range(3)):  # Anti-diagonal
        return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_empty_positions(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def player_move(board):
    while True:
        try:
            move = input("Enter your move (row and column, e.g., 1 1): ").split()
            row, col = int(move[0]) - 1, int(move[1]) - 1
            if (row, col) in get_empty_positions(board):
                board[row][col] = "X"
                break
            else:
                print("Invalid move! Try again.")
        except (ValueError, IndexError):
            print("Invalid input! Enter row and column numbers between 1 and 3.")

def bot_move_easy(board):
    row, col = random.choice(get_empty_positions(board))
    board[row][col] = "O"

def bot_move_medium(board):
    # Try to win
    for row, col in get_empty_positions(board):
        board[row][col] = "O"
        if check_winner(board, "O"):
            return
        board[row][col] = " "
    # Try to block the player
    for row, col in get_empty_positions(board):
        board[row][col] = "X"
        if check_winner(board, "X"):
            board[row][col] = "O"
            return
        board[row][col] = " "
    # Random move
    bot_move_easy(board)

def bot_move_hard(board):
    def minimax(board, depth, is_maximizing):
        if check_winner(board, "O"):
            return 10 - depth
        if check_winner(board, "X"):
            return depth - 10
        if is_draw(board):
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for row, col in get_empty_positions(board):
                board[row][col] = "O"
                score = minimax(board, depth + 1, False)
                board[row][col] = " "
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float("inf")
            for row, col in get_empty_positions(board):
                board[row][col] = "X"
                score = minimax(board, depth + 1, True)
                board[row][col] = " "
                best_score = min(best_score, score)
            return best_score

    best_score = -float("inf")
    best_move = None
    for row, col in get_empty_positions(board):
        board[row][col] = "O"
        score = minimax(board, 0, False)
        board[row][col] = " "
        if score > best_score:
            best_score = score
            best_move = (row, col)

    board[best_move[0]][best_move[1]] = "O"

def main():
    print("Welcome to Tic-Tac-Toe!")
    difficulty = input("Choose difficulty (easy, medium, hard): ").lower()

    board = [[" " for _ in range(3)] for _ in range(3)]
    print_board(board)

    while True:
        # Player's move
        player_move(board)
        print_board(board)
        if check_winner(board, "X"):
            print("Congratulations, you win!")
            break
        if is_draw(board):
            print("It's a draw!")
            break

        # Bot's move
        print("Bot is making a move...")
        if difficulty == "easy":
            bot_move_easy(board)
        elif difficulty == "medium":
            bot_move_medium(board)
        elif difficulty == "hard":
            bot_move_hard(board)
        else:
            print("Invalid difficulty. Defaulting to easy.")
            bot_move_easy(board)

        print_board(board)
        if check_winner(board, "O"):
            print("Bot wins! Better luck next time.")
            break
        if is_draw(board):
            print("It's a draw!")
            break

if __name__ == "__main__":
    main()

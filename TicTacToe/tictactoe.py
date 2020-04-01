##
 #  Worg
 ##
import sys
import copy
import time

class Board:
    min_player = None
    max_player = None

    def __init__(self, board = None):
        if board is None:
            self.board = [[' ' for y in range(3)] for x in range(3)]
        else:
            self.board = board


    def print(self):
        horizontal_line = '-------------'
        print(horizontal_line)
        for i in range(3):
            print('|', end = '')
            for j in range(3):
                print(' ' + str(self.board[i][j]) + ' ', end = '|')
            print('\n' + horizontal_line)


    def check_full_board(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    return False
        return True


    def valid_position(self, x, y):
        return self.board[x][y] == ' '


    def winning_combo(self, ch):
        """ Check if there is a winning combo with character ch (X or O) """
        if self.board[0][0] == ch and self.board[1][1] == ch and self.board[2][2] == ch:
            return True
        if self.board[0][2] == ch and self.board[1][1] == ch and self.board[2][0] == ch:
            return True
        if self.board[0][0] == ch and self.board[0][1] == ch and self.board[0][2] == ch:
            return True
        if self.board[1][0] == ch and self.board[1][1] == ch and self.board[1][2] == ch:
            return True
        if self.board[2][0] == ch and self.board[2][1] == ch and self.board[2][2] == ch:
            return True
        if self.board[0][0] == ch and self.board[1][0] == ch and self.board[2][0] == ch:
            return True
        if self.board[0][1] == ch and self.board[1][1] == ch and self.board[2][1] == ch:
            return True
        if self.board[0][2] == ch and self.board[1][2] == ch and self.board[2][2] == ch:
            return True
        return False



def next_turn(turn):
    if turn == 'X':
        return 'O'
    return 'X'


def generate_next_states(board : Board, turn):
    state_list = []
    for i in range(3):
        for j in range(3):
            if board.valid_position(i, j):
                new_board = Board(copy.deepcopy(board.board))
                new_board.board[i][j] = turn
                state_list.append(new_board)
    return state_list



def minimax(board : Board,  maximizing_player, turn):
    if board.check_full_board():
        return (0, None)

    if maximizing_player:
        value = -2  #  Worst scenario for maximizing
        best_move = None
        for next_state in generate_next_states(board, turn):
            if next_state.winning_combo(turn):  #  If it's a winning move
                value = 1
                best_move = next_state
                break

            result = minimax(next_state, not maximizing_player, next_turn(turn))
            if result[0] > value:
                value, best_move = result[0], next_state
        return (value, best_move)

    else:
        value = 2  #  Worst scenario for minimizing
        best_move = None
        for next_state in generate_next_states(board, turn):
            if next_state.winning_combo(turn):
                value = -1
                break

            result = minimax(next_state, not maximizing_player, next_turn(turn))
            if result[0] < value:
                value, best_move = result[0], next_state
        return (value, best_move)



def get_next_state(board, algo_type, turn):
    #  Choose the best move the AI can make and return the updated board
    result, best_move = minimax(board, True, turn)
    return best_move



def play_game(algo_type, player_character):
    board = Board()
    turn = 'X'

    while board.check_full_board() == False:
        #  Let the player make his move
        if turn == player_character:
            row = None
            col = None
            print("Let's see what tricks you have up your sleeve. Pick your next move. Bear in mind that the coordinates are 0-indexed")
            while True:
                row = int(input('Line = '))
                col = int(input('Column = '))

                if (row in range(0, 3)) and (col in range(0, 3)) and (board.valid_position(row, col)):
                    board.board[row][col] = player_character
                    break
                else:
                    print('Invalid row or column. Try again.')

            print('Nice move! The board looks like this:')
            board.print()
            if board.winning_combo(turn):
                print("Congratulations! You won!")  #  Shouldn't happen though
                return
        #  Let the AI show his skills
        else:
            board = get_next_state(board, algo_type, turn)
            print("Damn, that was a good move on computer's part. Current state:")
            board.print()
            if board.winning_combo(turn):
                print("You have been bested by the computer. Better luck next time.")
                return

        #  Switch turns. It's only fair.
        turn = next_turn(turn)

    print('The game ended with a draw.')
    board.print()


def main():
    algo_type = None
    while True:
        algo_type = input('Which algorithm shall the computer use?\n1. Minimax\n2. Alpha-beta\n')
        if algo_type in ['1', '2']:
            break
        else:
            print('Wrong pick. Try again.')

    player_character = None
    while True:
        player_character = input('Choose a character. Keep in mind that X always starts. Press 1 or 2.\n1. Play with X\n2. Play with O\n')
        if player_character == '1':
            player_character = 'X'
            break
        elif player_character == '2':
            player_character = 'O'
            break
        else:
            print('Wrong pick. Try again' + player_character)

    play_game(algo_type, player_character)


if __name__ == '__main__':
    main()

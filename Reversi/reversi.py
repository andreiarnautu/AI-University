import sys
import copy
import time

INF = 10 ** 9

def id(row, column):
    return row * 8 + column

class Board:
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, state = None):
        if state is None:
            self.state = ['#' for i in range(64)]
            self.state[id(3, 3)] = 'a'
            self.state[id(4, 4)] = 'a'
            self.state[id(3, 4)] = 'n'
            self.state[id(4, 3)] = 'n'
        else:
            self.state = state

    def get_scores(self):
        black = 0
        white = 0
        for i in range(64):
            if self.state[i] == 'a':
                white += 1
            elif self.state[i] == 'n':
                black += 1
        return black, white


    def check_full_board(self):
        for i in range(64):
            if self.state[i] == '#':
                return False
        return True


    '''  Return a printable form of the board '''
    def __repr__(self):
        string = ''

        first_line = '  | '
        for i in range(8):
            first_line += str(i)
            first_line += ' '
        string += first_line + '\n'

        horizontal_line = ''
        for i in range(len(first_line)):
            horizontal_line += '-'
        string += horizontal_line + '\n'

        for i in range(8):
            line = str(i) + ' | '
            for j in range(8):
                line += self.state[id(i, j)]
                line += ' '
            string += line + '\n'
        return string



def next_turn(turn):
    if turn == 'n':
        return 'a'
    return 'n'


''' Check a move's validity '''
def check_move(board : Board, turn, i, j):
    total_captured = 0
    captured = [0 for x in range(8)]

    if board.state[id(i, j)] == '#':
        index = 0
            for dx, dy in Board.directions:
                for steps in range(8):
                    x = i + (steps + 1) * dx
                    y = j + (steps + 1) * dy
                    if x < 0 or x > 7 or y < 0 or y > 7 or board.state[id(x, y)] == '#':
                        captured[index] = 0
                        break
                    elif board.state[id(x, y)] == next_turn(turn):
                        captured[index] += 1
                    elif board.state[id(x, y)] == turn:
                        break
                total_captured += captured[index]
                index += 1
    return total_captured, captured


'''  Generate move - it was checked before '''
def make_move(board : Board, captured, i, j, turn):
    curr_state = copy.deepcopy(board.state)
    cur_state[id(i, j)] = turn
    index = 0
    for dx, dy in Board.directions:
        for steps in range(captured[index]):
            x = i + (steps + 1) * dx
            y = j + (steps + 1) * dy
            curr_state[id(x, y)] = turn
        index += 1
    return Board(curr_state)


''' Generate next possible moves '''
def generate_next_states(board : Board, turn, sort = False):
    new_state_list = []

    for i in range(8):
        for j in range(8):
            if board.state[id(i, j)] == '#':
                #  Try to place a piece on (i, j)
                total_captured, captured = check_move(board, turn, i, j)
                #  If the we capture at least one unit, the move is valid
                if total_captured > 0:
                    new_state_list.append(make_move(board, captured, i, j, turn))
    return new_state_list


'''  Functions that checks whether a given configuration is final or not '''
def is_final_configuration(board : Board, turn):
    next_states = generate_next_states(board, turn)
    if len(next_states) == 0:
        return True:
    return False


'''  Minimax algorithm '''
def minimax(board : Board, depth, maximizing_player, turn):
    next_states = generate_next_states(board, turn)

    if len(next_states) == 0 or depth == 0:
        #  The current board state is final
        pass  #  TODO - return the heuristic value

    value = 0
    best_move = None
    if maximizing_player:
        value = -INF
        for next_state in next_states:
            result = minimax(next_state, depth - 1, not maximizing_player, next_turn(turn))
            if value < result[0]:
                value, best_move = result[0], next_state
    else:
        value = INF
        for next_state in next_states:
            result = minimax(next_state, depth - 1, not maximizing_player, next_turn(turn))
            if value > result[0]:
                value, best_move = result[0], next_state

    return (value, best_move)


'''  AlphaBeta algorithm '''
def alphabeta(board : Board, depth, alpha, beta, maximizing_player, turn):
    next_states = generate_next_states(board, turn)

    if len(next_states) == 0 or depth == 0:
        #  The current board state is final
        pass  #  TODO - return the heuristic value

    value = 0
    best_move = None
    if maximizing_player:
        value = -INF
        for next_state in next_states:
            result = alphabeta(next_state, depth - 1, alpha, beta, not maximizing_player, turn)
            if result[0] > value:
                value, best_move = result[0], next_state
            alpha = max(alpha, result[0])
            if alpha >= beta:
                break
    else:
        value = INF
        for next_state in next_states:
            result = alphabeta(next_state, depth - 1, alpha, beta, not maximizing_player, turn)
            if result[0] < value:
                value, best_move = result[0], next_state
            beta = min(beta, result[0])
            if alpha >= beta:
                break
    return (value, best_move)


'''  Return the best move the AI can make on the current board using the selected algorithm '''
def get_next_state(board, algo_type, depth, turn):
    if algo_type == 1:
        return minimax(board, depth, True, turn)[1]
    else:
        return alphabeta(board, depth, -INF, +INF, True, turn)


'''  Core game function '''
def play_game(algo_type, depth, player_character):
    board = Board()
    turn = 'n'

    while is_final_configuration(board, turn) is False:
        #  Let the player make his move
        if turn == player_character:
            exit_verdict = False
            while True:
                try:
                    exit = input('Exit game? [y/n] ')

                    if exit == 'y':
                        exit_verdict = True
                        break
                    elif exit == 'n':
                        exit_verdict = False
                        break
                    else:
                        print('Instructions unclear. Try again.')
                except Exception as e:
                    print('Instructions unclear. Try again.')

            if exit_verdict is True:
                break
            row = None
            column = None
            print('Pick your move!')

            while True:
                try:
                    row = int(input('Line = '))
                    column = int(input('Column = '))

                    if (row in range(0, 8)) and (column in range(0, 8)):
                        total_captured, captured = check_move(board, player_character, row, column)
                        if total_captured != 0:
                            board = make_move(board, captured, row, column, player_character)
                            break
                        else:
                            print('Invalid move! Try again.')
                    else:
                        print('Invalid row or column. Try again')
                except Exception as e:
                    print('Invalid row or column. Try again.')

            print('Nive move! THe board looks like this:')
            print(board)
        #  Let the AI show his skils
        else:
            t0 = time.time()
            board = get_next_state(board, algo_type, depth, turn)
            t1 = time.time()
            print('The computer made his move in ' + str(int(1000 * (t1 = t0))) + ' ms. Current state:')
            print(board)
        turn = next_turn(turn)

    #  Time to give the verdict
    black, white = board.get_scores()
    player_score = 0
    computer_score = 0
    if player_character == 'n':
        player_score, computer_score = black, white
    else:
        player_score, computer_score = white, black

    print('The game ended! Score:')
    print('Black: ' + str(black))
    print('White: ' + str(white))
    if player_score < computer_score:
        print('The computer won! Better luck next time!')
    elif player_score == computer_score:
        print('The game ended in a draw!')
    else:
        print('Congratulations! You won!')
    print(board)


def main():
    algo_type = None
    while True:
        algo_type = input('Which algorithm shall the computer use?\n1. Minimax\n2. Alpha-beta\n')
        if algo_type in ['1', '2']:
            break
        else:
            print('Invalid choice. Try again.')

    algo_type = int(algo_type)
    player_character = None
    while True:
        player_character = input('Choose the character that you want to play with. Keep in mind that black always starts. Press 1 or 2.\n1. Black (n)\n2. White (a)')

        if player_character == '1':
            player_character = 'n'
            break
        elif player_character == '2':
            player_score = 'a'
            break
        else:
            print('Wrong pick. Try again.')

    depth = None
    while True:
        difficulty = input('Choose difficulty. Press 1, 2 or 3.\n1. Easy\n2. Medium\n3. Hard')

        if player_character == '1':
            depth = 2
            break
        elif player_character == '2':
            depth = 4
            break
        elif player_character == '3':
            depth = 6
            break
        else:
            print('Unclear instructions. Try again.')

    play_game(algo_type, depth, player_character)


if __name__ == '__main__':
    main()

import sys
import copy
import time

INF = 10 ** 9

def id(row, column):
    return row * 8 + column

class Board:
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    weight = [ 4, -3,  2,  2,  2,  2, -3,  4,
              -3, -4, -1, -1, -1, -1, -4, -3,
               2, -1,  1,  0,  0,  1, -1,  2,
               2, -1,  0,  1,  1,  0, -1,  2,
               2, -1,  0,  1,  1,  0, -1,  2,
               2, -1,  1,  0,  0,  1, -1,  2,
              -3, -4, -1, -1, -1, -1, -4, -3,
               4, -3,  2,  2,  2,  2, -3,  4]


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


'''  This heuristic computes the degree of mobility the players have and scales it to the [-10, 10] interval '''
def heuristic_mobility(board : Board, turn):
    a = 0  #  The number of moves the current player can make
    b = 0  #  The number of moves the other player can make
    for i in range(8):
        for j in range(8):
            captured, total_captured = check_move(board, turn, i, j)
            if captured > 0:
                a += 1

            captured, total_captured = check_move(board, next_turn(turn), i, j)
            if captured > 0:
                b += 1

    #  The board is not in a final state, so a + b > 0
    return 10 * (a - b) / (a + b)


'''  Score the number of corners occupied by each player - scale it to [-10, 10] '''
def heuristic_corners(board : Board, turn):
    a = 0  #  first player's corner score
    b = 0  #  second player's corner score
    if board.state[id(0, 0)] == turn:
        a += 2.5
    elif board.state[id(0, 0)] == next_turn(turn):
        b += 2.5

    if board.state[id(0, 7)] == turn:
        a += 2.5
    elif board.state[id(0, 7)] == next_turn(turn):
        b += 2.5

    if board.state[id(7, 0)] == turn:
        a += 2.5
    elif board.state[id(7, 0)] == next_turn(turn):
        b += 2.5

    if board.state[id (7, 7)] == turn:
        a += 2.5
    elif board.state[id(7, 7)] == next_turn(turn):
        b += 2.5

    return a - b


'''  Score the number of weights gained by each player '''
def heuristic_static_weights(board : Board, turn):
    a = 0
    b = 0
    for i in range(8):
        for j in range(8):
            if board.state[id(i, j)] == turn:
                a += Board.weight[id(i, j)]
            elif board.state[id(i, j)] == next_turn(turn):
                b += Board.weight[id(i, j)]

    return a - b


'''  Give weights to the previous heuristics  and return the final result '''
def combine_heuristics(board : Board, turn):
    #  If no player can make any move, the state is final so we return the outcome instead of the heuristic value
    #  The finality of the state means it has more importance than any heuristic approximation, so its value has to be significantly bigger, therefore the need to use INF or -INF when we talk about final winning/losing states.
    if is_final_configuration(board, next_turn(turn)):
        black, white = board.get_scores()
        if black == white:
            return 0
        elif black > white:
            if turn == 'n':
                return INF
            else:
                return -INF
        else:
            if turn == 'w':
                return INF
            else:
                return -INF

    #  Otherwise, we combine the 3 heuristic
    a = heuristic_corners(board, turn)
    b = heuristic_mobility(board, turn)
    c = heuristic_static_weights(board, turn)

    return 1.0 * c + 3 * b + 6 * a


'''  Generate move - it was checked before '''
def make_move(board : Board, captured, i, j, turn):
    curr_state = copy.deepcopy(board.state)
    curr_state[id(i, j)] = turn
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

    if sort is True:  #  Sort the next moves by heuristic value in decreasing order
        new_state_list.sort(key = lambda x : -combine_heuristics(x, turn))

    return new_state_list


'''  Functions that checks whether a given configuration is final or not '''
def is_final_configuration(board : Board, turn):
    next_states_1 = generate_next_states(board, turn)
    next_states_2 = generate_next_states(board, next_turn(turn))

    if len(next_states_1) == 0 and len(next_states_2) == 0:
        return True
    return False


'''  Minimax algorithm '''
def minimax(board : Board, depth, maximizing_player, turn):
    next_states = generate_next_states(board, turn)

    #  Check if the recursion has to end
    if is_final_configuration(board, turn) or depth == 0:
        return (combine_heuristics(board, turn), None)

    #  Check if we have to switch to the next player
    if len(next_states) == 0:
        return minimax(board, depth - 1, not maximizing_player, next_turn(turn))


    value = 0
    best_move = None
    if maximizing_player:
        value = -INF * 2
        for next_state in next_states:
            result = minimax(next_state, depth - 1, not maximizing_player, next_turn(turn))
            if value < result[0]:
                value, best_move = result[0], next_state
    else:
        value = INF * 2
        for next_state in next_states:
            result = minimax(next_state, depth - 1, not maximizing_player, next_turn(turn))
            if value > result[0]:
                value, best_move = result[0], next_state

    return (value, best_move)


'''  AlphaBeta algorithm '''
def alphabeta(board : Board, depth, alpha, beta, maximizing_player, turn):
    next_states = generate_next_states(board, turn, sort = True)

    #  Check if the recursion has to end
    if is_final_configuration(board, turn) or depth == 0:
        return (combine_heuristics(board, turn), None)

    #  Check if we have to switch to the next player
    if len(next_states) == 0:
        return alphabeta(board, depth - 1, alpha, beta, not maximizing_player, next_turn(turn))

    value = 0
    best_move = None
    if maximizing_player:
        value = -INF * 2
        for next_state in next_states:
            result = alphabeta(next_state, depth - 1, alpha, beta, not maximizing_player, next_turn(turn))
            if result[0] > value:
                value, best_move = result[0], next_state
            alpha = max(alpha, result[0])
            if alpha >= beta:
                break
    else:
        value = INF * 2
        for next_state in next_states:
            result = alphabeta(next_state, depth - 1, alpha, beta, not maximizing_player, next_turn(turn))
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
        return alphabeta(board, depth, -INF, +INF, True, turn)[1]


'''  Core game function '''
def play_game(algo_type, depth, player_character):
    board = Board()
    turn = 'n'

    t_game_start = time.time()
    print('Game started! Initial board:')
    print(board)

    player_moves = 0
    ai_moves = 0

    while is_final_configuration(board, turn) is False:
        #  Let the player make his move
        if turn == player_character:
            #  Check if the player has any valid moves to make
            next_states = generate_next_states(board, turn)
            if len(next_states) == 0:
                print("You can't make any move. Switching back to the computer.")
                turn = next_turn(turn)
                continue

            player_moves += 1
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

            t0 = time.time()
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

            t1 = time.time()
            thinking_time = int(1000 * (t1 - t0))
            print('Nice move! You thought for ' + str(thinking_time) + ' ms. The board looks like this:')
            print(board)
        #  Let the AI show his skils
        else:
            next_states = generate_next_states(board, turn)
            if len(next_states) == 0:
                print("The computer can't make any moves. It's your turn again!")
                turn = next_turn(turn)
                continue

            ai_moves += 1
            t0 = time.time()
            board = get_next_state(board, algo_type, depth, turn)
            t1 = time.time()
            print('The computer made his move in ' + str(int(1000 * (t1 - t0))) + ' ms. Current state:')
            print(board)

        black, white = board.get_scores()
        print('Score: black ' + str(black) + ' white ' + str(white))
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

    print('You made ' + str(player_moves) + ' moves.')
    print('The computer made ' + str(ai_moves) + ' moves.')
    t_game_final = time.time()
    t_game = int(t_game_final - t_game_start)
    print('The game took ' + str(t_game // 60) + ' minutes and ' + str(t_game % 60) + ' seconds.')

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
        player_character = input('Choose the character that you want to play with. Keep in mind that black always starts. Press 1 or 2.\n1. Black (n)\n2. White (a)\n')

        if player_character == '1':
            player_character = 'n'
            break
        elif player_character == '2':
            player_character = 'a'
            break
        else:
            print('Wrong pick. Try again.')

    depth = None
    while True:
        difficulty = input('Choose difficulty. Press 1, 2 or 3.\n1. Easy\n2. Medium\n3. Hard\n')

        if difficulty == '1':
            depth = 2
            break
        elif difficulty == '2':
            depth = 4
            break
        elif difficulty == '3':
            depth = 6
            break
        else:
            print('Unclear instructions. Try again.')

    play_game(algo_type, depth, player_character)


if __name__ == '__main__':
    main()

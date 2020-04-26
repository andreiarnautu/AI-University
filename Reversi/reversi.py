import sys
import copy
import time

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


def generate_next_states(board : Board, turn, sort = False):
    new_state_list = []

    for i in range(8):
        for j in range(8):
            if board.state[id(i, j)] == '#':
                #  Try to place a piece on (i, j)
                total_captured = 0
                captured = [0 for x in range(8)]
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

                #  If the we capture at least one unit, the move is valid
                if total_captured > 0:
                    curr_state = copy.deepcopy(board.state)
                    index = 0
                    for dx, dy in Board.directions:
                        for steps in range(captured[index]):
                            x = i + (steps + 1) * dx
                            y = j + (steps + 1) * dy
                            curr_state[id(x, y)] = turn
                    new_state_list.append(Board(curr_state))
    return new_state_list






board = Board()
print(board)

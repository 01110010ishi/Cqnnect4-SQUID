from random import randint

import pygame
import sys

from classes.board import Board
from classes.q_piece import qPiece


# import random

class GameUI:

    def __init__(self, player):
        self.CHIP_SIZE = 80
        self.OFFSET_X = 500
        self.OFFSET_Y = 60
        self.CHIP_OFFSET = 20
        self.BOARD_HEIGHT = 600
        self.CHIP_RADIUS = int(self.CHIP_SIZE / 2)

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Connect 4 with Python')

        self._screen = pygame.display.set_mode((1700, 700))
        self._board_img = pygame.image.load("./img/board.png")
        self._board_img_numbers = pygame.image.load("./img/board_numbers.png")
        self._font = pygame.font.SysFont('Calibri', 26)

        self.init_ui(player)

    def init_ui(self, player):
        self._screen.fill((255, 255, 255))
        self.draw_board(-1, -1)
        self.draw_player(player)

        # this below is just for testing where to put this
        #pygame.draw.rect(self._screen, (255, 255, 255), [0, 500, 500, 50], 0)
        #pygame.draw.rect(self._screen, (255, 255, 255), [0, 700, 500, 50], 0)
        text1 = "Probability of Qpiece 1: s"
        text2 = "Probability of Qpiece 2: l"

        text1 = self._font.render(text1, True, (0, 0, 0))
        self._screen.blit(text1, (100, 500))
        text2 = self._font.render(text2, True, (0, 0, 0))
        self._screen.blit(text2, (100, 600))

    def draw_blochsphere(self, blochsphere, player):
        if player == 0:
            self._screen.blit(blochsphere, (0, 0))
        elif player == 1:
            self._screen.blit(blochsphere, (1200, 0))
        pygame.display.flip()

    def draw_player_won(self, player):
        pygame.draw.rect(self._screen, (255, 255, 255), [0, 0, 800, 50], 0)

        text = self.get_name(player) + " won! Restart (y | n)?"

        text = self._font.render(text, True, (0, 0, 0))
        self._screen.blit(text, (50, 10))

        pygame.display.flip()

    def draw_player(self, player):
        pygame.draw.rect(self._screen, (255, 255, 255), [self.OFFSET_X, 0, 800, 50], 0)

        text = "Current Player: " + self.get_name(player)

        text = self._font.render(text, True, (0, 0, 0))
        self._screen.blit(text, (self.OFFSET_X + 200, 10))

        pygame.display.flip()

    def draw_board(self, row, column, player=None, q=False):
        if player is not None:
            pygame.draw.circle(self._screen, self.get_color(player),
                               (self.OFFSET_X + self.CHIP_RADIUS + self.CHIP_OFFSET * (column - 1) + self.CHIP_SIZE * (
                                       column - 1),
                                self.BOARD_HEIGHT - self.CHIP_SIZE * row - self.CHIP_OFFSET * row), self.CHIP_RADIUS)
            font = pygame.font.Font(None, self.CHIP_RADIUS)
            if q:
                q_text = font.render('Q', True, (0, 0, 0))
                text_rect = q_text.get_rect(
                    center=(
                        self.OFFSET_X + self.CHIP_RADIUS + self.CHIP_OFFSET * (column - 1) + self.CHIP_SIZE * (
                                column - 1),
                        self.BOARD_HEIGHT - self.CHIP_SIZE * row - self.CHIP_OFFSET * row))
                self._screen.blit(q_text, text_rect)

        self._screen.blit(self._board_img, (self.OFFSET_X - 10, self.OFFSET_Y - 10))
        self._screen.blit(self._board_img_numbers,
                          (self.OFFSET_X + self.CHIP_RADIUS - 10, self.OFFSET_Y + self.BOARD_HEIGHT - 5))
        pygame.display.flip()

    def remove_collapsed_qp(self, column, row):
        pygame.draw.circle(self._screen, (255, 255, 255),
                           (self.OFFSET_X + self.CHIP_RADIUS + self.CHIP_OFFSET * (column - 1) + self.CHIP_SIZE * (
                                   column - 1),
                            self.BOARD_HEIGHT - self.CHIP_SIZE * row - self.CHIP_OFFSET * row), self.CHIP_RADIUS)

        self._screen.blit(self._board_img, (self.OFFSET_X - 10, self.OFFSET_Y - 10))
        self._screen.blit(self._board_img_numbers,
                          (self.OFFSET_X + self.CHIP_RADIUS - 10, self.OFFSET_Y + self.BOARD_HEIGHT - 5))
        pygame.display.flip()

    def get_name(self, player):
        if player == 0:
            return "Red"
        else:
            return "Yellow"

    def get_color(self, player):
        if player == 0:
            return (255, 0, 0)
        else:
            return (255, 255, 0)


class myGame:

    def __init__(self):
        self.board = Board()
        end_game = False
        player = 0
        row = -1
        column = -1
        turn = 0
        valid_keys = [1, 2, 3, 4, 5, 6, 7]
        self.gui = GameUI(player)
        self.q_pieces = []
        self.p1_qpiece = False
        self.p2_qpiece = False

        while not end_game:
            # figure out which player
            if turn % 2 == 0:
                player = 0
            else:
                player = 1

            # run game logic
            if self.generate_q_piece(player):
                # piece is a q-piece

                # get the first column of the qpiece
                valid_column = False
                while not valid_column:
                    column1 = int(input("Enter Column 1: "))
                    if column1 in valid_keys:
                        print('Col1 =', column1)
                        row1 = self.board.add_chip(player, column1)
                        print('Row1 =', row1)
                        # Adding a chip was possible
                        if row1 > -1:
                            valid_column = True

                # check if there is a q_piece underneath the qpiece 1
                if row1 > 0:
                    if self.check_qpiece_underneath(column1, row1):
                        # collapse the qpiece underneath
                        qp_underneath = self.get_collapsed_qpiece(column1, row1 - 1)
                        qp_underneath.measure()

                        # collapsed is the coordinate of the collapsed piece [col, row]
                        collapsed = qp_underneath.collapsed()
                        print('collapsed =', collapsed)

                        # if the collapsed qpiece was directly underneath the piece we are trying to place
                        if collapsed[0] == column1:
                            self.q_pieces.remove(qp_underneath)
                            self.board.remove_piece(column1, row1)
                            self.board.remove_piece(collapsed[0], collapsed[1])
                            self.gui.remove_collapsed_qp(collapsed[0], collapsed[1])
                            row1 = self.board.add_chip(player, column1)
                        else:
                            # remove qpiece
                            self.q_pieces.remove(qp_underneath)
                            self.board.remove_piece(collapsed[0], collapsed[1])
                            self.gui.remove_collapsed_qp(collapsed[0], collapsed[1])

                        #self.q_pieces.remove(qp_underneath)
                        if qp_underneath.player == 0:
                            self.p1_qpiece = False
                        else:
                            self.p2_qpiece = False

                        # need to get the coordinates of the other qpiece and then change that to a normal piece
                        self.gui.draw_board(qp_underneath.not_collapsed[1], qp_underneath.not_collapsed[0],
                                            player=qp_underneath.player)

                # update board
                self.gui.draw_board(row1, column1, player=player, q=True)

                # get the second column of the qpiece
                valid_column = False
                while not valid_column:
                    column2 = int(input("Enter Column 2: "))
                    if column2 in valid_keys:
                        print('Col2 =', column2)
                        row2 = self.board.add_chip(player, column2)
                        print('Row2 =', row2)
                        # adding second chip was possible
                        if row2 > -1:
                            valid_column = True

                # check if there is a q_piece underneath the piece
                if row2 > 0:
                    if self.check_qpiece_underneath(column2, row2):
                        # collapse the qpiece underneath

                        qp_underneath = self.get_collapsed_qpiece(column2, row2 - 1)
                        qp_underneath.measure()

                        collapsed2 = qp_underneath.collapsed()
                        if collapsed2[0] == column2:
                            self.q_pieces.remove(qp_underneath)
                            self.board.remove_piece(column2, row2)
                            self.gui.remove_collapsed_qp(collapsed2[0], collapsed2[1])
                            self.board.remove_piece(collapsed2[0], collapsed2[1])
                            row2 = self.board.add_chip(player, column2)
                        else:
                            self.q_pieces.remove(qp_underneath)
                            self.gui.remove_collapsed_qp(collapsed2[0], collapsed2[1])
                            self.board.remove_piece(collapsed2[0], collapsed2[1])

                        #self.q_pieces.remove(qp_underneath)
                        if qp_underneath.player == 0:
                            self.p1_qpiece = False
                        else:
                            self.p2_qpiece = False

                        # need to get the coordinates of the other qpiece and then change that to a normal piece
                        self.gui.draw_board(qp_underneath.not_collapsed[1], qp_underneath.not_collapsed[0],
                                            player=qp_underneath.player)

                # update board
                self.gui.draw_board(row2, column2, player=player, q=True)

                # now create the qPiece object
                qp = qPiece(column1, row1, column2, row2, player)
                self.q_pieces.append(qp)
                if player == 0:
                    self.p1_qpiece = True
                else:
                    self.p2_qpiece = True

                # for debugging purposes
                print('q_pieces on the board')
                for q in self.q_pieces:
                    print(q.get_col1(), q.get_col2())

                ...
                # user can apply gates now
                ...

                print("time to apply gates")
                '''should be change to fit code
                if the gates applied are "h, r(theta=1, phi=4), z" the array would store ['h', ['r', 1, 4], z]

                This function should be made into a simple key press, or button on the screen
                '''

                # screen = pygame.display.set_mode((800, 600))
                clock = pygame.time.Clock()
                bloch_sphere = qp.get_bloch_sphere()
                self.gui.draw_blochsphere(bloch_sphere, player)
                # self.gui._screen.blit(bloch_sphere, (0, 0))
                # pygame.display.flip()
                # clock.tick(60)
                end_gate_input = False
                while not end_gate_input:
                    valid_gate = False
                    while not valid_gate:
                        gate_input = (input('What gate are you applying (Type h x y z or r)): '))
                        if gate_input == 'h' or 'x' or 'y' or 'z' or 'r':
                            valid_gate = True
                            if gate_input == 'r':
                                theta = float(input('What theta value: '))
                                phi = float(input('What phi value: '))
                                qp.apply_gate('r', theta, phi)
                            else:
                                qp.apply_gate(gate_input)

                            bloch_sphere = qp.get_bloch_sphere()
                            self.gui.draw_blochsphere(bloch_sphere, player)
                            # pygame.display.flip()
                            # clock.tick(60)
                        else:
                            print("Incorrect input")
                    probs = qp.calculate_probs()
                    print(f"Probability for Q1 is {probs[0]} and probability for Q2 is {probs[1]}")
                    done_gates = input('Are you done applying gates? (y or n): ')
                    if done_gates == 'y':
                        end_gate_input = True

                # check if player won
                player_won = self.board.check_player_wins(player)
                if player_won:
                    # since they could have won with the qpiece they just placed, we need to check win after collapsing
                    # the piece just placed
                    qp.measure()
                    collapse = qp.collapsed()
                    self.gui.remove_collapsed_qp(collapse[0], collapse[1])
                    self.board.remove_piece(collapse[0], collapse[1])
                    self.q_pieces.remove(qp)
                    if qp.player == 0:
                        self.p1_qpiece = False
                    else:
                        self.p2_qpiece = False

                    self.gui.draw_board(qp.not_collapsed[1], qp.not_collapsed[0], player=player)

                    # now check again
                    player_won = self.board.check_player_wins(player)
                    if player_won:
                        self.gui.draw_player_won(player)
                        end_game = True

                turn += 1

            else:
                # piece is a normal piece

                # get the column
                valid_column = False
                while not valid_column:
                    column = int(input("Enter Column: "))
                    if column in valid_keys:
                        print('Col =', column)
                        row = self.board.add_chip(player, column)
                        print('Row =', row)
                        # Adding a chip was possible
                        if row > -1:
                            valid_column = True

                # check if there is a q_piece underneath the piece
                if row > 0:
                    if self.check_qpiece_underneath(column, row):

                        # collapse the qpiece underneath
                        qp_underneath = self.get_collapsed_qpiece(column, row - 1)
                        qp_underneath.measure()

                        # collapsed is the coordinate of the collapsed piece [col, row]
                        collapsed = qp_underneath.collapsed()
                        print('collapsed =', collapsed)

                        # if the collapsed qpiece was directly underneath the piece we are trying to place
                        if collapsed[0] == column:
                            self.q_pieces.remove(qp_underneath)
                            self.board.remove_piece(column, row)
                            self.board.remove_piece(collapsed[0], collapsed[1])
                            self.gui.remove_collapsed_qp(collapsed[0], collapsed[1])
                            row = self.board.add_chip(player, column)
                        else:
                            # remove qpiece from the board
                            self.q_pieces.remove(qp_underneath)
                            self.board.remove_piece(collapsed[0], collapsed[1])
                            self.gui.remove_collapsed_qp(collapsed[0], collapsed[1])

                        if qp_underneath.player == 0:
                            self.p1_qpiece = False
                        else:
                            self.p2_qpiece = False

                        # need to get the coordinates of the other qpiece and then change that to a normal piece
                        self.gui.draw_board(qp_underneath.not_collapsed[1], qp_underneath.not_collapsed[0],
                                            player=qp_underneath.player)

                # update board
                self.gui.draw_board(row, column, player=player)

                # check if player won
                player_won = self.board.check_player_wins(player)
                if player_won:
                    qp = self.find_qp_in_connect4(column, row, player)
                    if qp != -1:
                        qp.measure()
                        collapse = qp.collapsed()
                        self.gui.remove_collapsed_qp(collapse[0], collapse[1])
                        self.board.remove_piece(collapse[0], collapse[1])
                        self.q_pieces.remove(qp)
                        if qp.player == 0:
                            self.p1_qpiece = False
                        else:
                            self.p2_qpiece = False
                        self.gui.draw_board(qp.not_collapsed[1], qp.not_collapsed[0], player=player)
                        self.board.four = None

                        # now check again
                        player_won = self.board.check_player_wins(player)
                        if player_won:
                            self.gui.draw_player_won(player)
                            end_game = True
                    else:
                        self.gui.draw_player_won(player)
                        end_game = True

                turn += 1

    def generate_q_piece(self, player):
        if self.get_player_qp(player):
            return False
        else:
            q = False
            r = randint(0, 3)
            if r == 1:
                q = True
            return q

    def get_color(player):
        if player == 0:
            return (255, 0, 0)
        else:
            return (255, 255, 0)

    def check_qpiece_underneath(self, col, row):
        print("now doing check_qpiece_underneath()")
        underneath = False
        print(col, row - 1)
        for q in self.q_pieces:
            if col == q.col1 and row - 1 == q.row1:
                underneath = True
            elif col == q.col2 and row - 1 == q.row2:
                underneath = True
        print(underneath)
        return underneath

    def get_collapsed_qpiece(self, col, row):
        print("now doing get_collapsed_qpiece")
        print("col, row", col, row)
        for q in self.q_pieces:
            print('q1', q.get_col1(), q.get_row1())
            print('q2', q.get_col2(), q.get_row2())
            if (q.get_col1() == col and q.get_row1() == row) or (q.get_col2() == col and q.get_row2() == row):
                print(q)
                return q
        return None

    def find_qp_in_connect4(self, col, row, player):
        direction = self.board.four
        if direction == 'horizontal':
            for q in self.q_pieces:
                if q.get_row1() == row:
                    if q.get_col1() in range(col - 4, col) or q.get_col1() in range(col, col + 4):
                        return q
                elif q.get_row2() == row:
                    if q.get_col2() in range(col - 4, col) or q.get_col2() in range(col, col + 4):
                        return q
        elif direction == 'vertical':
            for q in self.q_pieces:
                if q.get_col1() == col:
                    if q.get_row1() in range(row - 4, row) or q.get_row1() in range(row, row + 4):
                        return q
                elif q.get_col2() == col:
                    if q.get_row2() in range(row - 4, row) or q.get_row2() in range(row, row + 4):
                        return q
        elif direction == '+diagonal':
            diag = []
            c = col
            r = row
            while c <= self.board.COLUMNS and r <= self.board.ROWS:
                if self.board._grid[r][c] != player:
                    break
                diag.append((c, r))
                c += 1
                r += 1

            c = col - 1
            r = row - 1
            while c > 0 and r >= 0:
                if self.board._grid[r][c] != player:
                    break
                diag.insert(0, (c, r))
                c -= 1
                r -= 1

            for q in self.q_pieces:
                for p in diag:
                    if q.get_col1() == p[0] and q.get_row1() == p[1]:
                        return q
                    elif q.get_col2() == p[0] and q.get_row2() == p[1]:
                        return q

        elif direction == '-diagonal':
            diag = []
            c = col
            r = row
            while c <= self.board.COLUMNS and r >= 0:
                if self.board._grid[r][c] != player:
                    break
                diag.append((c, r))
                c += 1
                r -= 1

            c = col - 1
            r = row + 1
            while c > 0 and r < self.board.ROWS:
                if self.board._grid[r][c] != player:
                    break
                diag.insert(0, (c, r))
                c -= 1
                r += 1

            for q in self.q_pieces:
                for p in diag:
                    if q.get_col1() == p[0] and q.get_row1() == p[1]:
                        return q
                    elif q.get_col2() == p[0] and q.get_row2() == p[1]:
                        return q
        return -1

    def draw_probability(self, q):
        pygame.draw.rect(self.gui._screen, (255, 255, 255), [0, 0, 800, 50], 0)

        probs = q.calculate_probs()

        text1 = "Probability of Qpiece 1: " + probs[0]
        text2 = "Probability of Qpiece 2: " + probs[1]

        text1 = self.gui._font.render(text1, True, (0, 0, 0))
        self.gui._screen.blit(text1, (self.gui.OFFSET_X, 100))
        text2 = self.gui._font.render(text2, True, (0, 0, 0))
        self.gui._screen.blit(text2, (self.gui.OFFSET_X + 50, 100))

        pygame.display.flip()

    def get_player_qp(self, player):
        if player == 0:
            return self.p1_qpiece
        elif player == 1:
            return self.p2_qpiece
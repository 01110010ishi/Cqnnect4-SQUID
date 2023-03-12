from random import randint

import pygame
import sys
import numpy as np
from classes.board import Board
from classes.q_piece import qPiece
from classes.slider import Slider


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

        self._screen = pygame.display.set_mode((1700, 900))
        self._board_img = pygame.image.load("./img/board.png")
        self._board_img_numbers = pygame.image.load("./img/board_numbers.png")
        self._font = pygame.font.SysFont('Calibri', 26)

        # Define the buttons
        self.gate_buttons_left = {
            'H': pygame.Rect(100, 600, 100, 50),
            'X': pygame.Rect(220, 600, 100, 50),
            'Y': pygame.Rect(340, 600, 100, 50),
            'Z': pygame.Rect(100, 660, 100, 50),
            'R': pygame.Rect(220, 660, 100, 50),
            'Done': pygame.Rect(340, 660, 100, 50)
        }
        self.gate_surfaces_left = {
            'H': pygame.Surface((100, 50)),
            'X': pygame.Surface((100, 50)),
            'Y': pygame.Surface((100, 50)),
            'Z': pygame.Surface((100, 50)),
            'R': pygame.Surface((100, 50)),
            'Done': pygame.Surface((100, 50))
        }
        self.gate_buttons_right = {
            'H': pygame.Rect(1300, 600, 100, 50),
            'X': pygame.Rect(1420, 600, 100, 50),
            'Y': pygame.Rect(1540, 600, 100, 50),
            'Z': pygame.Rect(1300, 660, 100, 50),
            'R': pygame.Rect(1420, 660, 100, 50),
            'Done': pygame.Rect(1540, 660, 100, 50)
        }
        self.gate_surfaces_right = {
            'H': pygame.Surface((100, 50)),
            'X': pygame.Surface((100, 50)),
            'Y': pygame.Surface((100, 50)),
            'Z': pygame.Surface((100, 50)),
            'R': pygame.Surface((100, 50)),
            'Done': pygame.Surface((100, 50))
        }

        self.theta_slider_left = Slider(self._screen, 60, 800, 200, 10, 0, np.pi, 0)
        self.phi_slider_left = Slider(self._screen, 60, 850, 200, 10, 0, 2 * np.pi, 0)
        self.theta_slider_right = Slider(self._screen, 1400, 800, 200, 10, 0, np.pi, 0)
        self.phi_slider_right = Slider(self._screen, 1400, 850, 200, 10, 0, 2 * np.pi, 0)

        self.init_ui(player)

    def init_ui(self, player):
        self._screen.fill((255, 255, 255))
        self.draw_board(-1, -1)
        self.draw_player(player)

    def draw_blochsphere(self, blochsphere, player):
        if player == 0:
            self._screen.blit(blochsphere, (0, 0))
        elif player == 1:
            self._screen.blit(blochsphere, (1200, 0))
        pygame.display.flip()

    def draw_player_won(self, player):
        pygame.draw.rect(self._screen, (255, 255, 255), [0, 0, 1700, 1000], 0)

        text = self.get_name(player) + " won!"

        text = self._font.render(text, True, (0, 0, 0))
        self._screen.blit(text, (50, 10))

        pygame.display.flip()

    def draw_player(self, player):
        pygame.draw.rect(self._screen, (255, 255, 255), [self.OFFSET_X, 0, 800, 50], 0)

        text = "Current Player: " + self.get_name(player)

        text = self._font.render(text, True, (0, 0, 0))
        self._screen.blit(text, (self.OFFSET_X + 100, 10))

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

    def draw_buttons_left(self):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GRAY = (128, 128, 128)

        # Draw the buttons
        for button in self.gate_surfaces_left:
            pygame.draw.rect(self.gate_surfaces_left[button], GRAY, (0, 0, 100, 50))
            text = self._font.render(button, True, WHITE)
            text_rect = text.get_rect(center=self.gate_buttons_left[button].center)
            # self.gate_surfaces[button].blit(text, text_rect)
            self._screen.blit(self.gate_surfaces_left[button], self.gate_buttons_left[button])
            self._screen.blit(text, text_rect)
            pygame.display.flip()

    def draw_buttons_right(self):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GRAY = (128, 128, 128)

        # Draw the buttons
        for button in self.gate_surfaces_right:
            pygame.draw.rect(self.gate_surfaces_right[button], GRAY, (0, 0, 100, 50))
            text = self._font.render(button, True, WHITE)
            text_rect = text.get_rect(center=self.gate_buttons_right[button].center)
            self._screen.blit(self.gate_surfaces_right[button], self.gate_buttons_right[button])
            self._screen.blit(text, text_rect)
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

    def update(self):
        pygame.display.update()


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
            # self.gui.draw_player(player)

            # run game logic
            if self.generate_q_piece(player):
                # piece is a q-piece
                qtext = "you got a Q-piece"
                qtext1 = self.gui._font.render(qtext, True, (0, 0, 0))
                self.gui._screen.blit(qtext1, (900, 10))

                valid_column = False  # get the first column of the qpiece
                while not valid_column:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            column1 = event.key - 48
                            if column1 in valid_keys:
                                row1 = self.board.add_chip(player, column1)
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

                        # self.q_pieces.remove(qp_underneath)
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
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            column2 = event.key - 48
                            if column2 in valid_keys:
                                if column2 != column1:
                                    row2 = self.board.add_chip(player, column2)
                                    # Adding a chip was possible
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

                        # self.q_pieces.remove(qp_underneath)
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

                # APPLY GATES
                bloch_sphere = qp.get_bloch_sphere()
                self.gui.draw_blochsphere(bloch_sphere, player)
                if player == 0:
                    # self.gui.draw_buttons_left()
                    buttons = self.gui.gate_buttons_left
                    surfaces = self.gui.gate_surfaces_left
                    theta_slider = self.gui.theta_slider_left
                    phi_slider = self.gui.phi_slider_left

                    self.gui.update()
                else:
                    # self.gui.draw_buttons_right()

                    buttons = self.gui.gate_buttons_right
                    surfaces = self.gui.gate_surfaces_right
                    theta_slider = self.gui.theta_slider_right
                    phi_slider = self.gui.phi_slider_right
                    self.gui.update()
                theta = theta_slider.value
                phi = phi_slider.value
                self.blit_buttons()
                self.gui.update()
                end_gate_input = False
                while not end_gate_input:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            for button in buttons:
                                if buttons[button].collidepoint(event.pos):
                                    if button == 'Done':
                                        end_gate_input = True
                                        self.gui.update()
                                        break
                                    elif button != 'R':
                                        qp.apply_gate(button.lower())
                                        bloch_sphere = qp.get_bloch_sphere()
                                        self.gui.draw_blochsphere(bloch_sphere, player)
                                        self.gui.update()
                            if theta_slider.knob_rect.collidepoint(event.pos):
                                theta_slider.dragging = True
                            elif phi_slider.knob_rect.collidepoint(event.pos):
                                phi_slider.dragging = True
                        elif event.type == pygame.MOUSEBUTTONUP:
                            theta_slider.dragging = False
                            phi_slider.dragging = False
                        elif event.type == pygame.MOUSEMOTION:
                            if theta_slider.dragging:
                                theta_slider.knob_rect.x = event.pos[0]
                                if theta_slider.knob_rect.x < theta_slider.rect.x:
                                    theta_slider.knob_rect.x = theta_slider.rect.x
                                elif theta_slider.knob_rect.x > theta_slider.rect.x + theta_slider.rect.width:
                                    theta_slider.knob_rect.x = theta_slider.rect.x + theta_slider.rect.width
                                theta_slider.value = theta_slider.min_value + (
                                            theta_slider.knob_rect.x - theta_slider.rect.x) * (
                                                             theta_slider.max_value - theta_slider.min_value) / theta_slider.rect.width
                                theta_slider.draw_value_text()
                                theta = theta_slider.value
                                qp.apply_gate('r', theta, phi)
                                bloch_sphere = qp.get_bloch_sphere()
                                self.gui.draw_blochsphere(bloch_sphere, player)
                            if phi_slider.dragging:
                                phi_slider.knob_rect.x = event.pos[0]
                                if phi_slider.knob_rect.x < phi_slider.rect.x:
                                    phi_slider.knob_rect.x = phi_slider.rect.x
                                elif phi_slider.knob_rect.x > phi_slider.rect.x + phi_slider.rect.width:
                                    phi_slider.knob_rect.x = phi_slider.rect.x + phi_slider.rect.width
                                phi_slider.value = phi_slider.min_value + (
                                        phi_slider.knob_rect.x - phi_slider.rect.x) * (
                                                           phi_slider.max_value - phi_slider.min_value) / phi_slider.rect.width
                                phi_slider.draw_value_text()
                                phi = phi_slider.value
                                qp.apply_gate('r', theta, phi)
                                bloch_sphere = qp.get_bloch_sphere()
                                self.gui.draw_blochsphere(bloch_sphere, player)


                    # Draw the sliders and knobs
                    theta_slider.draw()
                    phi_slider.draw()

                    # Update the knob positions
                    theta_slider.update_knob()
                    phi_slider.update_knob()
                    self.blit_buttons()
                    self.gui.update()
                    self.gui.draw_buttons_right()
                    self.gui.draw_buttons_left()
                    # pygame.display.flip()
                    self.gui.update()

                    probs = qp.calculate_probs()
                    probs[0] = (((probs[0] * 100) // 0.1) / 10)
                    probs[1] = (((probs[1] * 100) // 0.1) / 10)

                    text1 = "P of Qpiece1: " + str(probs[0]) + '%'
                    text2 = "P of Qpiece2: " + str(probs[1]) + '%'
                    # 1700x 700
                    xheight = 400
                    if player == 0:  # red player, left side
                        pygame.draw.rect(self.gui._screen, (255, 255, 255), [100, xheight + 50, 380, 500])

                        text1 = self.gui._font.render(text1, True, (0, 0, 0))
                        self.gui._screen.blit(text1, (100, xheight + 100))
                        text2 = self.gui._font.render(text2, True, (0, 0, 0))
                        self.gui._screen.blit(text2, (100, xheight + 150))
                    if player == 1:  # yellow player, right side
                        pygame.draw.rect(self.gui._screen, (255, 255, 255), [1400, xheight + 50, 500, 500])

                        text1 = self.gui._font.render(text1, True, (0, 0, 0))
                        self.gui._screen.blit(text1, (1400, xheight + 100))
                        text2 = self.gui._font.render(text2, True, (0, 0, 0))
                        self.gui._screen.blit(text2, (1400, xheight + 150))

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
                        # end_game = True

                turn += 1

            else:
                # piece is a normal piece
                pygame.draw.rect(self.gui._screen, (255, 255, 255), [900, 10, 200, 100])
                # get the column
                valid_column = False
                while not valid_column:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            column = event.key - 48
                            if column in valid_keys:
                                row = self.board.add_chip(player, column)
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
                        # end_game = True

                turn += 1

    def blit_buttons(self):
        surfaces_l = self.gui.gate_surfaces_left
        buttons_l = self.gui.gate_buttons_left
        surfaces_r = self.gui.gate_surfaces_right
        buttons_r = self.gui.gate_buttons_right
        for button in surfaces_l.keys():
            self.gui._screen.blit(surfaces_l[button], buttons_l[button])
            text1 = self.gui._font.render(button, True, (255, 255, 255))
            text_rect1 = text1.get_rect(center=buttons_l[button].center)
            self.gui._screen.blit(surfaces_l[button], buttons_l[button])
            self.gui._screen.blit(text1, text_rect1)

            self.gui._screen.blit(surfaces_r[button], buttons_r[button])
            text2 = self.gui._font.render(button, True, (255, 255, 255))
            text_rect2 = text2.get_rect(center=buttons_r[button].center)
            self.gui._screen.blit(surfaces_r[button], buttons_r[button])
            self.gui._screen.blit(text2, text_rect2)

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


if __name__ == "__main__":
    game = myGame()

import sys

from qiskit import *
from qiskit import Aer
from qiskit.tools.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
import numpy as np
import io
import pygame

class qPiece:

    # everytime a q_piece object is created...
    def __init__(self, col1, row1, col2, row2, player):
        # create a 1 qubit and 1 classical bit quantum circuit
        self.circuit = QuantumCircuit(1, 1)
        self.circuit.h(0)
        # initialize a state-vector for the qubit
        self.state_vector = self.get_sv()
        self.col1 = col1
        self.row1 = row1
        self.col2 = col2
        self.row2 = row2
        self.player = player
        self.not_collapsed = None

    # measure and collapse the superposition, returns the state-vector
    def measure(self):
        print("now measuring")
        self.circuit.measure(0, 0)
        self.state_vector = self.get_sv()

    # plots the bloch sphere of the current state-vector of qubit
    def get_bloch_sphere(self):
        self.state_vector = self.get_sv()
        if self.state_vector is not None:
            fig = plot_bloch_multivector(self.state_vector).figure
            plt.close(fig)
            return self.plot_to_surface(fig)

    def plot_to_surface(self, plot):
        buf = io.BytesIO()
        plot.savefig(buf, format='png')
        buf.seek(0)
        surf = pygame.image.load(buf)
        return surf

    # returns state-vector
    def get_sv(self):
        sv_simulator = Aer.get_backend('statevector_simulator')
        result = execute(self.circuit, backend=sv_simulator).result()
        self.state_vector = result.get_statevector()
        return self.state_vector

    # returns probabilities of state in a list
    def calculate_probs(self):
        p_0 = np.abs(self.get_sv()[0]) ** 2
        p_1 = np.abs(self.get_sv()[1]) ** 2
        return [p_0, p_1]

    def apply_gate(self, gate, theta=None, phi=None):

        if gate == 'x':
            self.circuit.x(0)
        if gate == 'z':
            self.circuit.z(0)
        if gate == 'y':
            self.circuit.y(0)
        if gate == 'h':
            self.circuit.h(0)
        if gate == 'r':
            self.circuit.r(theta, phi, 0)


    def collapsed(self):
        state = self.calculate_probs()
        print(state)
        if state[0] == 1:
            self.not_collapsed = [self.get_col1(), self.get_row1()]
            return [self.get_col2(), self.get_row2()]
        else:
            self.not_collapsed = [self.get_col2(), self.get_row2()]
            return [self.get_col1(), self.get_row1()]

    def get_col1(self):
        return self.col1

    def get_col2(self):
        return self.col2

    def get_row1(self):
        return self.row1

    def get_row2(self):
        return self.row2

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    qp = qPiece(2, 0, 5, 0, 0)
    # qp.apply_gate('h')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        bloch_sphere = qp.get_bloch_sphere()
        screen.blit(bloch_sphere, (0, 0))
        pygame.display.flip()
        clock.tick(60)
        stop = False
        while not stop:
            gate = input("Gate: ")
            if gate != 'stop':
                if gate == 'r':
                    theta = float(input('theta: '))
                    phi = float(input('phi: '))
                else:
                    theta = None
                    phi = None
                qp.apply_gate(gate, theta=theta, phi=phi)
                bloch_sphere = qp.get_bloch_sphere()
                screen.blit(bloch_sphere, (0, 0))
                pygame.display.flip()
                clock.tick(60)
            else:
                stop = True

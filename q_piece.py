from qiskit import *
from qiskit import Aer
from qiskit.tools.visualization import plot_bloch_multivector
import numpy as np


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
        plot_bloch_multivector(self.state_vector)

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
            self.get_bloch_sphere()
        if gate == 'z':
            self.circuit.z(0)
            self.get_bloch_sphere()
        if gate == 'y':
            self.circuit.y(0)
            self.get_bloch_sphere()
        if gate == 'h':
            self.circuit.h(0)
            self.get_bloch_sphere()
        if gate == 'r':
            self.circuit.r(theta, phi, 0)
            self.get_bloch_sphere()

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
from tequila.circuit._gates_impl import QGateImpl
from tequila import TequilaException
from tequila import BitNumbering
import numpy, typing, numbers

class QCircuit():

    @property
    def gates(self):
        if self._gates is None:
            return []
        else:
            return self._gates

    @property
    def numbering(self) -> BitNumbering:
        return BitNumbering.LSB

    @property
    def qubits(self):
        accumulate = []
        for g in self.gates:
            accumulate += list(g.qubits)
        return sorted(list(set(accumulate)))

    @property
    def n_qubits(self):
        return max(self.max_qubit() + 1, self._min_n_qubits)

    @n_qubits.setter
    def n_qubits(self, other):
        self._min_n_qubits = other
        if other < self.max_qubit() + 1:
            raise TequilaException(
                "You are trying to set n_qubits to " + str(other) + " but your circuit needs at least: " + str(
                    self.max_qubit() + 1))
        return self

    def __init__(self, gates=None):

        self._n_qubits = None
        self._min_n_qubits = 0
        if gates is None:
            self._gates = []
        else:
            self._gates = list(gates)

    def is_primitive(self):
        """
        Check if this is a single gate wrapped in this structure
        :return: True if the circuit is just a single gate
        """
        return len(self.gates) == 1

    def replace_gate(self, position, gates):
        if hasattr(gates, '__iter__'):
            gs = gates
        else:
            gs = [gates]

        new = self.gates[:position]
        new.extend(gs)
        new.extend(self.gates[(position + 1):])
        return QCircuit(gates=new)

    def dagger(self):
        """
        Sumner's Fork:
        I have changed this so that the call to dagger is just dagger all the way down.
        :return: Circuit in reverse with signs of rotations switched
        """
        result = QCircuit()
        for g in reversed(self.gates):
            result += g.dagger()
        return result

    def extract_variables(self) -> dict:
        """
        return a list containing all the variable objects contained in any of the gates within the unitary
        including those nested within transforms.
        """
        variables = []
        for i, g in enumerate(self.gates):
            if g.is_parametrized():
                variables += g.extract_variables()
        return list(set(variables))

    def max_qubit(self):
        """
        :return: Maximum index this circuit touches
        """
        qmax = 0
        for g in self.gates:
            qmax = max(qmax, g.max_qubit)
        return qmax

    def __iadd__(self, other):
        if isinstance(other, QGateImpl):
            other = self.wrap_gate(other)

        if isinstance(other, list) and isinstance(other[0], QGateImpl):
            self._gates += other
        else:
            self._gates += other.gates
        self._min_n_qubits = max(self._min_n_qubits, other._min_n_qubits)
        return self

    def __add__(self, other):
        gates = [g.copy() for g in (self.gates + other.gates)]
        result = QCircuit(gates=gates)
        result._min_n_qubits = max(self._min_n_qubits, other._min_n_qubits)
        return result

    def __str__(self):
        result = "circuit: \n"
        for g in self.gates:
            result += str(g) + "\n"
        return result

    def __eq__(self, other):
        if len(self.gates) != len(other.gates):
            return False
        for i, g in enumerate(self.gates):
            if g != other.gates[i]:
                return False
        return True

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def wrap_gate(gate: QGateImpl):
        """
        :param gate: Abstract Gate
        :return: wrap gate in QCircuit structure (enable arithmetic operators)
        """
        if isinstance(gate, QCircuit):
            return gate
        else:
            return QCircuit(gates=[gate])
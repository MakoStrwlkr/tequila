from openvqe.hamiltonian import QubitHamiltonian, PX, PY, PZ
from numpy import random


def test_simple_arithmetic():
    qubit = random.randint(0, 5)
    primitives = [PX, PY, PZ]
    assert (PX(qubit).conjugate() == PX(qubit))
    assert (PY(qubit).conjugate() == -1 * PY(qubit))
    assert (PZ(qubit).conjugate() == PZ(qubit))
    assert (PX(qubit).transpose() == PX(qubit))
    assert (PY(qubit).transpose() == -1 * PY(qubit))
    assert (PZ(qubit).transpose() == PZ(qubit))
    for P in primitives:
        assert (P(qubit) * P(qubit) == QubitHamiltonian())
        n = random.randint(0, 10)
        nP = QubitHamiltonian.init_zero()
        for i in range(n):
            nP += P(qubit)
        assert (n * P(qubit) == nP)

    for i, Pi in enumerate(primitives):
        i1 = (i + 1) % 3
        i2 = (i + 2) % 3
        assert (Pi(qubit) * primitives[i1](qubit) == 1j * primitives[i2](qubit))
        assert (primitives[i1](qubit) * Pi(qubit) == -1j * primitives[i2](qubit))

        for qubit2 in random.randint(6, 10, 5):
            if qubit2 == qubit: continue
            P = primitives[random.randint(0, 2)]
            assert (Pi(qubit) * primitives[i1](qubit) * P(qubit2) == 1j * primitives[i2](qubit) * P(qubit2))
            assert (P(qubit2) * primitives[i1](qubit) * Pi(qubit) == -1j * P(qubit2) * primitives[i2](qubit))


def test_conjugation():
    primitives = [PX, PY, PZ]
    factors = [1, -1, 1j, -1j, 0.5 + 1j]
    string = QubitHamiltonian.init_unit()
    cstring = QubitHamiltonian.init_unit()
    for repeat in range(10):
        for q in random.randint(0, 7, 5):
            ri = random.randint(0, 2)
            P = primitives[ri]
            sign = 1
            if ri == 1:
                sign = -1
            factor = factors[random.randint(0, len(factors) - 1)]
            cfactor = factor.conjugate()
            string *= factor * P(qubit=q)
            cstring *= cfactor * sign * P(qubit=q)

        assert (string.conjugate() == cstring)


def test_transposition():
    primitives = [PX, PY, PZ]
    factors = [1, -1, 1j, -1j, 0.5 + 1j]

    assert ((PX(0) * PX(1) * PY(2)).transpose() == -1 * PX(0) * PX(1) * PY(2))
    assert ((PX(0) * PX(1) * PZ(2)).transpose() == PX(0) * PX(1) * PZ(2))

    for repeat in range(10):
        string = QubitHamiltonian.init_unit()
        tstring = QubitHamiltonian.init_unit()
        for q in range(5):
            ri = random.randint(0, 2)
            P = primitives[ri]
            sign = 1
            if ri == 1:
                sign = -1
            factor = factors[random.randint(0, len(factors) - 1)]
            string *= factor * P(qubit=q)
            tstring *= factor * sign * P(qubit=q)

        print("string =", string)
        print("stringt=", string.transpose())
        print("tstring=", tstring)
        assert (string.transpose() == tstring)


def make_random_pauliword(complex=True):
    primitives=[PX, PY, PZ]
    result = QubitHamiltonian.init_unit()
    for q in random.choice(range(10), 5, replace=False):
        P = primitives[random.randint(0, 2)]
        real = random.uniform(0, 1)
        imag = 0
        if complex:
            imag = random.uniform(0, 1)
        factor = real + imag * 1j
        result *= factor*P(q)
    return result


def test_dagger():
    assert (PX(0).dagger() == PX(0))
    assert (PY(0).dagger() == PY(0))
    assert (PZ(0).dagger() == PZ(0))

    for repeat in range(10):
        string = make_random_pauliword(complex=False)
        assert(string.dagger() == string)
        assert ((1j*string).dagger() == -1j*string)


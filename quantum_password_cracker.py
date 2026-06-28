"""
Quantum Password Cracker
=========================
Uses Grover's Algorithm to crack numeric passwords, demonstrating
the quantum speedup over classical brute-force search.

The user enters a numeric password, which is converted to binary.
Grover's algorithm then searches for the password using quadratically
fewer iterations than a classical computer would need.

Requirements: qiskit, qiskit-aer (installed automatically via run_password_cracker.bat)
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from getpass import getpass
import math


def crack_password(password):
    n = bin(int(password))[2:]  # Convert to binary
    num_qubits = len(n)
    N = 2 ** num_qubits
    opt = math.floor(math.pi / 4 * math.sqrt(N))

    if num_qubits > 15:
        print(f"Error: {num_qubits} qubits needed. Maximum supported is 15 qubits for simulation.")
        print("Real quantum hardware would be needed for larger passwords.")
        return
    elif num_qubits > 10:
        print(f"Note: {num_qubits} qubits needed. This may take a moment...")

    print(f"\nPassword stored as: {'*' * len(password)}")
    print(f"Binary representation: {num_qubits} bits")
    print(f"Classical brute-force: up to {N} checks")
    print(f"Grover iterations needed: {opt}")
    print("\nCracking password...\n")

    # Circuit
    circuit = QuantumCircuit(num_qubits, num_qubits)

    # Superposition
    for i in range(num_qubits):
        circuit.h(i)

    # Grover iterations
    for i in range(opt):
        # Oracle Step 1: X-wrap qubits that are '0' in the target
        for j in range(num_qubits):
            if n[j] == '0':
                circuit.x(j)

        # Oracle Step 2: Multi-controlled Z
        if num_qubits == 2:
            circuit.cz(0, 1)
        elif num_qubits == 3:
            circuit.h(2)
            circuit.ccx(0, 1, 2)
            circuit.h(2)
        else:
            circuit.h(num_qubits - 1)
            circuit.mcx(list(range(num_qubits - 1)), num_qubits - 1)
            circuit.h(num_qubits - 1)

        # Oracle Step 3: Undo X-wrap
        for j in range(num_qubits):
            if n[j] == '0':
                circuit.x(j)

        # Diffuser
        for j in range(num_qubits):
            circuit.h(j)
        for j in range(num_qubits):
            circuit.x(j)

        if num_qubits == 2:
            circuit.cz(0, 1)
        elif num_qubits == 3:
            circuit.h(2)
            circuit.ccx(0, 1, 2)
            circuit.h(2)
        else:
            circuit.h(num_qubits - 1)
            circuit.mcx(list(range(num_qubits - 1)), num_qubits - 1)
            circuit.h(num_qubits - 1)

        for j in range(num_qubits):
            circuit.x(j)
        for j in range(num_qubits):
            circuit.h(j)

    # Measurement
    for i in range(num_qubits):
        circuit.measure(i, i)

    # Run
    simulator = AerSimulator()
    job = simulator.run(circuit, shots=1000)
    result = job.result()
    counts = result.get_counts()

    # Convert result back
    measured = max(counts, key=counts.get)[::-1]
    cracked_password = int(measured, 2)

    # Output
    print("=" * 45)
    print("  QUANTUM PASSWORD CRACKER")
    print("=" * 45)
    print(f"  Secret password:     {password}")
    print(f"  Binary:              {n}")
    print(f"  Cracked binary:      {measured}")
    print(f"  Cracked password:    {cracked_password}")
    print(f"  Match:               {'Yes' if cracked_password == int(password) else 'No'}")
    print(f"  Classical checks:    up to {N}")
    print(f"  Grover iterations:   {opt}")
    print(f"  Quantum speedup:     {N}:{opt}")
    print("=" * 45)


if __name__ == "__main__":
    print("=" * 45)
    print("  QUANTUM PASSWORD CRACKER")
    print("  Powered by Grover's Algorithm")
    print("=" * 45)

    password = getpass("\nEnter your numeric password: ")
    crack_password(password)

    input("\nPress Enter to exit...")

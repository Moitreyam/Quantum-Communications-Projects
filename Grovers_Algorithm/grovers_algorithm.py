"""
Grover's Search Algorithm Simulation
======================================
Demonstrates Grover's algorithm for searching an unsorted database.

Supports 2-qubit (4 states) and 3-qubit (8 states) search with
automatic optimal iteration calculation.

Requirements: qiskit, qiskit-aer (installed automatically via run_grovers.bat)
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import math


def grovers_search(target):
    num_qubits = len(target)
    N = 2 ** num_qubits
    opt = math.floor(math.pi / 4 * math.sqrt(N))

    circuit = QuantumCircuit(num_qubits, num_qubits)

    # Superposition
    for i in range(num_qubits):
        circuit.h(i)

    # Grover iterations
    for i in range(opt):
        # Oracle: X-wrap qubits that are '0' in the target
        for j in range(num_qubits):
            if target[j] == '0':
                circuit.x(j)

        # Multi-controlled Z
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

        # Undo X-wrap
        for j in range(num_qubits):
            if target[j] == '0':
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

    measured = max(counts, key=counts.get)[::-1]
    top_count = counts[max(counts, key=counts.get)]

    print(f"\nTarget state:     |{target}>")
    print(f"Grover's found:   |{measured}>")
    print(f"Success rate:     {top_count}/1000")
    print(f"Iterations used:  {opt}")
    print(f"Search space:     {N} states")
    print(f"Quantum speedup:  {N}:{opt}")


if __name__ == "__main__":
    print("=" * 45)
    print("  GROVER'S SEARCH ALGORITHM")
    print("=" * 45)

    print("\nChoose an option:")
    print("1. Search for a specific target state")
    print("2. Test all states for 2 qubits")
    print("3. Test all states for 3 qubits")

    choice = input("\nEnter choice (1/2/3): ")

    if choice == "1":
        target = input("Enter target state (e.g., 101): ")
        grovers_search(target)
    elif choice == "2":
        for t in ['00', '01', '10', '11']:
            grovers_search(t)
            print("-" * 40)
    elif choice == "3":
        for t in ['000', '001', '010', '011', '100', '101', '110', '111']:
            grovers_search(t)
            print("-" * 40)
    else:
        print("Invalid choice!")

    input("\nPress Enter to exit...")

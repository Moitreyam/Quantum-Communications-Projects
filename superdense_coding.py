"""
Superdense Coding Protocol Simulation
=======================================
Simulates the Superdense Coding protocol using Qiskit.

Demonstrates how Alice can send two classical bits to Bob
by transmitting only one qubit, using a pre-shared entangled pair.

Requirements: qiskit, qiskit-aer (installed automatically via run_superdense.bat)
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def superdense(n):
    circuit = QuantumCircuit(2, 2)

    # Create entangled pair
    circuit.h(0)
    circuit.cx(0, 1)

    # Alice's encoding
    if n == '00':
        pass
    elif n == '01':
        circuit.x(0)
    elif n == '10':
        circuit.z(0)
    elif n == '11':
        circuit.x(0)
        circuit.z(0)
    else:
        print("Invalid 2-bit input. Please use 2 digits between 0 and 1")
        return

    # Bob's Bell measurement
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    circuit.measure(1, 1)

    # Run circuit
    simulator = AerSimulator()
    job = simulator.run(circuit, shots=1000)
    result = job.result()
    counts = result.get_counts()

    measured = list(counts.keys())[0][::-1]
    print(f"\nAlice sent: {n}")
    print(f"Bob received: {measured}")
    print(f"Shots: {list(counts.values())[0]}/1000")
    print(f"\n{circuit.draw()}")


if __name__ == "__main__":
    print("=" * 50)
    print("  Superdense Coding Protocol")
    print("=" * 50)

    print("\nChoose an option:")
    print("1. Send a specific 2-bit message")
    print("2. Test all four messages")

    choice = input("\nEnter choice (1/2): ")

    if choice == "1":
        n = input("Hi Alice! Please type in your 2-bit values: ")
        superdense(n)
    elif choice == "2":
        for msg in ['00', '01', '10', '11']:
            superdense(msg)
            print("\n" + "-" * 40)
    else:
        print("Invalid choice!")

    input("\nPress Enter to exit...")

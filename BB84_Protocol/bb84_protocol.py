"""
BB84 Quantum Key Distribution Protocol Simulation
===================================================
Simulates the BB84 QKD protocol with and without eavesdropper (Eve) detection.

The BB84 protocol was introduced by Bennett and Brassard in 1984.
It enables secure key exchange between two parties (Alice and Bob)
using quantum mechanics, with the ability to detect eavesdroppers (Eve).

Requirements: qiskit, qiskit-aer (installed automatically via run_bb84.bat)
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import random

def bb84(n, choice):
    # Preparation of qubits by Alice
    alice_bases = []
    alice_bits = []
    for i in range(n):
        alice_bases.append(random.choice(['Z', 'X']))
        alice_bits.append(random.randint(0, 1))

    if choice.lower() == 'yes':
        # Presence of Eve
        eve_bases = []
        eve_bits = []
        for i in range(n):
            eve_bases.append(random.choice(['Z', 'X']))
            if eve_bases[i] == alice_bases[i]:
                eve_bits.append(alice_bits[i])
            else:
                eve_bits.append(random.randint(0, 1))

        circuit = QuantumCircuit(n, n)

        for i in range(n):
            if eve_bits[i] == 1:
                circuit.x(i)
            if eve_bases[i] == 'X':
                circuit.h(i)

        bob_bases = []
        for i in range(n):
            bob_bases.append(random.choice(['Z', 'X']))
            if bob_bases[i] == 'X':
                circuit.h(i)
        for i in range(n):
            circuit.measure(i, i)

        simulator = AerSimulator()
        result = simulator.run(circuit, shots=1).result()
        counts = result.get_counts()
        bob_bits = list(counts.keys())[0][::-1]

        # Comparison
        shared_key = []
        for i in range(n):
            if alice_bases[i] == bob_bases[i]:
                shared_key.append(alice_bits[i])

        bob_key = []
        for i in range(n):
            if alice_bases[i] == bob_bases[i]:
                bob_key.append(int(bob_bits[i]))

        errors = 0
        for i in range(len(shared_key)):
            if shared_key[i] != bob_key[i]:
                errors += 1

        error_rate = errors / len(shared_key) if len(shared_key) > 0 else 0
        print(f"\nErrors: {errors} out of {len(shared_key)}")
        print(f"Error rate: {error_rate:.2%}")

        if error_rate > 0.1:
            print("Eve detected! Key compromised. Abort!")
        else:
            print("Channel appears secure.")

        print("Alice's key:", shared_key)
        print("Bob's key:", bob_key)
        print(circuit.draw())

    elif choice.lower() == 'no':
        # Absence of Eve
        circuit = QuantumCircuit(n, n)

        for i in range(n):
            if alice_bits[i] == 1:
                circuit.x(i)
            if alice_bases[i] == 'X':
                circuit.h(i)

        bob_bases = []
        for i in range(n):
            bob_bases.append(random.choice(['Z', 'X']))
            if bob_bases[i] == 'X':
                circuit.h(i)
        for i in range(n):
            circuit.measure(i, i)

        simulator = AerSimulator()
        result = simulator.run(circuit, shots=1).result()
        counts = result.get_counts()
        bob_bits = list(counts.keys())[0][::-1]

        # Comparison
        shared_key = []
        for i in range(n):
            if alice_bases[i] == bob_bases[i]:
                shared_key.append(alice_bits[i])

        bob_key = []
        for i in range(n):
            if alice_bases[i] == bob_bases[i]:
                bob_key.append(int(bob_bits[i]))

        print("\nAlice's key:", shared_key)
        print("Bob's key:", bob_key)
        print(circuit.draw())

    else:
        print("Invalid input!")


if __name__ == "__main__":
    print("=" * 50)
    print("  BB84 Quantum Key Distribution Protocol")
    print("=" * 50)
    n = int(input("\nHi Alice! How many qubits do you want to prepare? "))
    choice = input("Do you want to simulate with the presence of Eve? (Yes/No): ")
    bb84(n, choice)
    input("\nPress Enter to exit...")

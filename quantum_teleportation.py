"""
Quantum Teleportation Protocol Simulation
==========================================
Simulates the Quantum Teleportation protocol using Qiskit.

Demonstrates teleportation of a quantum state from Alice to Bob
using a shared entangled pair and classical communication.

Two modes:
1. Superposition state (H|0>) - shows 50/50 corrected output
2. Definitive state (|1>) - shows 100% corrected output proving teleportation

Requirements: qiskit, qiskit-aer (installed automatically via run_teleportation.bat)
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def teleport(state):
    circuit = QuantumCircuit(3, 3)

    # Step 1: Prepare Alice's qubit
    if state == "definitive":
        circuit.x(0)  # |1> state
        print("\nTeleporting definitive state |1>")
    else:
        circuit.h(0)  # superposition state
        print("\nTeleporting superposition state (|0>+|1>)/sqrt(2)")

    # Step 2: Create entangled pair between q1 and q2
    circuit.h(1)
    circuit.cx(1, 2)

    # Step 3: Alice's Bell measurement
    circuit.cx(0, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    circuit.measure(1, 1)

    # Step 4: Bob's measurement
    circuit.measure(2, 2)

    # Run circuit
    simulator = AerSimulator()
    job = simulator.run(circuit, shots=1000)
    result = job.result()
    counts = result.get_counts()

    print(f"\nRaw counts: {counts}\n")

    # Step 5: Post-selection analysis with classical correction
    for outcome, count in sorted(counts.items()):
        q0_bit = int(outcome[2])
        q1_bit = int(outcome[1])
        q2_bit = int(outcome[0])

        corrected_q2 = q2_bit
        if q1_bit == 1:
            corrected_q2 ^= 1

        print(f"Alice: q0={q0_bit} q1={q1_bit} | Bob raw: {q2_bit} | Bob corrected: {corrected_q2} | Count: {count}")

    print(f"\n{circuit.draw()}")


if __name__ == "__main__":
    print("=" * 50)
    print("  Quantum Teleportation Protocol")
    print("=" * 50)

    print("\nChoose the state to teleport:")
    print("1. Superposition state (|0>+|1>)/sqrt(2)")
    print("2. Definitive state |1>")
    print("3. Both")

    choice = input("\nEnter choice (1/2/3): ")

    if choice == "1":
        teleport("superposition")
    elif choice == "2":
        teleport("definitive")
    elif choice == "3":
        teleport("superposition")
        print("\n" + "=" * 50 + "\n")
        teleport("definitive")
    else:
        print("Invalid input!")

    input("\nPress Enter to exit...")

# Quantum Communications Projects

A collection of quantum communication protocol simulations built from scratch using Qiskit, as part of my journey into Quantum Communications, Networks, and Computing.

---

## BB84 Quantum Key Distribution Protocol

A simulation of the BB84 QKD protocol, first introduced by Bennett and Brassard in 1984. This protocol enables two parties (Alice and Bob) to generate a shared secret key using quantum mechanics, with the ability to detect any eavesdropper (Eve) attempting to intercept the communication.

### How It Works

1. **Alice** prepares qubits by randomly choosing classical bits (0 or 1) and encoding them in randomly selected bases (Z or X)
2. **Bob** receives the qubits and measures them using his own randomly chosen bases
3. Alice and Bob publicly compare their bases (not bit values) and keep only the bits where their bases matched — this is the **sifted key**
4. They sacrifice a portion of the sifted key to check for errors — if the error rate exceeds ~10%, an eavesdropper is detected

### Why It's Secure

- Measuring a qubit in the wrong basis destroys the encoded information
- The **No-Cloning Theorem** prevents Eve from copying qubits
- Eve's interference introduces a detectable error rate of approximately **25%**

### Features

- User-defined number of qubits
- Toggle between simulation with and without an eavesdropper
- Circuit visualization
- Sifted key generation and comparison
- Error rate calculation and eavesdropper detection

### Files

| File | Description |
|------|-------------|
| `BB84_Protocol.ipynb` | Jupyter Notebook with full explanation and simulation |
| `bb84_protocol.py` | Standalone Python script |
| `run_bb84.bat` | Windows batch file — auto-installs dependencies and runs the simulation |

### Quick Start

**Option 1: Jupyter Notebook**
```
pip install qiskit qiskit-aer
jupyter notebook BB84_Protocol.ipynb
```

**Option 2: Command Line**
```
pip install qiskit qiskit-aer
python bb84_protocol.py
```

**Option 3: One-Click (Windows)**

Download `bb84_protocol.py` and `run_bb84.bat` into the same folder, then double-click `run_bb84.bat`. It installs dependencies automatically and runs the simulation.

### Sample Output

**Without Eve:**
```
Alice's key: [1, 0, 1, 0, 0, 1, 0, 1]
Bob's key:   [1, 0, 1, 0, 0, 1, 0, 1]
Channel appears secure.
```

**With Eve:**
```
Errors: 4 out of 18
Error rate: 22.22%
Eve detected! Key compromised. Abort!
```

---

## Built With

- Python 3.13
- Qiskit 2.4.1
- Qiskit Aer (simulator)

## Upcoming Projects

- Quantum Teleportation
- Superdense Coding
- Grover's Search Algorithm
- QKD with Noise Simulation

## Author

Built as part of a structured learning path in Quantum Communications and Computing.

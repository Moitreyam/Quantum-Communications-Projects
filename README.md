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

## Quantum Teleportation Protocol

A simulation of the Quantum Teleportation protocol, which allows Alice to transfer an unknown quantum state to Bob using a shared entangled pair and two classical bits of communication — without physically transmitting the qubit.

### How It Works

1. Alice and Bob share an **entangled Bell pair** (created using H + CNOT gates)
2. Alice performs a **Bell measurement** (CNOT + H, then measure) on her original qubit and her half of the entangled pair — this destroys her original state
3. Alice sends the **two classical bits** from her measurement to Bob
4. Bob applies **correction gates** (X for bit flip, Z for phase flip) based on Alice's bits to recover the original state

### Key Concepts

- Entanglement as a shared resource between distant parties
- Bell measurement to extract relationship information
- Classical communication is essential — without it, Bob has random noise
- No-cloning theorem: Alice's state is destroyed, not copied
- Nothing travels faster than light — teleportation requires classical bits

### Features

- Teleportation of superposition state — verifies 50/50 corrected output
- Teleportation of definitive state |1⟩ — proves protocol with 100% corrected output
- Post-selection analysis with classical correction
- Circuit visualization

### Files

| File | Description |
|------|-------------|
| `Quantum_Teleportation.ipynb` | Jupyter Notebook with full explanation and simulation |
| `quantum_teleportation.py` | Standalone Python script |
| `run_teleportation.bat` | Windows batch file — auto-installs dependencies and runs the simulation |

### Quick Start

**Option 1: Jupyter Notebook**
```
pip install qiskit qiskit-aer
jupyter notebook Quantum_Teleportation.ipynb
```

**Option 2: Command Line**
```
pip install qiskit qiskit-aer
python quantum_teleportation.py
```

**Option 3: One-Click (Windows)**

Download `quantum_teleportation.py` and `run_teleportation.bat` into the same folder, then double-click `run_teleportation.bat`.

### Sample Output

**Teleporting definitive state |1⟩:**
```
Alice: q0=0 q1=1 | Bob raw: 0 | Bob corrected: 1 | Count: 270
Alice: q0=1 q1=1 | Bob raw: 0 | Bob corrected: 1 | Count: 261
Alice: q0=0 q1=0 | Bob raw: 1 | Bob corrected: 1 | Count: 239
Alice: q0=1 q1=0 | Bob raw: 1 | Bob corrected: 1 | Count: 230
```
Bob's corrected qubit is always 1 — teleportation successful.

---

## Superdense Coding Protocol

A simulation of the Superdense Coding protocol — the inverse of quantum teleportation. Alice sends two classical bits of information to Bob by transmitting only one qubit, using a pre-shared entangled pair.

### How It Works

1. Alice and Bob share an **entangled Bell pair**
2. Alice encodes her 2-bit message by applying gates to **her qubit only**:
   - `00` → no gate (sends Φ⁺)
   - `01` → X gate (sends Ψ⁺)
   - `10` → Z gate (sends Φ⁻)
   - `11` → X then Z (sends Ψ⁻)
3. Alice sends her qubit to Bob
4. Bob now has both qubits — he performs a **Bell measurement** (CNOT + H) to decode the 2-bit message

### Why It Works

The four Bell states are mutually orthogonal — perfectly distinguishable through measurement. Each encoding gate transforms the shared Bell state into a different one, and Bob's Bell measurement reveals exactly which one Alice created.

### Security

An eavesdropper intercepting Alice's qubit gains no useful information without Bob's half of the entangled pair. The intercepted qubit alone appears completely random.

### Features

- User-defined 2-bit message input
- All four Bell state encodings (00, 01, 10, 11)
- 100% accurate transmission across all cases
- Circuit visualization

### Files

| File | Description |
|------|-------------|
| `Superdense_Coding.ipynb` | Jupyter Notebook with full explanation and simulation |
| `superdense_coding.py` | Standalone Python script |
| `run_superdense.bat` | Windows batch file — auto-installs dependencies and runs the simulation |

### Quick Start

**Option 1: Jupyter Notebook**
```
pip install qiskit qiskit-aer
jupyter notebook Superdense_Coding.ipynb
```

**Option 2: Command Line**
```
pip install qiskit qiskit-aer
python superdense_coding.py
```

**Option 3: One-Click (Windows)**

Download `superdense_coding.py` and `run_superdense.bat` into the same folder, then double-click `run_superdense.bat`.

### Sample Output

```
Alice sent: 10
Bob received: 10
Shots: 1000/1000
```

---

## Built With

- Python 3.13
- Qiskit 2.4.1
- Qiskit Aer (simulator)

## Upcoming Projects

- Grover's Search Algorithm
- QKD with Noise Simulation

## Author

Built as part of a structured learning path in Quantum Communications and Computing.

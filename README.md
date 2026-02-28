# Policy Audit Tool 

A formal policy verification system built using Python and constraint solving.  
This project demonstrates how logical satisfiability checking can be used to evaluate institutional access control policies.

---

## Overview

This project demonstrates:

* Constraint-based policy validation
* Integration of formal logic into software systems
* Use of the Z3 SMT solver
* Dynamic schema-driven GUI forms
* Persistent policy storage using JSON
* Standalone application packaging

Instead of relying on traditional conditional logic, policies are evaluated using formal logical constraints and satisfiability checking.

---

## Learning Objectives

* Understand constraint solving and SMT concepts
* Model real-world policies using formal logic
* Implement solver-based validation using Python
* Design schema-driven dynamic forms
* Package Python applications into standalone executables
* Recognize the importance of formal verification in system security

---

## Technologies Used

* Python 3.8+
* Z3 SMT Solver
* Tkinter (Python GUI Toolkit)
* JSON (Schema & Persistence)
* PyInstaller (Executable Packaging)

---

## Features

* Multiple policy types (SIS, Exam, Lab, Privacy)
* Schema-driven dynamic field generation
* Role/action/system dropdown validation
* Boolean constraint handling
* Policy evaluation (ALLOWED / DENIED)
* Policy deletion
* Persistent storage via `policies.json`
* Standalone EXE support
* Lightweight and educational-focused design

---

## Project Structure

```
policy-audit-tool/
│
├── README.md
├── main.py              # Core logic & constraint evaluation
├── gui.py               # Graphical user interface
├── policy_schemas.json  # Policy type definitions
└── dist/                # Generated executable (after build)
```
---

## Technical Background

### Constraint-Based Policy Evaluation

Instead of writing nested conditional statements, this system uses a formal constraint solver.

### How It Works:

1. Policy fields are converted into symbolic variables.
2. Logical constraints are added to the solver.
3. The solver checks satisfiability.
4. If `sat` → Policy is **ALLOWED**
5. If `unsat` → Policy is **DENIED**

This approach ensures policies are logically consistent and verifiable.

---

## Example Policy Evaluation

Example:
Policy ID: P1
Type: SIS
Role: student
Action: view
Owner: yes

Result → ALLOWED


If a conflicting configuration is introduced:


Policy ID: P2
Type: SIS
Role: student
Action: delete
Owner: no

Result → DENIED


---

## Installation & Setup

### 1. Clone Repository

```
git clone https://github.com/Mikayn/Policy-Audit-Tool.git

```
---

### 2. Requirements

- Python 3.8+
- pip

Check Python:

Windows:
```
python --version
```

macOS / Linux:
```
python3 --version
```

---

### 3. Install Dependencies

```
pip install z3-solver rich
```

---

### 4. Run the Application

CLI Version:
```
python main.py
```

GUI Version:
```
python gui.py
```

---

## Building Standalone Executable

To package as a standalone EXE:

```
pyinstaller --onefile --noconsole --collect-all z3
--add-data "policy_schemas.json;."
--add-data "policies.json;."
gui.py
```

The executable will be located in the `dist/` folder.

---

## Results

Key Achievements:

* Successfully integrates formal constraint solving into a GUI application
* Demonstrates real-world policy validation concepts
* Handles dynamic schema-driven form generation
* Supports persistent storage and standalone execution

---

## Future Improvements

* Policy conflict detection
* Role hierarchy modeling
* More advanced logical constraints
* Logging system
* Improved UI styling
* Export policies to CSV or PDF

---

## Author

Aryan Ghimire
BSc (Hons) Cybersecurity & Ethical Hacking  
Coventry University (via Softwarica College) 
Academic Project – Policy Audit Tool  
Year: 2026

---

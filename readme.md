# Aegis-D  
**Deterministic Risk Assessment Kernel (Research Prototype)**

Aegis-D is a deterministic, auditable, input-order-independent risk assessment
kernel designed for autonomy research, simulation, and safety-oriented system
design.

It transforms geometric facts into conservative risk assessments with complete
audit trails and explicit limitations.  
It is **not** a control system and **not** certified for operational use.

---

## Design Intent

This project exists to demonstrate how autonomy-adjacent systems can be built
to prioritize:

- Determinism over optimization
- Auditability over sophistication
- Explicit limitations over hidden capability
- Human-in-the-loop oversight over full autonomy

The goal is not to act — the goal is to **inform humans reliably**.

---

## What This Is

- A deterministic decision primitive
- Input-order independent by construction
- Fully auditable (hash, parameters, explanations, constitution)
- Conservative by default
- Explicit about performance envelopes and limits
- Suitable for research, simulation, and education

## What This Is Not

- Not a control system
- Not probabilistic or learning-based
- Not hardware-validated
- Not certified for safety-critical operation
- Not autonomous

---

## Architecture Overview

The kernel is intentionally layered, with strict separation of concerns:

1. **Geometry Kernel**  
   Pure math (vectors, CPA). No interpretation.

2. **Risk Scoring Kernel**  
   Deterministic heuristics with explicit parameters and thresholds.

3. **Assessment & Selection**  
   Input-order-independent selection of the most concerning condition,
   with deterministic hashing and complete audit records.

4. **Temporal Aggregation (Optional)**  
   Conservative smoothing strategies (MAX by default).

5. **Action Recommendation (Non-Authoritative)**  
   Human-gated suggestions only. No actuation.

Each layer is independently inspectable and testable.

---

## Determinism & Auditability

Given the same inputs and parameters, Aegis-D will always produce:

- The same risk level
- The same score
- The same selected condition
- The same input hash

Every assessment includes:
- Deterministic input hash
- Parameter trace
- Score explanation
- System constitution (capabilities & limits)
- Timestamp (excluded from hash)

This enables reproducibility, debugging, and post-hoc analysis.

---

## Human-in-the-Loop by Design

Aegis-D does not execute actions.

For elevated, high, or critical risk levels:
- Human approval is explicitly required
- Recommendations are advisory only
- Physical and ethical boundaries are enforced in code

Autonomy creep is intentionally prevented.

---

## Running the Demo

```bash
python scripts/demo.py
Running Validations
python scripts/validate.py
These scripts demonstrate:
•	Determinism
•	Input-order independence
•	Conservative temporal behavior
•	Human approval gating
________________________________________
Status
Research prototype.
Provided for inspection, learning, and discussion — not deployment.
________________________________________
License
MIT

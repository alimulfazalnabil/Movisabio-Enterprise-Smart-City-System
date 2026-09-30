# Safety Architecture

The MoviSabio Enterprise system implements a strict, multi-layered safety architecture designed to absolutely prevent physical collisions resulting from AI or optimization errors.

## The Principle of Separation of Powers

The architecture enforces a strict decoupling between **Intelligence** and **Actuation**:

1. **AI/Optimization (The Brain)**: Calculates what *should* happen for optimal traffic flow. It issues a `SignalDecision` (a requested phase).
2. **Safety Engine (The Gatekeeper)**: Receives the `SignalDecision` and checks it against rigid, mathematical safety rules (e.g., Conflict Matrices, minimum green times, pedestrian clearances). 
3. **The Controller (The Final Authority)**: Receives commands via the Outbox only if the Safety Engine approves them. The roadside hardware remains the ultimate arbiter of safety.

## The Conflict Matrix

At the core of the Safety Engine is the Conflict Matrix. A conflict matrix is a static configuration defining which signal phases physically intersect. 

If the AI requests `North-South GREEN` while `East-West` is currently `GREEN`, the Safety Engine will immediately flag a `Conflict matrix violation` and override the requested state to `RED`, ensuring the command outbox never transmits a dangerous instruction to the intersection.

## Automated Verification

The Safety Engine is unit tested against known edge cases and malicious/faulty AI inputs (see `tests/unit/test_safety_engine.py`) to guarantee mathematical soundness before deployment to any physical intersection.

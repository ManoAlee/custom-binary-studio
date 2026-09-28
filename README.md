# ⚡ NEXUS Custom Binary Studio — High-Performance Computational Ecosystem

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![WebGL2 / WebGPU](https://img.shields.io/badge/Render-WebGL2%20%2F%20WebGPU-orange.svg)](nexus.html)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![CI Status](https://github.com/ManoAlee/custom-binary-studio/actions/workflows/ci.yml/badge.svg)](https://github.com/ManoAlee/custom-binary-studio/actions)
[![Live Interactive Studio](https://img.shields.io/badge/Live-Interactive%20Studio-brightgreen.svg)](https://manoalee.github.io/custom-binary-studio/nexus.html)

**A cutting-edge interactive computational laboratory uniting Pure Mathematics, Relativistic Physics, Hodgkin-Huxley Neurodynamics, Higher-Dimensional Geometry, and Information Theory into an ultra-fluid web visualization engine.**

[Interactive Modules](#interactive-modules) •
[System Architecture](#system-architecture) •
[Mathematical Foundations](#mathematical-foundations) •
[Local Deployment](#local-deployment) •
[Python Engine Suite](#python-engine-suite) •
[License](#license)

</div>

---

## Overview

**NEXUS (Custom Binary Studio)** is an interdisciplinary simulation workspace engineered for researchers, engineers, and computer scientists. It merges high-throughput GPU computing (GLSL shaders, WebGPU/WebGL2) with Python analytical backends to render complex physical, neural, and geometric phenomena directly in the browser at 60+ FPS.

From calculating **Hodgkin-Huxley membrane action potentials** and **Kerr Black Hole relativistic frame-dragging** to projecting **4D Tesseracts and Calabi-Yau manifolds**, NEXUS bridges the gap between rigorous scientific computation and visual intuition.

---

## Interactive Modules

```
                    ┌──────────────────────────────────────────────┐
                    │          NEXUS SIMULATION ENGINE             │
                    └──────────────────────┬───────────────────────┘
                                           │
         ┌──────────────────┬──────────────┴─────┬──────────────────┐
         ▼                  ▼                    ▼                  ▼
   [Relativity]      [Neurodynamics]      [Higher-Dim Geo]   [Info Theory]
   • Kerr Spacetime  • Hodgkin-Huxley     • 4D Tesseract     • Shannon H(X)
   • Ergosfera 0.98c • Action Potential   • Calabi-Yau 6D    • Hamming ECC
   • Redshift Lens   • Qualia Synthesizer • 120-Cell Glome   • Turing Machine
```

### 1. Relativistic & Gravitational Physics
- **Kerr Spacetime Simulation:** Ray-traced general relativistic gravitational lensing around a spinning black hole with frame-dragging, ergosfera boundary, and relativistic Doppler beaming ($a/M = 0.98$).
- **N-Body Gravitational Dynamics:** Real-time Barnes-Hut / symplectic particle integrator modeling galactic collisions and Lagrange orbital resonance.
- **Alcubierre Metric Warp Bubble:** Exotic spacetime metric contraction/expansion visualization.

### 2. Computational Neurodynamics
- **Hodgkin-Huxley Membrane Model (1952):** Real-time numerical integration of non-linear differential conductances ($I = C_m \frac{dV}{dt} + \bar{g}_K n^4(V - V_K) + \bar{g}_{Na} m^3 h(V - V_{Na}) + \bar{g}_l(V - V_l)$).
- **3D Anatomical Cortex:** Interactive volumetric mapping of human cortical structures, gyri, sulci, and the limbic complex (hippocampus, amygdala).
- **VALIS Qualia Synthesizer:** Harmonic frequency synthesis across neural oscillation bands (Delta, Theta, Alpha, Beta, Gamma).

### 3. Higher-Dimensional Geometry & Chaos
- **4D Hyper-Spatial Projection:** Orthographic and stereographic projections of 4-polytopes: Tesseract ($8$-cell), 16-cell, 24-cell, 120-cell, and 6-dimensional Calabi-Yau compactifications.
- **Non-Linear Strange Attractors:** High-precision Runge-Kutta 4th order integrator for Lorenz, Rössler, Chen, and Aizawa chaotic dynamical systems.
- **Quantum Wave Interference:** 2D wave equation solver simulating Young's double-slit experiment and quantum probability density diffraction.

### 4. Information Theory & Universal Computation
- **Shannon Entropy & Huffman Coding:** Real-time computation of bit entropy $H(X) = -\sum p_i \log_2 p_i$ and minimum redundancy prefix trees.
- **Hamming Error-Correcting Code:** Single-error correction and double-error detection (SECDED) simulation in memory registers.
- **Universal Turing Machine:** Infinite-tape state machine executing binary arithmetic with step-by-step state transition logs.

---

## Mathematical Foundations

### Hodgkin-Huxley Non-Linear Conductance

$$\frac{dV}{dt} = \frac{1}{C_m} \left( I_{\text{ext}} - \bar{g}_{\text{Na}} m^3 h (V - V_{\text{Na}}) - \bar{g}_{\text{K}} n^4 (V - V_{\text{K}}) - g_L (V - V_L) \right)$$

Gate probability state equations:
$$\frac{dx}{dt} = \alpha_x(V)(1 - x) - \beta_x(V)x \quad \text{for } x \in \{m, h, n\}$$

### Kerr Metric Line Element (Boyer-Lindquist Coordinates)

$$ds^2 = -\left(1 - \frac{2Mr}{\rho^2}\right) dt^2 - \frac{4Mar \sin^2\theta}{\rho^2} dt\,d\phi + \frac{\rho^2}{\Delta} dr^2 + \rho^2 d\theta^2 + \left(r^2 + a^2 + \frac{2Ma^2r\sin^2\theta}{\rho^2}\right)\sin^2\theta\,d\phi^2$$

where:
$$\rho^2 = r^2 + a^2 \cos^2\theta, \quad \Delta = r^2 - 2Mr + a^2$$

---

## Python Engine Suite

The repository includes a suite of standalone command-line computational engines:

- `custom_binary_engine.py`: Binary analysis, bit manipulation, and custom entropy evaluation.
- `non_binary_frontier_engine.py`: Multi-state non-binary quantum state representations and fuzzy truth evaluation.
- `reverse_engineer_engine.py`: Static structural disassembly and binary pattern recognition.
- `master_binary_ecosystem.py`: Central orchestration CLI coordinating analytical modules.

```bash
# Execute the master ecosystem CLI
python master_binary_ecosystem.py --help
```

---

## Local Deployment

To run the interactive suite locally:

```bash
# 1. Clone the repository
git clone https://github.com/ManoAlee/custom-binary-studio.git
cd custom-binary-studio

# 2. Launch local lightweight HTTP server
python -m http.server 8000

# 3. Open in your modern WebGL2/WebGPU enabled browser
# URL: http://localhost:8000/nexus.html
```

---

## Contributing

Contributions are welcomed across all domains (differential equations, GLSL shaders, UI enhancements, and Python backends). Please follow:
1. Ensure all Python modules pass `python -m py_compile *.py`.
2. Maintain standard WebGL2/WebGPU compatibility without non-standard vendor extensions.
3. Submit a PR with a description of the physical or mathematical phenomenon modeled.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

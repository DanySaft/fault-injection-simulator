# RISC-V Fault Injection Framework

## Overview
This project is an automated hardware security testing framework designed to simulate physical fault injections (such as voltage glitching or laser attacks) on bare-metal RISC-V binaries. Built with [Unicorn Engine](https://www.unicorn-engine.org/), this tool allows for precise, deterministic emulation of a CPU to evaluate the resilience of embedded C code against physical tampering.

## Project Architecture
The framework is designed with a modular architecture to easily integrate new targets and fault models:

* `target/` : Contains the bare-metal C source code, compilation scripts, and the compiled `.bin` targets.
* `config.py` : Defines the virtual hardware memory map (Base Address, Stack Pointer limits, etc.).
* `target_loader.py` : Handles binary loading and initializes a clean, isolated virtual CPU for each simulation run.
* `fault_models.py` : Contains the physical attack simulations (e.g., Instruction Skip).
* `main.py` : The core orchestrator. It executes the "Golden Run" (tracing normal execution) and launches the automated fuzzing campaign.

## Current Progress

### Instruction Skip Model
- **RISC-V 32-bit Bare-Metal Emulation:** Configured Unicorn Engine to execute RISC-V binaries without an OS.
- **Automated Execution Tracing:** Developed a hooking mechanism to record the precise execution path (PC register tracking) of a healthy execution.
- **Instruction Skip Implementation:** Created a fault model simulating a Single Fault Injection that forces the Program Counter (PC) to skip exactly one instruction during execution.
- **Vulnerability Discovery:** Successfully bypassed a basic PIN verification algorithm by systematically fuzzing the execution path, identifying critical points of failure (bypassing conditional branches `bne` and corrupting memory loads).

## Next Steps

- **Smart Card Scenario (PTC):** Develop a more complex, stateful C target involving a PIN Try Counter (anti-bruteforce mechanism) to simulate real-world smart card vulnerabilities.
- **Software Hardening:** Implement industry-standard software countermeasures on the C target, including:
  - Hardened Booleans (maximizing the Hamming distance between True/False states).
  - Control Flow Integrity (CFI) via step counters.
- **Advanced Fault Models:** Expand `fault_models.py` to include new physical attack simulations, such as Register/Memory **Bit-Flips**, to test the robustness of the implemented countermeasures.

## Setup

### 1.1 Compile to a 32-bit RISC-V object file

```bash
riscv64-unknown-elf-gcc -march=rv32im -mabi=ilp32 -O0 -c target/target.c -o target/target.o
```

### 1.2 Extract the raw binary footprint for Unicorn

```bash
riscv64-unknown-elf-objcopy -O binary target/target.o target/target.bin
```

### 2.1 Create the virtualenv Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2.2 Launch the setup

```bash
./main.py
```

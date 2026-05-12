# ABI Stateful Vault Fuzzer

## Overview

I built this project to explore how stateful fuzzing can be used to automatically discover accounting vulnerabilities in DeFi smart contracts.

The project is a generic ABI-driven stateful fuzzer focused on detecting inflation-style attacks in vault protocols. Instead of hardcoding a specific exploit sequence, the engine dynamically loads contract ABIs, discovers callable state-changing functions, generates randomized transaction sequences, mutates blockchain state, and automatically searches for accounting anomalies.

The core vulnerability targeted by the project is the classic inflation attack pattern found in vault-style protocols where direct asset donations manipulate `totalAssets()` and cause future deposits to mint zero shares due to integer division rounding.

The project combines:

* Solidity smart contracts
* Foundry tooling
* Stateful fuzzing
* ABI introspection
* Multi-actor transaction simulation
* Exploit minimization
* Automated anomaly detection
* Local EVM execution using Anvil

---

# What Problem This Project Solves

Many DeFi vault protocols calculate shares using accounting formulas based on:

* total assets inside the vault
* total shares already minted

If an attacker directly transfers assets into the vault without minting shares, the vault accounting becomes distorted.

This can create a situation where:

1. the attacker manipulates the exchange rate
2. a victim deposits real assets
3. the victim receives zero shares
4. the victim effectively loses funds

This type of issue is commonly referred to as an inflation attack.

The goal of this project is to automatically discover such vulnerable execution paths using stateful fuzzing.

---

# What Makes The Fuzzer Generic

The important architectural idea behind the project is that the exploit path is not hardcoded.

The engine does not manually execute:

* deposit
* donate
* deposit

Instead, it:

1. dynamically loads ABI metadata
2. discovers callable functions automatically
3. generates randomized transaction sequences
4. mutates transaction order and parameters
5. executes sequences on-chain
6. monitors vault accounting changes
7. detects exploit conditions automatically

This makes the architecture protocol-driven rather than exploit-script-driven.

The only vulnerability-specific component is the oracle responsible for defining what counts as an inflation-style accounting anomaly.

---

# Project Architecture

```text
inflation-fuzzer/
│
├── contracts/
├── script/
├── test/
├── fuzzer/
├── foundry.toml
└── README.md
```

---

# Smart Contracts

## MockERC20.sol

A simplified ERC20 implementation used as the underlying vault asset.

It supports:

* mint
* transfer
* approve
* transferFrom
* allowance tracking

The fuzzer uses this token for:

* attacker deposits
* victim deposits
* direct donation attacks
* balance resets during fuzzing

---

## VulnerableVault.sol

This is the intentionally vulnerable vault contract.

The vault:

* accepts deposits
* tracks vault shares
* calculates share minting
* maintains asset accounting

The vulnerability exists because direct token donations increase vault assets without minting new shares.

This causes exchange-rate distortion and enables inflation attacks.

---

## IVaultLike.sol

A lightweight interface abstraction representing vault-like protocol behavior.

It helps keep the fuzzing architecture modular and protocol-oriented.

---

# Python Fuzzer Architecture

The Python engine is responsible for:

* ABI loading
* function discovery
* sequence generation
* transaction mutation
* stateful execution
* anomaly detection
* exploit minimization

The entire fuzzing process runs against a live local EVM environment using Foundry + Anvil.

---

# Core Components

## bootstrap.py

Initializes the fuzzing environment.

Responsibilities:

* connect to local blockchain
* load ABI artifacts
* create Web3 contract objects
* dynamically discover callable functions
* initialize accounts and protocol state

This file is responsible for the ABI-driven nature of the project.

---

## sequences.py

Generates and mutates transaction sequences.

Responsibilities:

* randomized argument generation
* randomized actor selection
* donation transaction generation
* sequence mutation
* state-space exploration

The engine explores multi-step transaction paths rather than isolated single-function calls.

---

## executor.py

The runtime execution engine.

Responsibilities:

* execute generated transaction sequences
* approve token transfers
* simulate attacker and victim interactions
* track vault accounting changes
* invoke the anomaly oracle
* collect execution traces

This component performs the actual stateful interaction with the live EVM.

---

## oracle.py

Defines what counts as an exploit.

The oracle detects situations where:

* accounting was manipulated using donations
* a victim deposit occurred
* vault shares did not increase correctly
* a zero-share style anomaly occurred

This is the semantic vulnerability detector of the system.

---

## state.py

Implements blockchain snapshot/revert logic.

This allows:

* deterministic fuzzing
* isolated sequence execution
* reproducible exploit discovery

Each fuzzing sequence executes independently while still maintaining state evolution inside the sequence itself.

---

## minimizer.py

Reduces exploit traces to the smallest reproducible transaction sequence.

This makes discovered exploits:

* easier to understand
* easier to debug
* easier to demonstrate

---

## engine.py

The main coordinator of the project.

It:

1. initializes the environment
2. generates fuzzing populations
3. executes sequences
4. mutates state
5. detects anomalies
6. minimizes exploits
7. stores exploit traces

This file controls the complete fuzzing lifecycle.

---

# Stateful Fuzzing Workflow

```text
Deploy Contracts
        ↓
Load ABI Artifacts
        ↓
Discover Callable Functions
        ↓
Generate Transaction Sequences
        ↓
Execute Stateful Interactions
        ↓
Track Vault Accounting Changes
        ↓
Detect Inflation Anomalies
        ↓
Minimize Exploit Trace
        ↓
Save exploit.json
```

---

# Example Exploit Pattern

The engine is capable of automatically discovering sequences similar to:

```text
attacker deposit
        ↓
attacker donation
        ↓
victim deposit
        ↓
victim receives zero shares
```

without manually hardcoding the exploit path.

---

# Technologies Used

* Solidity
* Foundry
* Anvil
* Python
* Web3.py
* Stateful fuzzing
* ABI introspection
* Local EVM testing

---

# How To Run The Project

## Step 1 — Install Git

Download Git:

[https://git-scm.com/downloads](https://git-scm.com/downloads)

Verify installation:

```bash
git --version
```

---

## Step 2 — Install Python

Download Python:

[https://www.python.org/downloads/](https://www.python.org/downloads/)

During installation:

Enable:

```text
Add Python to PATH
```

Verify:

```bash
python --version
```

---

## Step 3 — Install Foundry

Open PowerShell and run:

```powershell
iwr https://raw.githubusercontent.com/foundry-rs/foundry/master/foundryup/install.ps1 -useb | iex
```

Then run:

```bash
foundryup
```

Verify:

```bash
forge --version
```

---

## Step 4 — Clone The Repository

```bash
git clone <your-repo-link>
cd abi-stateful-vault-fuzzer
```

---

## Step 5 — Install forge-std

```bash
git init
forge install foundry-rs/forge-std
```

---

## Step 6 — Install Python Dependencies

```bash
pip install web3
```

---

## Step 7 — Build Contracts

```bash
forge build
```

This generates:

* compiled bytecode
* ABI artifacts
* contract metadata

---

## Step 8 — Start Local Blockchain

```bash
anvil
```

Keep this terminal open.

---

## Step 9 — Copy The First Private Key

Inside the Anvil output, copy:

```text
Private Keys
(0) 0x...
```

This key will be used for deployment.

---

## Step 10 — Deploy Contracts

Open a new terminal inside the project folder and run:

```bash
forge script script/Deploy.s.sol --broadcast --rpc-url http://127.0.0.1:8545 --private-key YOUR_PRIVATE_KEY
```

Replace:

```text
YOUR_PRIVATE_KEY
```

with the private key copied from Anvil.

---

## Step 11 — Copy Contract Addresses

Deployment output will show:

```text
Token: 0x...
Vault: 0x...
```

Copy both addresses.

---

## Step 12 — Run Tests

```bash
forge test
```

This verifies that:

* contracts compile correctly
* the inflation vulnerability exists
* the environment is configured properly

---

## Step 13 — Run The Fuzzer

```bash
cd fuzzer
python engine.py
```

---

## Step 14 — Enter Contract Addresses

Paste:

* deployed vault address
* deployed token address

when prompted.

---

## Step 15 — Wait For Exploit Discovery

The engine will:

* discover ABI functions
* generate stateful transaction sequences
* mutate interactions
* search for accounting anomalies
* automatically detect exploit paths

Eventually you should see:

```text
🚨 TRUE INFLATION ATTACK FOUND 🚨
```

followed by:

```text
🚨 EXPLOIT FOUND 🚨
```

---

# Final Notes

This project helped me explore:

* smart contract security
* stateful fuzzing
* DeFi vault accounting
* ABI-driven automation
* EVM execution internals
* exploit discovery workflows
* blockchain testing infrastructure

The main focus of the project was building a lightweight research-oriented fuzzing system capable of automatically discovering exploit paths in vault-style protocols through stateful protocol interaction rather than hardcoded exploit scripting.

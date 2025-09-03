# Assembler Documentation

## Table of Contents

1. [Installation](#installation)
2. [Architecture Notes](#architecture-notes)
3. [Labels](#labels)
4. [Macros](#macros)
5. [Operands](#operands)
6. [Instructions and Directives](#instructions-and-directives)
7. [Full Instruction Reference](#full-instruction-reference)

---

## Installation

Install via pip:

```bash
pip install git+https://github.com/jcbyte/facPU.git
```

Assemble a program and generate a Factorio blueprint ready for flashing:

```bash
facpu filename
```

## Architecture Notes

- Registers may store any signed 32-bit integer (−2,147,483,648 to +2,147,483,647).
- Memory may store only unsigned 31-bit values (0 to 2,147,483,647).

## Labels

Labels mark positions in code for jumps or references.

### Syntax

**Block Style:**

```
<label_name>:
  MOV R0 R1
  ; continue
```

**Inline Style:**

```
<label_name>: MOV R0 R1
; continue
```

### Usage

```
JMP <label_name>
```

## Macros

Macros are inline code expansions that always start with `#`.  
Parameters are optional — if none are required, you can simply use `#NAME`.

### Syntax

- **Without parameters:** `#NAME`
- **With parameters:** `#NAME(p1, p2, ...)`

### Defined Macros

`#define(NAME, string)`  
Defines a new macro.

- `NAME` — the macro identifier (used as `#NAME`).
- `string` — the replacement text. (Supporting positional parameters `$1`, `$2`, ...)

**Example:**

```
#define(FILL, GDS 0 0 15 15 $1)

#FILL(3) ; expands to GDS 0 0 15 15 3
```

---

`#col(R, G, B)` or `#col(hex)`  
Generates an 8-bit color value in **RRRGGGBB** format.

**Example:**

```
#col(128, 0, 255) ; Purple, expands to 0b0110011
#col(00ffff); Cyan, expands to 0b00011111
```

## Operands

- **R1, R2, R3, ..., R15** — General-purpose registers.
- **IMM** — Immediate (constant) value (0–1023) or a label.
- **ADDR** — Memory address or label.

## Instructions and Directives

### CPU Instructions

**`MOV`**  
`MOV R1 R2` – Copy value from `R2` to `R1`.

**`LI`**  
`LI R1 IMM` – Load immediate value `IMM` into register `R1`.

**`LD`**  
`LD R1 ADDR` – Load value from memory address `ADDR` into `R1`.

**`ST`**  
`ST ADDR R1` – Store value from `R1` into memory address `ADDR`.

**`LDR`**  
`LDR R1 [R2]` – Load value from the memory address contained in `R2` into `R1`.

**`STR`**  
`STR [R1] R2` – Store value from `R2` into the memory address contained in `R1`.

**`JMP`**  
`JMP ADDR` – Jump to instruction at address `ADDR`.

**`BEQ` (alias)**  
`BEQ R1 R2 ADDR` – Branch to `ADDR` if `R1 == R2`.  
`BEQ R1 IMM ADDR` – Branch to `ADDR` if `R1 == IMM`.

**`BNE` (alias)**  
`BNE R1 R2 ADDR` – Branch to `ADDR` if `R1 ≠ R2`.  
`BNE R1 IMM ADDR` – Branch to `ADDR` if `R1 ≠ IMM`.

**`BLT` (alias)**  
`BLT R1 R2 ADDR` – Branch if `R1 < R2`.  
`BLT R1 IMM ADDR` – Branch if `R1 < IMM`.

**`BGT` (alias)**  
`BGT R1 R2 ADDR` – Branch if `R1 > R2`.  
`BGT R1 IMM ADDR` – Branch if `R1 > IMM`.

**`CALL`**  
`CALL ADDR` – Call subroutine at `ADDR` _(push return address and jump)_.

**`RET`**  
`RET` – Return from subroutine _(pop return address and jump)_.

**`NOP`**  
`NOP` – No operation; processor does nothing this cycle.

**`HLT`**  
`HLT` – Halt execution.

---

### ALU Instructions

**`ADD` (alias)**  
`ADD R1 R2 R3` – Add `R2` and `R3`, store in `R1`.  
`ADD R1 R2 IMM` – Add `R2` and `IMM`, store in `R1`.

**`SUB` (alias)**  
`SUB R1 R2 R3` – Subtract `R3` from `R2`, store in `R1`.  
`SUB R1 R2 IMM` – Subtract `IMM` from `R2`, store in `R1`

**`MUL` (alias)**  
`MUL R1 R2 R3` – Multiply `R2` by `R3`, store in `R1`.  
`MUL R1 R2 IMM` – Multiply `R2` by `IMM`, store in `R1`

**`DIV` (alias)**  
`DIV R1 R2 R3` – Divide `R2` by `R3`, store quotient in `R1`.  
`DIV R1 R2 IMM` – Divide `R2` by `IMM`, store quotient in `R1`.

**`MOD` (alias)**  
`MOD R1 R2 R3` – Compute `R2 mod R3`, store in `R1`.  
`MOD R1 R2 IMM` – Compute `R2 mod IMM`, store in `R1`.

**`POW` (alias)**  
`POW R1 R2 R3` – Raise `R2` to power `R3`, store in `R1`.  
`POW R1 R2 IMM` – Raise `R2` to power `IMM`, store in `R1`.

**`SHL` (alias)**  
`SHL R1 R2 R3` – Shift `R2` left by `R3` bits, store in `R1`.  
`SHL R1 R2 IMM` – Shift `R2` left by `IMM` bits, store in `R1`.

**`SHR` (alias)**  
`SHR R1 R2 R3` – Shift `R2` right by `R3` bits, store in `R1`.  
`SHR R1 R2 IMM` – Shift `R2` right by `IMM` bits, store in `R1`.

**`AND` (alias)**  
`AND R1 R2 R3` – Bitwise AND `R2` and `R3`, store in `R1`.  
`AND R1 R2 IMM` – Bitwise AND `R2` with `IMM`, store in `R1`.

**`OR` (alias)**  
`OR R1 R2 R3` – Bitwise OR `R2` and `R3`, store in `R1`.  
`OR R1 R2 IMM` – Bitwise OR `R2` with `IMM`, store in `R1`.

**`XOR` (alias)**  
`XOR R1 R2 R3` – Bitwise XOR `R2` and `R3`, store in `R1`.  
`XOR R1 R2 IMM` – Bitwise XOR `R2` with `IMM`, store in `R1`.

---

### Graphics Instructions

**`GDS` (alias)**  
Draw a rectangle in the off-screen buffer at `(param 1, param 2)` of size `(param 3 x param 4)` and color `param 5` (RRRGGGBB format).  
`GDS IMM IMM IMM IMM IMM`  
`GDS IMM IMM IMM IMM R1`  
`GDS IMM IMM R1 R2 IMM`  
`GDS IMM IMM R1 R2 R3`  
`GDS R1 R2 IMM IMM IMM`  
`GDS R1 R2 IMM IMM R3`  
`GDS R1 R2 R3 R4 IMM`  
`GDS R1 R2 R3 R4 R5`  
**Note:** The width and height is offset by 1, (0x0 -> 1x1).  
**Note:** The first 4 `IMM` parameters are 4 bits (0-15), and the last is 8 bits (0-255).

**`GSWP`**  
`GSWP` – Swap the visible graphics buffer with the off-screen buffer.

---

### Keyboard Instructions

**`KRD`**  
`KRD R1` – Pop the value from the keyboard, store in `R1`.

**`KRDP`**  
`KRDP R1` – Read the value from the keyboard, store in `R1`.

---

### Directives

**`DAT`**  
`DAT DATA` – Define raw data in memory.

## Full Instruction Reference

| Instruction | Operands                                                                                                                                                                                                  | Alias                                                                                  | Description                                       |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------- |
| **MOV**     | `R1 R2`                                                                                                                                                                                                   | —                                                                                      | Copy value from `R2` to `R1`                      |
| **LI**      | `R1 IMM`                                                                                                                                                                                                  | —                                                                                      | Load immediate value into `R1`                    |
| **LD**      | `R1 ADDR`                                                                                                                                                                                                 | —                                                                                      | Load value from memory address into `R1`          |
| **ST**      | `ADDR R1`                                                                                                                                                                                                 | —                                                                                      | Store value from `R1` into memory address         |
| **LDR**     | `R1 [R2]`                                                                                                                                                                                                 | —                                                                                      | Load value from memory address in `R2`            |
| **STR**     | `[R1] R2`                                                                                                                                                                                                 | —                                                                                      | Store value from `R2` into memory address in `R1` |
| **JMP**     | `ADDR`                                                                                                                                                                                                    | —                                                                                      | Jump to instruction at `ADDR`                     |
| **BEQ**     | `R1 R2 ADDR` / `R1 IMM ADDR`                                                                                                                                                                              | `BEQ/R`, `BEQ/I`                                                                       | Branch if equal                                   |
| **BNE**     | `R1 R2 ADDR` / `R1 IMM ADDR`                                                                                                                                                                              | `BNE/R`, `BNE/I`                                                                       | Branch if not equal                               |
| **BLT**     | `R1 R2 ADDR` / `R1 IMM ADDR`                                                                                                                                                                              | `BLT/R`, `BLT/I`                                                                       | Branch if less than                               |
| **BGT**     | `R1 R2 ADDR` / `R1 IMM ADDR`                                                                                                                                                                              | `BGT/R`, `BGT/I`                                                                       | Branch if greater than                            |
| **CALL**    | `ADDR`                                                                                                                                                                                                    | —                                                                                      | Call subroutine (push return address)             |
| **RET**     | —                                                                                                                                                                                                         | —                                                                                      | Return from subroutine                            |
| **NOP**     | —                                                                                                                                                                                                         | —                                                                                      | No operation                                      |
| **HLT**     | —                                                                                                                                                                                                         | —                                                                                      | Halt execution                                    |
| **ADD**     | `R1 R2 R3` / `R1 R2 IMM`                                                                                                                                                                                  | `ADD/R`, `ADD/I`                                                                       | Add values                                        |
| **SUB**     | `R1 R2 R3` / `R1 R2 IMM`                                                                                                                                                                                  | `SUB/R`, `SUB/I`                                                                       | Subtract values                                   |
| **MUL**     | `R1 R2 R3` / `R1 R2 IMM`                                                                                                                                                                                  | `MUL/R`, `MUL/I`                                                                       | Multiply values                                   |
| **DIV**     | `R1 R2 R3` / `R1 R2 IMM`                                                                                                                                                                                  | `DIV/R`, `DIV/I`                                                                       | Divide values                                     |
| **MOD**     | `R1 R2 R3` / `R1 R2 IMM`                                                                                                                                                                                  | `MOD/R`, `MOD/I`                                                                       | Modulo operation                                  |
| **POW**     | `R1 R2 R3` / `R1 R2 IMM`                                                                                                                                                                                  | `POW/R`, `POW/I`                                                                       | Power operation                                   |
| **SHL**     | `R1 R2 R3` / `R1 R2 IMM`                                                                                                                                                                                  | `SHL/R`, `SHL/I`                                                                       | Shift left                                        |
| **SHR**     | `R1 R2 R3` / `R1 R2 IMM`                                                                                                                                                                                  | `SHR/R`, `SHR/I`                                                                       | Shift right                                       |
| **AND**     | `R1 R2 R3` / `R1 R2 IMM`                                                                                                                                                                                  | `AND/R`, `AND/I`                                                                       | Bitwise AND                                       |
| **OR**      | `R1 R2 R3` / `R1 R2 IMM`                                                                                                                                                                                  | `OR/R`, `OR/I`                                                                         | Bitwise OR                                        |
| **XOR**     | `R1 R2 R3` / `R1 R2 IMM`                                                                                                                                                                                  | `XOR/R`, `XOR/I`                                                                       | Bitwise XOR                                       |
| **GDS**     | `GDS IMM IMM IMM IMM IMM` / `GDS IMM IMM IMM IMM R1` / `GDS IMM IMM R1 R2 IMM` / `GDS IMM IMM R1 R2 R3` / `GDS R1 R2 IMM IMM IMM` / `GDS R1 R2 IMM IMM R3` / `GDS R1 R2 R3 R4 IMM` / `GDS R1 R2 R3 R4 R5` | `GDS/III`, `GDS/IIR`, `GDS/IRI`, `GDS/IRR`, `GDS/RII`, `GDS/RIR`, `GDS/RRI`, `GDS/RRR` | Draw rectangle in off-screen buffer               |
| **GSWP**    | —                                                                                                                                                                                                         | —                                                                                      | Swap visible and off-screen graphics buffer       |
| **KRD**     | `R1`                                                                                                                                                                                                      | —                                                                                      | Pop value from keyboard                           |
| **KRDP**    | `R1`                                                                                                                                                                                                      | —                                                                                      | Read value from keyboard                          |
| **DAT**     | `DATA`                                                                                                                                                                                                    | —                                                                                      | Define raw memory data                            |

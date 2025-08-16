# facPU

Factorio CPU - a single threaded ~1Hz 31-bit CPU implemented in factorio.  
Including a corresponding assembler for writing and assembling programs.

## Hardware Specifications

- **Registers:** 16 general-purpose 31-bit registers
- **Memory:** 1024 memory locations, each 31-bit wide
- **Call Stack:** 16 call/return stack slots

## Getting Started

### Factorio
#todo list facotio mods  
#todo list facotio blueprint  

### Assembly
#todo pip install git+https://github.com/jcbyte/facPU.git  
#todo explain cli  
#todo explain flashing  

#todo explain cpu proccess #todo where does this belong?

## Assembly Language

```
; just some facPU assembly

start:
  LI R1 2
  LD R2 d
  POW R0 R1 R2
  loop: SUB R0 R0 1
  BEQ R0 0 start
  JMP loop

d: DAT 10
```

Supporting labels

### Operands
- **R1, R2, R3, ...** — General purpose registers.
- **IMM** — Immediate (constant) value _(max 1023)_.
- **ADDR** — Memory address or label.
- **DATA** — Raw data (used with `DAT` directive).

### Instructions

#### Data

- `MOV R1 R2`  
  **Description:** Copy value from `R2` to `R1`.  
  **RTL:** `R1 ← R2`

- `LI R1 IMM`  
  **Description:** Load immediate value `IMM` into register `R1`.  
  **RTL:** `R1 ← IMM`

- `LD R1 ADDR`  
  **Description:** Load the value stored at memory address `ADDR` into `R1`.  
  **RTL:** `R1 ← Mem[ADDR]`

- `ST ADDR R1`  
  **Description:** Store value in `R1` into memory address `ADDR`.  
  **RTL:** `Mem[ADDR] ← R1`

- `LDR R1 [R2]`  
  **Description:** Load the value from the memory address contained in `R2` into `R1`.  
  **RTL:** `R1 ← Mem[R2]`

- `STR [R1] R2`  
  **Description:** Store the value from `R2` into the memory address contained in `R1`.  
  **RTL:** `Mem[R1] ← R2`

#### Control Flow

- `JMP ADDR`  
  **Description:** Jump to instruction at address `ADDR`.  
  **RTL:** `PC ← ADDR`

- `BEQ R1 R2 ADDR`  
  **Description:** Branch to `ADDR` if `R1 == R2`.  
  **RTL:** `if (R1 = R2) then PC ← ADDR`

- `BNE R1 R2 ADDR`  
  **Description:** Branch to `ADDR` if `R1 ≠ R2`.  
  **RTL:** `if (R1 ≠ R2) then PC ← ADDR`

- `BLT R1 R2 ADDR`  
  **Description:** Branch to `ADDR` if `R1 < R2`.  
  **RTL:** `if (R1 < R2) then PC ← ADDR`

- `BGT R1 R2 ADDR`  
  **Description:** Branch to `ADDR` if `R1 > R2`.  
  **RTL:** `if (R1 > R2) then PC ← ADDR`

- `BEQI R1 IMM ADDR`  
  **Description:** Branch to `ADDR` if `R1 == IMM`.  
  **RTL:** `if (R1 = IMM) then PC ← ADDR`

- `BNEI R1 IMM ADDR`  
  **Description:** Branch to `ADDR` if `R1 ≠ IMM`.  
  **RTL:** `if (R1 ≠ IMM) then PC ← ADDR`

- `BLTI R1 IMM ADDR`  
  **Description:** Branch to `ADDR` if `R1 < IMM`.  
  **RTL:** `if (R1 < IMM) then PC ← ADDR`

- `BGTI R1 IMM ADDR`  
  **Description:** Branch to `ADDR` if `R1 > IMM`.  
  **RTL:** `if (R1 > IMM) then PC ← ADDR`

- `CALL ADDR`  
  **Description:** Call subroutine at `ADDR` _(push return address and jump)_.  
  **RTL:** `RS[SP] ← PC + 1; SP ← SP + 1; PC ← ADDR`

- `RET`  
  **Description:** Return from subroutine _(pop return address and jump)_.  
  **RTL:** `PC ← RS[SP]; SP ← SP - 1`

- `NOP`  
  **Description:** No operation; processor does nothing this cycle.  
  **RTL:** — 

- `HLT`  
  **Description:** Halt execution.  
  **RTL:** — 

#### ALU

- `ADD R1 R2 R3`  
  **Description:** Add `R2` and `R3`, store in `R1`.  
  **RTL:** `R1 ← R2 + R3`

- `SUB R1 R2 R3`  
  **Description:** Subtract `R3` from `R2`, store in `R1`.  
  **RTL:** `R1 ← R2 - R3`

- `MUL R1 R2 R3`  
  **Description:** Multiply `R2` by `R3`, store in `R1`.  
  **RTL:** `R1 ← R2 * R3`

- `DIV R1 R2 R3`  
  **Description:** Divide `R2` by `R3`, store quotient in `R1`.  
  **RTL:** `R1 ← R2 / R3`

- `MOD R1 R2 R3`  
  **Description:** Compute `R2` modulo `R3`, store in `R1`.  
  **RTL:** `R1 ← R2 mod R3`

- `POW R1 R2 R3`  
  **Description:** Raise `R2` to power `R3`, store in `R1`.  
  **RTL:** `R1 ← R2 ^ R3`

- `SHL R1 R2 R3`  
  **Description:** Shift `R2` left by `R3` bits, store in `R1`.  
  **RTL:** `R1 ← R2 << R3`

- `SHR R1 R2 R3`  
  **Description:** Shift `R2` right by `R3` bits, store in `R1`.  
  **RTL:** `R1 ← R2 >> R3`

- `AND R1 R2 R3`  
  **Description:** Bitwise AND `R2` and `R3`, store in `R1`.  
  **RTL:** `R1 ← R2 & R3`

- `OR R1 R2 R3`  
  **Description:** Bitwise OR `R2` and `R3`, store in `R1`.  
  **RTL:** `R1 ← R2 | R3`

- `XOR R1 R2 R3`  
  **Description:** Bitwise XOR `R2` and `R3`, store in `R1`.  
  **RTL:** `R1 ← R2 ^ R3`

#### ALU with Immediate

- `ADDI R1 R2 IMM`  
  **Description:** Add `R2` and immediate `IMM`, store in `R1`.  
  **RTL:** `R1 ← R2 + IMM`

- `SUBI R1 R2 IMM`  
  **Description:** Subtract immediate `IMM` from `R2`, store in `R1`.  
  **RTL:** `R1 ← R2 - IMM`

- `MULI R1 R2 IMM`  
  **Description:** Multiply `R2` by immediate `IMM`, store in `R1`.  
  **RTL:** `R1 ← R2 * IMM`

- `DIVI R1 R2 IMM`  
  **Description:** Divide `R2` by immediate `IMM`, store quotient in `R1`.  
  **RTL:** `R1 ← R2 / IMM`

- `MODI R1 R2 IMM`  
  **Description:** Compute `R2` modulo immediate `IMM`, store in `R1`.  
  **RTL:** `R1 ← R2 mod IMM`

- `POWI R1 R2 IMM`  
  **Description:** Raise `R2` to power immediate `IMM`, store in `R1`.  
  **RTL:** `R1 ← R2 ^ IMM`

- `SHLI R1 R2 IMM`  
  **Description:** Shift `R2` left by immediate `IMM` bits, store in `R1`.  
  **RTL:** `R1 ← R2 << IMM`

- `SHRI R1 R2 IMM`  
  **Description:** Shift `R2` right by immediate `IMM` bits, store in `R1`.  
  **RTL:** `R1 ← R2 >> IMM`

- `ANDI R1 R2 IMM`  
  **Description:** Bitwise AND `R2` with immediate `IMM`, store in `R1`.  
  **RTL:** `R1 ← R2 & IMM`

- `ORI R1 R2 IMM`  
  **Description:** Bitwise OR `R2` with immediate `IMM`, store in `R1`.  
  **RTL:** `R1 ← R2 | IMM`

- `XORI R1 R2 IMM`  
  **Description:** Bitwise XOR `R2` with immediate `IMM`, store in `R1`.  
  **RTL:** `R1 ← R2 ^ IMM`

#### Data Definition

- `DAT DATA`  
  **Description:** Define raw data `DATA` in memory.  
  **RTL:** Memory location ← `DATA`

## Licence

[GNU General Public License v3.0](LICENSE)

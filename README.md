# facPU

Factorio CPU - A single threaded ~14Hz 31-bit CPU fully implemented inside factorio.  
Including a corresponding assembler, allowing you to write and flash custom programs directly into the game.

This repository provides everything you need to use, build, and program the CPU.

## Hardware Specifications

- **Registers:** 16 general-purpose 31-bit registers
- **Memory:** 1024 memory locations, each 31-bit wide
- **Call Stack:** 16 call/return stack slots
- **Graphics:** 16x16 double-buffered display, supporting 256 colours
- **Arithmetic:** ALU supporting `+ - * / % ^ << >> AND OR XOR`
- **Input**: Alphanumeric keyboard with select extra characters

## Getting Started

### 1. Factorio Setup

#### Required Mods
- Space Age  
- [Circuit Wire Poles](https://mods.factorio.com/mod/circuit-wire-poles)  
- [Electric Pole Range Multiplier](https://mods.factorio.com/mod/ElectricPoleRangeMultiplier) *(set “Range factor” to **10**)*  
- [Global Power Network](https://mods.factorio.com/mod/global-power-network)  
- [Pushbutton](https://mods.factorio.com/mod/pushbutton)  
- [Text Plates](https://mods.factorio.com/mod/textplates)  

#### Recommended Mods

- [Instant Blueprint](https://mods.factorio.com/mod/InstantBP)  
- [Clear Skies](https://mods.factorio.com/mod/ClearSkies)  
- [Almost Invisible Electric Wires 2.0](https://mods.factorio.com/mod/AlmostInvisibleElectricWires2)  

#### Loading the CPU

- Import the blueprint from [blueprint.txt](/factorio_resources/blueprint.txt), **or**  
- Download my world from [facPU.zip](/factorio_resources/facPU.zip).  

### Extra Notes

> Setting the **"Toggle Entity"** keybind to **"F"** lets you **activate combinators and pushbuttons** by pressing F while hovering on them.

For better performance, increase tick speed in the Factorio console:  
`/c game.speed = 25`  
_(25 is stable on my systems, but you can experiment.)_

I would recommend disabling clouds for smoother rendering **→ Settings → Graphics → Show clouds (off)**.

### 2. Flashing

1. Enable "BLANK ZERO" (bottom-left, near the clock).
2. Paste the generated blueprint over the flasher combinators (bottom-right).
    - Ensure the first instruction aligns with the first combinator.
3. Enable the combinator with a tick to flash the code into memory.
4. Once flashing is complete, optionally disable "BLANK ZERO" for improved performance.

### 3. Running the CPU

Use the 3 control buttons by the clock:

- **PWR** – Start the CPU
- **HLT** – Halt execution
- **RST** – Reset the CPU

## Writing Programs

Programs can be written in a custom assembly language and assembled using the **facPU** assembler which supports **labels** and **macros**.

For full documentation, see [Assembly Documentation](/DOCS.md).

### Examples

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

More examples can be found in [demos](/demos/).

## Licence

[Apache License 2.0](LICENSE)

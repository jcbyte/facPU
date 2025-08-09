import re
from pathlib import Path
from typing import List

from colored import Fore, Style

from hardware_definition import (INSTRUCTION_SIZE, INSTRUCTIONS, OPCODE_SIZE,
                                 PARAM_SIZE, InstructionInfo)

max_reg: int = (1 << PARAM_SIZE["register"]) - 1
max_immediate: int = (1 << PARAM_SIZE["immediate"]) - 1
max_address: int = (1 << PARAM_SIZE["address"]) - 1


class AssemblyError(Exception):
    def __init__(self, message: str, token: str | None = None):
        super().__init__(message)
        self.token = token


def parse_op(token: str) -> InstructionInfo:
    instr = token.strip().upper()
    if instr not in INSTRUCTIONS:
        raise AssemblyError(f"Instruction {Style.underline}{token}{Style.res_underline} unknown", token=token)

    return INSTRUCTIONS[instr]


def parse_register(token: str) -> int:
    match = re.fullmatch(r"R(\d+)", token.strip(), re.IGNORECASE)
    if not match:
        raise AssemblyError(f"Register {Style.underline}{token}{Style.res_underline} has invalid syntax", token=token)

    reg_num = int(match.group(1))
    if not (0 <= reg_num <= max_reg):
        raise AssemblyError(f"Register {Style.underline}{token}{Style.res_underline} out of range (max {max_reg})", token=token)

    return reg_num


def parse_immediate(token: str) -> int:
    try:
      val = int(token, 0)  # auto-detect binary/hex
    except ValueError:
        raise AssemblyError(f"Immediate value {Style.underline}{token}{Style.res_underline} has invalid syntax", token=token)

    if not (0 <= val <= max_immediate):
        raise AssemblyError(f"Immediate value {Style.underline}{token}{Style.res_underline} out of range (max {max_immediate})", token=token)

    return val


def parse_address(token: str) -> int:
    try:
      val = int(token, 0)  # auto-detect binary/hex
    except ValueError:
        raise AssemblyError(f"Address {Style.underline}{token}{Style.res_underline} has invalid syntax", token=token)
    
    if not (0 <= val <= max_address):
        raise AssemblyError(f"Address {Style.underline}{token}{Style.res_underline} out of range (max {max_address})", token=token)

    return val


def assemble_line(line: str) -> int | None:
    line = line.split(";")[0].strip()  # remove comments
    if not line:
        return None

    parts = re.split(r"[,\s]+", line)
    instr = parts[0]
    params = parts[1:]
    instr_info = parse_op(instr)

    if len(instr_info["params"]) != len(params):
        raise AssemblyError(f"Instruction {Style.underline}{instr}{Style.res_underline} expects {len(instr_info["params"])} params, but got {len(params)}")
    

    binary = instr_info["opcode"]
    instruction_length = OPCODE_SIZE

    for param, ptype in zip(params, instr_info["params"]):
        match ptype:
            case "register":
                reg_num = parse_register(param)
                binary = (binary << PARAM_SIZE["register"]) | reg_num
                instruction_length += PARAM_SIZE["register"]
            case "immediate":
                value = parse_immediate(param)
                binary = (binary << PARAM_SIZE["immediate"]) | value
                instruction_length += PARAM_SIZE["immediate"]
            case "address":
                addr = parse_address(param)
                binary = (binary << PARAM_SIZE["address"]) | addr
                instruction_length += PARAM_SIZE["address"]

    binary <<= INSTRUCTION_SIZE - instruction_length

    return binary


def assemble(file: Path) -> List[int]:
    if not file.exists():
        raise ValueError(f"{Fore.red}File {Style.underline}{file}{Style.res_underline} cannot be found{Style.reset}")

    with open(file, "r") as f:
        lines = f.readlines()

    machine_code: List[int] = []
    for line_num, line in enumerate(lines):
        try:
            binary = assemble_line(line)
            if binary is not None:
                machine_code.append(binary)
        except AssemblyError as e:
            error_line = line.strip()
            if e.token:
                token_index = error_line.find(e.token)
                error_line = (
                    f"{error_line[:token_index]}"
                    f"{Style.underline}{error_line[token_index:token_index+len(e.token)]}{Style.res_underline}"
                    f"{error_line[token_index+len(e.token):]}"
                )
            else:
                error_line = f"{Style.underline}{error_line}{Style.res_underline}"

            error_msg = (
                f"{Fore.red}Error on line {line_num + 1}{Style.reset}\n"
                + (f"  {line_num + 1 - 1}: {lines[line_num - 1].strip()}\n" if line_num > 0 else "")
                + f"  {Fore.yellow}{line_num + 1}: {error_line}{Style.reset}\n"
                + (f"  {line_num + 1 + 1}: {lines[line_num + 1].strip()}\n" if line_num < len(lines) - 1 else "")
                + f"{Fore.red}{e}{Style.reset}\n"
            )
            raise Exception(error_msg)

    return machine_code

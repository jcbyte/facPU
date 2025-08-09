import re
from pathlib import Path
from typing import Dict, List, Literal, TypedDict

from colored import Fore, Style

ParamType = Literal["register", "immediate", "address"]


class InstructionInfo(TypedDict):
    opcode: int
    params: List[ParamType]


OPCODE_SIZE = 7
PARAM_SIZE: Dict[ParamType, int] = {"register": 4, "immediate": 10, "address": 10}
INSTRUCTION_SIZE = 31

INSTRUCTIONS: Dict[str, InstructionInfo] = {
    "MOV": {"opcode": 0b0000000, "params": ["register", "register"]},
    "LI": {"opcode": 0b0000001, "params": ["register", "immediate"]},
    "LD": {"opcode": 0b0000010, "params": ["register", "address"]},
    "ST": {"opcode": 0b0000011, "params": ["address", "register"]},
    "LDR": {"opcode": 0b0000100, "params": ["register", "register"]},
    "STR": {"opcode": 0b0000101, "params": ["register", "register"]},
    "NOP": {"opcode": 0b0001000, "params": []},
    "HLT": {"opcode": 0b0001001, "params": []},
    "JMP": {"opcode": 0b0010000, "params": ["address"]},
    "BEQ": {"opcode": 0b0010001, "params": ["register", "register", "address"]},
    "BNE": {"opcode": 0b0010010, "params": ["register", "register", "address"]},
    "BLT": {"opcode": 0b0010011, "params": ["register", "register", "address"]},
    "BGT": {"opcode": 0b0010100, "params": ["register", "register", "address"]},
    "BEQI": {"opcode": 0b0010101, "params": ["register", "immediate", "address"]},
    "BNEI": {"opcode": 0b0010110, "params": ["register", "immediate", "address"]},
    "BLTI": {"opcode": 0b0010111, "params": ["register", "immediate", "address"]},
    "BGTI": {"opcode": 0b0011000, "params": ["register", "immediate", "address"]},
    "CALL": {"opcode": 0b0011001, "params": ["address"]},
    "RET": {"opcode": 0b0011010, "params": []},
    "ADD": {"opcode": 0b0100000, "params": ["register", "register", "register"]},
    "SUB": {"opcode": 0b0100001, "params": ["register", "register", "register"]},
    "MUL": {"opcode": 0b0100010, "params": ["register", "register", "register"]},
    "DIV": {"opcode": 0b0100011, "params": ["register", "register", "register"]},
    "MOD": {"opcode": 0b0100100, "params": ["register", "register", "register"]},
    "POW": {"opcode": 0b0100101, "params": ["register", "register", "register"]},
    "SHL": {"opcode": 0b0100110, "params": ["register", "register", "register"]},
    "SHR": {"opcode": 0b0100111, "params": ["register", "register", "register"]},
    "AND": {"opcode": 0b0101000, "params": ["register", "register", "register"]},
    "OR": {"opcode": 0b0101001, "params": ["register", "register", "register"]},
    "XOR": {"opcode": 0b0101010, "params": ["register", "register", "register"]},
    "ADDI": {"opcode": 0b0110000, "params": ["register", "register", "immediate"]},
    "SUBI": {"opcode": 0b0110001, "params": ["register", "register", "immediate"]},
    "MULI": {"opcode": 0b0110010, "params": ["register", "register", "immediate"]},
    "DIVI": {"opcode": 0b0110011, "params": ["register", "register", "immediate"]},
    "MODI": {"opcode": 0b0110100, "params": ["register", "register", "immediate"]},
    "POWI": {"opcode": 0b0110101, "params": ["register", "register", "immediate"]},
    "SHLI": {"opcode": 0b0110110, "params": ["register", "register", "immediate"]},
    "SHRI": {"opcode": 0b0110111, "params": ["register", "register", "immediate"]},
    "ANDI": {"opcode": 0b0111000, "params": ["register", "register", "immediate"]},
    "ORI": {"opcode": 0b0111001, "params": ["register", "register", "immediate"]},
    "XORI": {"opcode": 0b0111010, "params": ["register", "register", "immediate"]},
}

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

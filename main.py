import re
from typing import Dict, List, Literal, TypedDict

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

def parse_op(token: str) -> InstructionInfo:
    instr = token.strip().upper()
    if instr not in INSTRUCTIONS:
        raise ValueError(f"Unknown instruction: {token}")
    
    return INSTRUCTIONS[instr]
        

def parse_register(token: str) -> int:
    match = re.fullmatch(r"R(\d+)", token.strip(), re.IGNORECASE)
    if not match:
        raise ValueError(f"Invalid register syntax: {token}")

    reg_num = int(match.group(1))
    if not (0 <= reg_num <= max_reg):
        raise ValueError(f"Register out of range: {token}")
    
    return reg_num


def parse_immediate(token: str) -> int:
    val = int(token, 0) # auto-detect binary/hex
    if not (0 <= val <= max_immediate):
        raise ValueError(f"Immediate out of range: {token}")
    
    return val


def parse_address(token: str) -> int:
    val = int(token, 0) # auto-detect binary/hex
    if not (0 <= val <= max_address):
        raise ValueError(f"Address out of range: {token}")
    
    return val

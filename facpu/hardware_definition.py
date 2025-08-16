from typing import Literal, TypedDict

ParamType = Literal["reg", "imm4", "imm8", "imm10", "addr"]


class InstructionInfo(TypedDict):
    opcode: int
    params: list[ParamType]


OPCODE_SIZE = 7
PARAM_SIZE: dict[ParamType, int] = {"reg": 4, "imm4": 4, "imm8": 8, "imm10": 10, "addr": 10}
INSTRUCTION_SIZE = 31

INSTRUCTIONS: dict[str, InstructionInfo] = {
    "MOV": {"opcode": 0b0000000, "params": ["reg", "reg"]},
    "LI": {"opcode": 0b0000001, "params": ["reg", "imm10"]},
    "LD": {"opcode": 0b0000010, "params": ["reg", "addr"]},
    "ST": {"opcode": 0b0000011, "params": ["addr", "reg"]},
    "LDR": {"opcode": 0b0000100, "params": ["reg", "reg"]},
    "STR": {"opcode": 0b0000101, "params": ["reg", "reg"]},
    "NOP": {"opcode": 0b0001000, "params": []},
    "HLT": {"opcode": 0b0001001, "params": []},
    "JMP": {"opcode": 0b0010000, "params": ["addr"]},
    "BEQ": {"opcode": 0b0010001, "params": ["reg", "reg", "addr"]},
    "BNE": {"opcode": 0b0010010, "params": ["reg", "reg", "addr"]},
    "BLT": {"opcode": 0b0010011, "params": ["reg", "reg", "addr"]},
    "BGT": {"opcode": 0b0010100, "params": ["reg", "reg", "addr"]},
    "BEQI": {"opcode": 0b0010101, "params": ["reg", "imm10", "addr"]},
    "BNEI": {"opcode": 0b0010110, "params": ["reg", "imm10", "addr"]},
    "BLTI": {"opcode": 0b0010111, "params": ["reg", "imm10", "addr"]},
    "BGTI": {"opcode": 0b0011000, "params": ["reg", "imm10", "addr"]},
    "CALL": {"opcode": 0b0011001, "params": ["addr"]},
    "RET": {"opcode": 0b0011010, "params": []},
    "ADD": {"opcode": 0b0100000, "params": ["reg", "reg", "reg"]},
    "SUB": {"opcode": 0b0100001, "params": ["reg", "reg", "reg"]},
    "MUL": {"opcode": 0b0100010, "params": ["reg", "reg", "reg"]},
    "DIV": {"opcode": 0b0100011, "params": ["reg", "reg", "reg"]},
    "MOD": {"opcode": 0b0100100, "params": ["reg", "reg", "reg"]},
    "POW": {"opcode": 0b0100101, "params": ["reg", "reg", "reg"]},
    "SHL": {"opcode": 0b0100110, "params": ["reg", "reg", "reg"]},
    "SHR": {"opcode": 0b0100111, "params": ["reg", "reg", "reg"]},
    "AND": {"opcode": 0b0101000, "params": ["reg", "reg", "reg"]},
    "OR": {"opcode": 0b0101001, "params": ["reg", "reg", "reg"]},
    "XOR": {"opcode": 0b0101010, "params": ["reg", "reg", "reg"]},
    "ADDI": {"opcode": 0b0110000, "params": ["reg", "reg", "imm10"]},
    "SUBI": {"opcode": 0b0110001, "params": ["reg", "reg", "imm10"]},
    "MULI": {"opcode": 0b0110010, "params": ["reg", "reg", "imm10"]},
    "DIVI": {"opcode": 0b0110011, "params": ["reg", "reg", "imm10"]},
    "MODI": {"opcode": 0b0110100, "params": ["reg", "reg", "imm10"]},
    "POWI": {"opcode": 0b0110101, "params": ["reg", "reg", "imm10"]},
    "SHLI": {"opcode": 0b0110110, "params": ["reg", "reg", "imm10"]},
    "SHRI": {"opcode": 0b0110111, "params": ["reg", "reg", "imm10"]},
    "ANDI": {"opcode": 0b0111000, "params": ["reg", "reg", "imm10"]},
    "ORI": {"opcode": 0b0111001, "params": ["reg", "reg", "imm10"]},
    "XORI": {"opcode": 0b0111010, "params": ["reg", "reg", "imm10"]},
}

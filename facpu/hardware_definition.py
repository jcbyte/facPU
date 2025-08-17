from typing import Literal, TypedDict

ParamType = Literal["reg", "imm4", "imm8", "imm10", "addr"]


class InstructionInfo(TypedDict):
    opcode: int
    params: list[ParamType]


OPCODE_SIZE = 7
PARAM_SIZE: dict[ParamType, int] = {"reg": 4, "imm4": 4, "imm8": 8, "imm10": 10, "addr": 10}
INSTRUCTION_SIZE = 31

INSTRUCTIONS: dict[str, InstructionInfo] = {
    # CPU
    "MOV": {"opcode": 0b0000000, "params": ["reg", "reg"]},
    "LI": {"opcode": 0b0000001, "params": ["reg", "imm10"]},
    "LD": {"opcode": 0b0000010, "params": ["reg", "addr"]},
    "ST": {"opcode": 0b0000011, "params": ["addr", "reg"]},
    "LDR": {"opcode": 0b0000100, "params": ["reg", "reg"]},
    "STR": {"opcode": 0b0000101, "params": ["reg", "reg"]},
    "NOP": {"opcode": 0b0001000, "params": []},
    "HLT": {"opcode": 0b0001001, "params": []},
    "JMP": {"opcode": 0b0010000, "params": ["addr"]},
    "BEQ/R": {"opcode": 0b0010001, "params": ["reg", "reg", "addr"]},
    "BNE/R": {"opcode": 0b0010010, "params": ["reg", "reg", "addr"]},
    "BLT/R": {"opcode": 0b0010011, "params": ["reg", "reg", "addr"]},
    "BGT/R": {"opcode": 0b0010100, "params": ["reg", "reg", "addr"]},
    "BEQ/I": {"opcode": 0b0010101, "params": ["reg", "imm10", "addr"]},
    "BNE/I": {"opcode": 0b0010110, "params": ["reg", "imm10", "addr"]},
    "BLT/I": {"opcode": 0b0010111, "params": ["reg", "imm10", "addr"]},
    "BGT/I": {"opcode": 0b0011000, "params": ["reg", "imm10", "addr"]},
    "CALL": {"opcode": 0b0011001, "params": ["addr"]},
    "RET": {"opcode": 0b0011010, "params": []},
    # CPU - ALU
    "ADD/R": {"opcode": 0b0100000, "params": ["reg", "reg", "reg"]},
    "SUB/R": {"opcode": 0b0100001, "params": ["reg", "reg", "reg"]},
    "MUL/R": {"opcode": 0b0100010, "params": ["reg", "reg", "reg"]},
    "DIV/R": {"opcode": 0b0100011, "params": ["reg", "reg", "reg"]},
    "MOD/R": {"opcode": 0b0100100, "params": ["reg", "reg", "reg"]},
    "POW/R": {"opcode": 0b0100101, "params": ["reg", "reg", "reg"]},
    "SHL/R": {"opcode": 0b0100110, "params": ["reg", "reg", "reg"]},
    "SHR/R": {"opcode": 0b0100111, "params": ["reg", "reg", "reg"]},
    "AND/R": {"opcode": 0b0101000, "params": ["reg", "reg", "reg"]},
    "OR/R": {"opcode": 0b0101001, "params": ["reg", "reg", "reg"]},
    "XOR/R": {"opcode": 0b0101010, "params": ["reg", "reg", "reg"]},
    "ADD/I": {"opcode": 0b0110000, "params": ["reg", "reg", "imm10"]},
    "SUB/I": {"opcode": 0b0110001, "params": ["reg", "reg", "imm10"]},
    "MUL/I": {"opcode": 0b0110010, "params": ["reg", "reg", "imm10"]},
    "DIV/I": {"opcode": 0b0110011, "params": ["reg", "reg", "imm10"]},
    "MOD/I": {"opcode": 0b0110100, "params": ["reg", "reg", "imm10"]},
    "POW/I": {"opcode": 0b0110101, "params": ["reg", "reg", "imm10"]},
    "SHL/I": {"opcode": 0b0110110, "params": ["reg", "reg", "imm10"]},
    "SHR/I": {"opcode": 0b0110111, "params": ["reg", "reg", "imm10"]},
    "AND/I": {"opcode": 0b0111000, "params": ["reg", "reg", "imm10"]},
    "ORI/": {"opcode": 0b0111001, "params": ["reg", "reg", "imm10"]},
    "XOR/I": {"opcode": 0b0111010, "params": ["reg", "reg", "imm10"]},
    # Graphics
    "GDS/III": {"opcode": 0b1000000, "params": ["imm4", "imm4", "imm4", "imm4", "imm8"]},
    "GDS/IIR": {"opcode": 0b1000001, "params": ["imm4", "imm4", "imm4", "imm4", "reg"]},
    "GDS/IRI": {"opcode": 0b1000010, "params": ["imm4", "imm4", "reg", "reg", "imm8"]},
    "GDS/IRR": {"opcode": 0b1000011, "params": ["imm4", "imm4", "reg", "reg", "reg"]},
    "GDS/RII": {"opcode": 0b1000100, "params": ["reg", "reg", "imm4", "imm4", "imm8"]},
    "GDS/RIR": {"opcode": 0b1000101, "params": ["reg", "reg", "imm4", "imm4", "reg"]},
    "GDS/RRI": {"opcode": 0b1000110, "params": ["reg", "reg", "reg", "reg", "imm8"]},
    "GDS/RRR": {"opcode": 0b1000111, "params": ["reg", "reg", "reg", "reg", "reg"]},
    "GSWP": {"opcode": 0b1001000, "params": []},
    # Keyboard
    "KRD": {"opcode": 0b1010000, "params": ["reg"]},
    "KRDP": {"opcode": 0b1010001, "params": ["reg"]},
}

import inspect
from typing import Callable

from colored import Style

ALIASED_INSTRUCTIONS = {
    "BEQ": ["BEQ/R", "BEQ/I"],
    "BNE": ["BNE/R", "BNE/I"],
    "BLT": ["BLT/R", "BLT/I"],
    "BGT": ["BGT/R", "BGT/I"],
    "ADD": ["ADD/R", "ADD/I"],
    "SUB": ["SUB/R", "SUB/I"],
    "MUL": ["MUL/R", "MUL/I"],
    "DIV": ["DIV/R", "DIV/I"],
    "MOD": ["MOD/R", "MOD/I"],
    "POW": ["POW/R", "POW/I"],
    "SHL": ["SHL/R", "SHL/I"],
    "SHR": ["SHR/R", "SHR/I"],
    "AND": ["AND/R", "AND/I"],
    "OR ": ["OR /R", "OR /I"],
    "XOR": ["XOR/R", "XOR/I"],
    "GDS": ["GDS/III", "GDS/IIR", "GDS/IRI", "GDS/IRR", "GDS/RII", "GDS/RIR", "GDS/RRI", "GDS/RRR"],
}


class PseudoInstruction:
    def __init__(self, func: Callable[..., int]) -> None:
        self.func = func

    def get_expected_parameters(self) -> int:
        sig = inspect.signature(self.func)
        params = sig.parameters
        # ignore line, as this is not passed from the assembly code
        return len(params) - (1 if "line_no" in params else 0)


def data_instr(data: str, line_no: int) -> int:
    from .assembler import AssemblyError
    from .hardware_definition import INSTRUCTION_SIZE

    try:
        val = int(data, 0)  # auto-detect binary/hex
    except ValueError:
        raise AssemblyError(f"Data value {Style.underline}{data}{Style.res_underline} has invalid syntax", line_no, token=data)

    max_binary: int = (1 << INSTRUCTION_SIZE) - 1
    if not (0 <= val <= max_binary):
        raise AssemblyError(f"Data value {Style.underline}{data}{Style.res_underline} out of range (max {max_binary})", line_no, token=data)

    return val


ASSEMBLER_PSEUDO_INSTRUCTIONS: dict[str, PseudoInstruction] = {
    "DAT": PseudoInstruction(data_instr),
}

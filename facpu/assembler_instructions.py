import inspect
from typing import Callable

from colored import Style


class PseudoInstruction:
    def __init__(self, func: Callable[..., int]) -> None:
        self.func = func

    def get_expected_parameters(self) -> int:
        sig = inspect.signature(self.func)
        params = sig.parameters
        # ignore line, as this is not passed from the assembly code
        return len(params) - (1 if "line" in params else 0)


def data_instr(data: str, line: int) -> int:
    from .assembler import MAX_BINARY, AssemblyError
    
    try:
        val = int(data, 0)  # auto-detect binary/hex
    except ValueError:
        raise AssemblyError(f"Data value {Style.underline}{data}{Style.res_underline} has invalid syntax", line, token=data)

    if not (0 <= val <= MAX_BINARY):
        raise AssemblyError(f"Data value {Style.underline}{data}{Style.res_underline} out of range (max {MAX_BINARY})", line, token=data)

    return val


ASSEMBLER_PSEUDO_INSTRUCTIONS: dict[str, PseudoInstruction] = {
    "DAT": PseudoInstruction(data_instr),
}

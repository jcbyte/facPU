import re
from typing import Callable

from colored import Style


class Macro:
    def __init__(self, func: Callable[[list[str], int], str]) -> None:
        self.func = func


class UserMacroRegistry:
    macros: dict[str, str] = {}


def define_macro(args: list[str], line_no: int) -> str:
    from .assembler import AssemblyError

    if len(args) != 2:
        raise AssemblyError(f"Macro {Style.underline}define{Style.res_underline} expects 2 params, but got {len(args)}", line_no)

    macro_name, macro_content = args

    UserMacroRegistry.macros.update({macro_name: macro_content})

    return ""


MACROS: dict[str, Macro] = {
    "define": Macro(define_macro),
}

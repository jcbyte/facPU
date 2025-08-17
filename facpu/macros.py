import re
from typing import Callable

from colored import Style


class Macro:
    def __init__(self, func: Callable[[list[str], int], str]) -> None:
        self.func = func


def col_macro(args: list[str], line_no: int) -> str:
    from .assembler import AssemblyError

    if len(args) == 1:
        hex_string = args[0]
        if len(hex_string) != 6:
            raise AssemblyError(
                f"Macro {Style.underline}col{Style.res_underline} was expecting a 6 character hex string, but got {len(hex_string)} characters", line_no, token=hex_string
            )

        try:
            rgb = [int(hex_string[i : i + 2], 16) for i in (0, 2, 4)]
        except ValueError:
            raise AssemblyError(f"Macro {Style.underline}col{Style.res_underline} hex string contains invalid characters", line_no, token=hex_string)

    elif len(args) == 3:
        rgb: list[int] = []
        for arg in args:
            try:
                arg_int = int(arg)
            except ValueError:
                raise AssemblyError(f"Macro {Style.underline}col{Style.res_underline} RGB values contain invalid characters", line_no, token=arg)

            if not (0 <= arg_int < 256):
                raise AssemblyError(f"Macro {Style.underline}col{Style.res_underline} RGB values must be between 0 and 255", line_no, token=arg)

            rgb.append(arg_int)

    else:
        raise AssemblyError(f"Macro {Style.underline}col{Style.res_underline} expects 1 or 3 params, but got {len(args)}", line_no)

    scaled_rgb = (rgb[0] * 7) // 255, (rgb[1] * 7) // 255, (rgb[2] * 3) // 255

    packed_scaled_rgb = (scaled_rgb[0] << 5) | (scaled_rgb[1] << 2) | (scaled_rgb[2] << 0)

    return str(packed_scaled_rgb)


class UserMacroRegistry:
    macros: dict[str, str] = {}

    @staticmethod
    def apply_macro(macro:str, args:list[str], line_no:int) -> str:
        from .assembler import AssemblyError
        
        macro_str = UserMacroRegistry.macros.get(macro, "")

        def replacer(match: re.Match) -> str:
          index = int(match.group(1)) - 1  # $1 -> args[0]

          try:
              return str(args[index])
          except IndexError:
              raise AssemblyError(f"Defined macro {Style.underline}{macro}{Style.res_underline} requires at least {index + 1} params, but got {len(args)}", line_no)
      
        return re.sub(r"\$(\d+)", replacer, macro_str)



def define_macro(args: list[str], line_no: int) -> str:
    from .assembler import AssemblyError

    if len(args) != 2:
        raise AssemblyError(f"Macro {Style.underline}define{Style.res_underline} expects 2 params, but got {len(args)}", line_no)

    macro_name, macro_content = args

    UserMacroRegistry.macros.update({macro_name: macro_content})

    return ""


MACROS: dict[str, Macro] = {
    "col": Macro(col_macro),
    "define": Macro(define_macro),
}

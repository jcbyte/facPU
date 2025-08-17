import re
from pathlib import Path

from colored import Fore, Style

from .assembler_instructions import ALIASED_INSTRUCTIONS, ASSEMBLER_PSEUDO_INSTRUCTIONS, PseudoInstruction
from .hardware_definition import INSTRUCTION_SIZE, INSTRUCTIONS, OPCODE_SIZE, PARAM_SIZE, InstructionInfo, ParamType
from .macros import MACROS, UserMacroRegistry


class AssemblyError(Exception):
    def __init__(self, message: str, line: int, token: str | None = None):
        super().__init__(message)
        self.line = line
        self.token = token

    def format_error(self, lines) -> str:
        error_line = lines[self.line].strip()

        token_index = error_line.find(self.token) if self.token else -1
        if token_index >= 0:
            assert self.token is not None  # for python type checker

            error_line = (
                f"{error_line[:token_index]}"
                f"{Style.underline}{error_line[token_index:token_index+len(self.token)]}{Style.res_underline}"
                f"{error_line[token_index+len(self.token):]}"
            )
        else:
            error_line = f"{Style.underline}{error_line}{Style.res_underline}"

        return (
            f"{Fore.red}Error on line {self.line + 1}{Style.reset}\n"
            + (f"  {self.line + 1 - 1}: {lines[self.line - 1].strip()}\n" if self.line > 0 else "")
            + f"  {Fore.yellow}{self.line + 1}: {error_line}{Style.reset}\n"
            + (f"  {self.line + 1 + 1}: {lines[self.line + 1].strip()}\n" if self.line < len(lines) - 1 else "")
            + f"{Fore.red}{self}{Style.reset}\n"
        )


def parse_macros(line: str, line_no: int) -> str:
    i = 0
    n = len(line)
    result = ""

    while i < n:
        if line[i] == "#":
            # Start of macro

            j = i + 1
            # Get macro name (letters, digits, underscore)
            while j < n and (line[j].isalnum() or line[j] == "_"):
                j += 1
            macro_name = line[i + 1 : j]
            arg_str = ""

            if j < n and line[j] == "(":
                # If macro has parentheses
                depth = 1
                k = j + 1
                # Skip over embedded macros and only return on the correct depth
                while k < n and depth > 0:
                    if line[k] == "(":
                        depth += 1
                    elif line[k] == ")":
                        depth -= 1
                    k += 1

                args_text = line[j + 1 : k - 1]  # Content inside parentheses

                # Recursively parse arguments
                arg_str = parse_macros(args_text, line_no)

                i = k
            else:
                # If macro does not have parentheses
                i = j

            # Replace macro with called macro function
            args = [arg.strip() for arg in arg_str.split(",") if arg.strip()]
            if macro_name in MACROS:
                resolved_macro = MACROS[macro_name].func(args, line_no)
            elif macro_name in UserMacroRegistry.macros:
                resolved_macro = UserMacroRegistry.apply_macro(macro_name, args, line_no)
            else:
                raise AssemblyError(f"Macro {Style.underline}{macro_name}{Style.res_underline} unknown", line_no, token=f"#{macro_name}")

            result += resolved_macro
        else:
            # If not macro just write back line character
            result += line[i]
            i += 1

    return result


def detect_param_type(param: str) -> set[ParamType]:
    if param.strip().startswith("R"):
        return {"reg"}
    else:
        return {"imm4", "imm8", "imm10", "addr"}


def resolve_instr_alias(instr: str, params: list[str]) -> str | None:
    for possible_instr in ALIASED_INSTRUCTIONS[instr]:
        possible_instr_info = INSTRUCTIONS[possible_instr]

        if len(possible_instr_info["params"]) != len(params):
            continue

        if all(possible_instr_param in detect_param_type(our_param) for our_param, possible_instr_param in zip(params, possible_instr_info["params"])):
            return possible_instr

    return None


def preprocess(lines: list[str]) -> tuple[list[tuple[int, str]], dict[str, int]]:
    processed_lines: list[tuple[int, str]] = []
    address: int = 0
    labels: dict[str, int] = {}

    for i, line in enumerate(lines):
        # Remove comments
        clean_line = line.split(";")[0].strip()

        # Identify and remove labels
        found_labels = re.findall(r"([^\s]+):", clean_line)
        if found_labels:
            for label in found_labels:
                if label in labels:
                    raise AssemblyError(f"Duplicate label {Style.underline}{label}{Style.res_underline} found", i, token=label)
                labels.update({label: address})
            clean_line = re.sub(r"[^\s]+:", "", clean_line).strip()

        # Parse Macros
        clean_line = parse_macros(clean_line, i)

        # Alias commands
        instr, params = split_line(clean_line)
        if instr in ALIASED_INSTRUCTIONS:
            real_instr = resolve_instr_alias(instr, params)
            if real_instr is None:
                raise AssemblyError(
                    f"Instruction {instr} with these parameters cannot be aliased to one of \n{"\n".join([f"  {possible_instr} - {", ".join(INSTRUCTIONS[possible_instr]["params"])}" for possible_instr in ALIASED_INSTRUCTIONS[instr]])}",
                    i,
                )
            clean_line = ",".join([real_instr, *params])

        # Remove empty lines
        if not clean_line:
            continue

        processed_lines.append((i, clean_line))
        address += 1

    return processed_lines, labels


def split_line(content: str) -> tuple[str, list[str]]:
    parts = re.split(r"[,\s]+", content)
    instr, *params = parts
    return instr, params


def parse_op(token: str, line: int) -> InstructionInfo | PseudoInstruction:
    instr = token.strip().upper()

    if instr in INSTRUCTIONS:
        return INSTRUCTIONS[instr]

    if instr in ASSEMBLER_PSEUDO_INSTRUCTIONS:
        return ASSEMBLER_PSEUDO_INSTRUCTIONS[instr]

    raise AssemblyError(f"Instruction {Style.underline}{token}{Style.res_underline} unknown", line, token=token)


def parse_register(token: str, line: int) -> int:
    match = re.fullmatch(r"R(\d+)", token.strip(), re.IGNORECASE)
    if not match:
        raise AssemblyError(f"Register {Style.underline}{token}{Style.res_underline} has invalid syntax", line, token=token)

    max_reg: int = (1 << PARAM_SIZE["reg"]) - 1

    reg_num = int(match.group(1))
    if not (0 <= reg_num <= max_reg):
        raise AssemblyError(f"Register {Style.underline}{token}{Style.res_underline} out of range (max {max_reg})", line, token=token)

    return reg_num


def parse_immediate(type: ParamType, token: str, line: int) -> int:
    try:
        val = int(token, 0)  # auto-detect binary/hex
    except ValueError:
        raise AssemblyError(f"Immediate value {Style.underline}{token}{Style.res_underline} has invalid syntax", line, token=token)

    max_immediate: int = (1 << PARAM_SIZE[type]) - 1
    if not (0 <= val <= max_immediate):
        raise AssemblyError(f"Immediate value {Style.underline}{token}{Style.res_underline} out of range (max {max_immediate})", line, token=token)

    return val


def parse_address(token: str, labels: dict[str, int], line: int) -> int:
    val = labels.get(token)

    if val is None:
        try:
            val = int(token, 0)  # auto-detect binary/hex
        except ValueError:
            raise AssemblyError(f"Address {Style.underline}{token}{Style.res_underline} has invalid syntax", line, token=token)

    max_address: int = (1 << PARAM_SIZE["addr"]) - 1
    if not (0 <= val <= max_address):
        raise AssemblyError(f"Address {Style.underline}{token}{Style.res_underline} out of range (max {max_address})", line, token=token)

    return val


def assemble_line(line: tuple[int, str], labels: dict[str, int]) -> int:
    line_no, content = line
    instr, params = split_line(content)

    instr_info = parse_op(instr, line_no)
    is_pseudo_instr = isinstance(instr_info, PseudoInstruction)

    expected_params = instr_info.get_expected_parameters() if is_pseudo_instr else len(instr_info["params"])
    if expected_params != len(params):
        raise AssemblyError(f"Instruction {Style.underline}{instr}{Style.res_underline} expects {expected_params} params, but got {len(params)}", line_no)

    if is_pseudo_instr:
        binary = instr_info.func(*params, line_no)
    else:
        binary = instr_info["opcode"]
        instruction_length = OPCODE_SIZE

        for param, ptype in zip(params, instr_info["params"]):
            match ptype:
                case "reg":
                    reg_num = parse_register(param, line_no)
                    binary = (binary << PARAM_SIZE["reg"]) | reg_num
                    instruction_length += PARAM_SIZE["reg"]
                case "imm4" | "imm8" | "imm10":
                    value = parse_immediate(ptype, param, line_no)
                    binary = (binary << PARAM_SIZE[ptype]) | value
                    instruction_length += PARAM_SIZE[ptype]
                case "addr":
                    addr = parse_address(param, labels, line_no)
                    binary = (binary << PARAM_SIZE["addr"]) | addr
                    instruction_length += PARAM_SIZE["addr"]

        binary <<= INSTRUCTION_SIZE - instruction_length

    return binary


def assemble(file: Path) -> list[int]:
    if not file.exists():
        raise Exception(f"{Fore.red}File {Style.underline}{file}{Style.res_underline} cannot be found{Style.reset}")

    with open(file, "r") as f:
        lines = f.readlines()

    try:
        processed_lines, labels = preprocess(lines)

        machine_code: list[int] = []
        for line in processed_lines:
            binary = assemble_line(line, labels)
            machine_code.append(binary)

    except AssemblyError as e:
        raise Exception(e.format_error(lines))

    return machine_code

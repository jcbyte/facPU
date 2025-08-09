from argparse import ArgumentParser
from pathlib import Path

import pyperclip
from colored import Fore, Style

from assembler import assemble
from factorio import generate_flasher_blueprint


def main():
    parser = ArgumentParser(description="facPU assembler")
    parser.add_argument("filename", type=str, help="Input assembly file")

    args = parser.parse_args()

    fpu_file = Path(args.filename)
    try:
        machine_code = assemble(fpu_file)
    except Exception as e:
        print(e)
        return

    factorio_blueprint = generate_flasher_blueprint(machine_code, label=fpu_file.name)
    pyperclip.copy(factorio_blueprint)
    print(
        f"{Fore.green}Factorio blueprint generated{Style.reset}\n"
        + f"{Fore.cyan}{Style.underline}{factorio_blueprint}{Style.reset}\n"
        + f"{Fore.yellow}This has also been copied to your clipboard{Style.reset}"
    )


if __name__ == "__main__":
    main()

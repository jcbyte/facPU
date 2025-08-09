from argparse import ArgumentParser
from pathlib import Path

from assembler import assemble


def main():
    parser = ArgumentParser(description="facPU assembler")
    parser.add_argument('filename', type=str, help='Input assembly file')

    args = parser.parse_args()

    fpu_file = Path(args.filename)
    try:
      machine_code = assemble(fpu_file)
    except Exception as e:
        print(e)
        return

    print(machine_code)

if __name__ == "__main__":
    main()
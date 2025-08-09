from argparse import ArgumentParser
from pathlib import Path

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
    print(factorio_blueprint)


if __name__ == "__main__":
    main()

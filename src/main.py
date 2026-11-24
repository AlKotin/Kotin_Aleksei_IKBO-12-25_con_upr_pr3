"""Command-line assembler for the educational virtual machine."""

import argparse

from src.assembler import read_program
from src.encoder import (
    encode_instruction,
    encode_program,
    format_bytes,
    save_program,
)


def main():
    """Assemble YAML, write binary code, and show test bytes."""
    parser = argparse.ArgumentParser(description="UVM assembler")
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    try:
        program = read_program(args.source)
        save_program(args.output, encode_program(program))
    except (ValueError, OSError) as error:
        parser.error(str(error))

    print(f"Assembled instructions: {len(program)}")
    if args.test:
        for command in program:
            data = encode_instruction(command)
            print(f"{command.name}: {format_bytes(data)}")


if __name__ == "__main__":
    main()
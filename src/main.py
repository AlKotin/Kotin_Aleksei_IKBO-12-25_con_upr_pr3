"""Командная строка ассемблера первого этапа."""

import argparse

from src.assembler import read_program


def main():
    """Прочитать программу и показать поля в тестовом режиме."""
    parser = argparse.ArgumentParser(description="Ассемблер УВМ")
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    try:
        program = read_program(args.source)
    except ValueError as error:
        parser.error(str(error))

    if args.test:
        for number, command in enumerate(program, start=1):
            fields = f"A={command.field_a}"
            if command.field_b is not None:
                fields += f", B={command.field_b}"
            print(f"{number}. {command.name}: {fields}")
    else:
        print(f"Разобрано команд: {len(program)}")


if __name__ == "__main__":
    main()
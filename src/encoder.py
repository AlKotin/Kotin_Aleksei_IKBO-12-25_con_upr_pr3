"""Encode UVM instructions into five-byte machine words."""

from pathlib import Path

INSTRUCTION_BYTES = 5
OPCODE_BITS = 6


def encode_instruction(command):
    """Store field A in low bits and field B above it."""
    word = command.field_a
    if command.field_b is not None:
        word |= command.field_b << OPCODE_BITS
    return word.to_bytes(INSTRUCTION_BYTES, byteorder="little")


def encode_program(program):
    """Join encoded instructions into one binary program."""
    return b"".join(encode_instruction(item) for item in program)


def save_program(path, data):
    """Write the binary program to the requested path."""
    Path(path).write_bytes(data)


def format_bytes(data):
    """Format bytes as hexadecimal values for test mode."""
    return ", ".join(f"0x{byte:02X}" for byte in data)
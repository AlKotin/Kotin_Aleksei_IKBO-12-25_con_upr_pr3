"""Check UVM machine-code generation against the specification."""

import tempfile
import unittest
from pathlib import Path

from src.assembler import read_program
from src.encoder import encode_instruction, encode_program, save_program

EXPECTED = [
    bytes.fromhex("3A AB 00 00 00"),
    bytes.fromhex("25 00 00 00 00"),
    bytes.fromhex("38 00 00 00 00"),
    bytes.fromhex("0E 00 00 00 00"),
]


class EncoderTests(unittest.TestCase):
    """Check each instruction and the complete binary file."""

    def test_specification_bytes(self):
        """Match all four byte sequences from the UVM specification."""
        program = read_program("examples/spec.yaml")
        actual = [encode_instruction(item) for item in program]
        self.assertEqual(actual, EXPECTED)

    def test_binary_file(self):
        """Write the complete program in instruction order."""
        program = read_program("examples/spec.yaml")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "program.bin"
            save_program(path, encode_program(program))
            self.assertEqual(path.read_bytes(), b"".join(EXPECTED))


if __name__ == "__main__":
    unittest.main()
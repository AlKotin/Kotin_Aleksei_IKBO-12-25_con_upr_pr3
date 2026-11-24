"""Проверки разбора команд варианта 9."""

import unittest

from src.assembler import Instruction, parse_program, read_program


class AssemblerTests(unittest.TestCase):
    """Проверить поля команд и ошибки исходного файла."""

    def test_specification_commands(self):
        """Сравнить поля четырёх команд со спецификацией."""
        program = read_program("examples/spec.yaml")
        expected = [
            Instruction("LOAD_CONST", 58, 684),
            Instruction("READ", 37),
            Instruction("WRITE", 56),
            Instruction("BITREVERSE", 14),
        ]
        self.assertEqual(program, expected)

    def test_unknown_command(self):
        """Отклонить команду, отсутствующую в УВМ."""
        with self.assertRaisesRegex(ValueError, "Неизвестная команда"):
            parse_program("- UNKNOWN:\n")

    def test_constant_overflow(self):
        """Отклонить константу за пределами поля B."""
        with self.assertRaisesRegex(ValueError, "не помещается"):
            parse_program("- LOAD_CONST: 1073741824\n")

    def test_unexpected_operand(self):
        """Отклонить операнд у команды без поля B."""
        with self.assertRaisesRegex(ValueError, "не принимает"):
            parse_program("- READ: 5\n")


if __name__ == "__main__":
    unittest.main()
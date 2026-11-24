"""Разбор YAML-программы в команды учебной виртуальной машины."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

OPCODES = {
    "LOAD_CONST": 58,
    "READ": 37,
    "WRITE": 56,
    "BITREVERSE": 14,
}
COMMAND_FIELDS = 1
MIN_CONSTANT = 0
MAX_CONSTANT = (1 << 30) - 1


@dataclass(frozen=True)
class Instruction:
    """Команда с полями из спецификации УВМ."""

    name: str
    field_a: int
    field_b: Optional[int] = None


def parse_instruction(item):
    """Проверить одну YAML-команду и создать её представление."""
    if not isinstance(item, dict) or len(item) != COMMAND_FIELDS:
        raise ValueError("Команда должна содержать ровно одно поле")

    name, value = next(iter(item.items()))
    if not isinstance(name, str) or name not in OPCODES:
        raise ValueError(f"Неизвестная команда: {name}")

    if name == "LOAD_CONST":
        if type(value) is not int:
            raise ValueError("LOAD_CONST требует целую константу")
        if value < MIN_CONSTANT or value > MAX_CONSTANT:
            raise ValueError("Константа не помещается в поле B")
    elif value is not None:
        raise ValueError(f"Команда {name} не принимает операнд")

    return Instruction(name, OPCODES[name], value)


def parse_program(text):
    """Преобразовать YAML-текст в список команд."""
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as error:
        raise ValueError(f"Ошибка YAML: {error}") from error

    if not isinstance(data, list) or not data:
        raise ValueError("Программа должна быть непустым списком")

    return [parse_instruction(item) for item in data]


def read_program(path):
    """Прочитать исходный файл и разобрать программу."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ValueError(f"Не удалось прочитать файл: {error}") from error
    return parse_program(text)
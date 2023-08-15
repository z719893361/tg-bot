import inspect
import sys
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from typing import TypeVar, List, Type

T = TypeVar('T')


def load_classes_from_directory(directory: Path, base_class: Type[T]) -> List[Type[T]]:
    for path in directory.glob('*'):
        if not path.match('*.py'):
            continue
        spec = spec_from_file_location(__name__, path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, base_class) and cls != base_class:
                yield cls


def scan_and_load(directory: Path, current):
    for path in directory.glob('*'):
        if path == current:
            continue
        if path.match('*.py'):
            spec = spec_from_file_location(__name__, path)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
        if path.is_dir():
            scan_and_load(path, current)

import functools
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


@functools.lru_cache()
def get_project_root():
    current_path = Path(__file__)
    for _ in range(__name__.count('.') + 1):
        current_path = current_path.parent
    return current_path


def scan_and_load(directory: Path):
    root = get_project_root()

    for path in directory.glob('*'):
        if path.is_dir():
            scan_and_load(path)
        if not path.match('*.py'):
            continue
        module_name = path.relative_to(root).as_posix().replace('/', '.').replace('\\', '.').rstrip('.py')
        if module_name in sys.modules:
            continue
        spec = spec_from_file_location(module_name, path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
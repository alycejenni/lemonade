import importlib
import os
from abc import ABCMeta
from modules.undefined import Undefined

lem_mod_files = [m.replace('.py', '') for m in os.listdir('/home/alice/shell/scripts/eyecandy/lemonade/modules') if
                 not m.startswith('_') and m.endswith('.py')]
lem_mod = {m: importlib.import_module('modules.' + m) for m in lem_mod_files}
modules = {}
for name, imported in lem_mod.items():
    items = [getattr(imported, i) for i in dir(imported) if not i.startswith('_')]
    try:
        cls = next(i for i in items if
                   isinstance(i, ABCMeta) and hasattr(i, 'name') and i.name == name)
        modules[name] = cls
    except StopIteration:
        continue


def get_module(module_name):
    return modules.get(module_name, Undefined)

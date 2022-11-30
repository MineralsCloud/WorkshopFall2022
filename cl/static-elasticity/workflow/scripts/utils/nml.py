import re
from itertools import tee
import io
import f90nml
import re

def is_nml_start(line):
    return line.strip().startswith("&")
def is_nml_end(line):
    return line.strip().endswith("/")

def _func(nml: list, other: list) -> str:
    return "".join(nml + other)

def transform(fp: io.StringIO, func: callable = _func):

    lines = fp.readlines()
    start = False
    last = 0

    for i, line in enumerate(lines):
        if is_nml_start(line):
            start = True
        if start and is_nml_end(line):
            start = False
            last = i + 1

    return func(lines[:last], lines[last:])

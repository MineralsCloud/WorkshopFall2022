import sys
import click
import io
import numpy
import re

from utils.units import _from_ang3
from utils.voigt import e_, E_

def make_strain(key: E_, value: float):
    i, j = key.s
    e = numpy.zeros((3, 3))
    e[i-1, j-1] = 1
    e[j-1, i-1] = 1
    strain = numpy.diag([1, 1, 1]) + e * value
    return strain

@click.command()
@click.option("-e", help="Strain key")
@click.option("-v", "--value", type=click.FLOAT, help="Amount of strain")
def main(e: str, value: float):

    for line in sys.stdin:
        sys.stdout.write(line)
        if "CELL_PARAMETERS" in line: break
    
    lattice = ""
    for _ in range(3):
        line = sys.stdin.readline()
        lattice += line
    lattice = numpy.loadtxt(io.StringIO(lattice))

    # Start transform
    if e and value:
        key = e_(re.search(r"(\d+)$", e).group(1))
        lattice = lattice @ make_strain(key, value)
    # End of transform

    for i in range(3):
        sys.stdout.write(" " * 4 + "".join("%16.8f" % x for x in lattice[i]) + "\n")

    sys.stdout.write(sys.stdin.read())

    
if __name__ == "__main__":
    main()

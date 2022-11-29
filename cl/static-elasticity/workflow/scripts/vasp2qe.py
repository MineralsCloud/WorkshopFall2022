'''Convert vasp coordinates to QE input format
'''

import click
from pathlib import Path
from utils.units import _from_ang
import numpy
from io import StringIO
from collections import OrderedDict
import sys


@click.command(help=__doc__)
@click.argument("fname", type=click.Path(exists=True))
def main(fname: str):
    with open(fname) as fp:
        fp.readline()

        # lattice parameters

        alat = float(fp.readline().strip())

        sio = StringIO()
        for _ in range(3): sio.write(fp.readline())
        sio.seek(0)
        lattice = numpy.loadtxt(sio) * alat

        sys.stdout.write("CELL_PARAMETERS (bohr)\n")
        lattice = _from_ang(lattice)
        for i in range(3):
            sys.stdout.write(" ".join("%16.8f" % x for x in lattice[i]))
            sys.stdout.write("\n")
        
        # empty line

        sys.stdout.write("\n")

        # atomic types 

        typen = fp.readline().strip().split()
        typec = (int(x) for x in fp.readline().strip().split())
        types = OrderedDict(zip(typen, typec))

        # direct

        line = fp.readline().strip()
        if line == "Direct":
            sys.stdout.write("ATOMIC_POSITIONS (crystal)\n")
        else:
            raise NotImplementedError(f"{line} coords not supported")

        # atomic positions

        for typen, typec in types.items():
            for _ in range(typec):
                line = fp.readline()
                sys.stdout.write("%-3s" % typen + line)

if __name__ == "__main__":
    main()
import sys
import click
import io
import numpy

# from utils.units import _from_ang3

@click.command()
@click.option("-v", "--volume", type=click.FLOAT)
def main(volume: float):

    # volume = _from_ang3(volume)

    for line in sys.stdin:
        sys.stdout.write(line)
        if "CELL_PARAMETERS" in line: break
    
    lattice = ""
    for _ in range(3):
        line = sys.stdin.readline()
        lattice += line
    lattice = numpy.loadtxt(io.StringIO(lattice))

    # Start transform
    v0 = numpy.linalg.det(lattice)
    lattice *= ((volume / v0) ** (1/3))
    # End of transform

    for i in range(3):
        sys.stdout.write(" " * 4 + "".join("%16.8f" % x for x in lattice[i]) + "\n")

    sys.stdout.write(sys.stdin.read())

    
if __name__ == "__main__":
    main()

import click
import io
import numpy
import sys

def get_abc(fp: io.StringIO):

    lines = fp.readlines()
    i = next(i for i, line in enumerate(lines) if line.strip().upper().startswith("CELL_PARAMETERS"))

    sio = io.StringIO()
    sio.writelines(lines[i+1:i+4])
    sio.seek(0)

    lattice = numpy.loadtxt(sio)
    return numpy.linalg.norm(lattice, axis=1).tolist()

@click.command()
@click.argument("fnames", nargs=-1)
def main(fnames: list):
    for fname in fnames:
        with open(fname) as fp:
            abc = get_abc(fp)
            sys.stdout.write(" ".join("%16.8f" % x for x in abc) + "\n")

if __name__ == "__main__":
    main()
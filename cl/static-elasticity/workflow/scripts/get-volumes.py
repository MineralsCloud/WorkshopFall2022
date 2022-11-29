'''Get a list of volumes
'''

import click
import numpy
import sys
import json


@click.command(help=__doc__)
@click.argument("vmin", type=click.FLOAT)
@click.argument("vmax", type=click.FLOAT)
@click.argument("nv", type=click.INT)
def main(vmin, vmax, nv):
    v_array = numpy.round(numpy.linspace(vmin, vmax, nv), 2).tolist()
    json.dump(v_array, sys.stdout)
    sys.stdout.write("\n")

if __name__ == "__main__":
    main()

from pathlib import Path
import click
import pandas
from utils.voigt import c_
import itertools
import sys
import numpy

columns = [
    "c11", "c22", "c33",
    "c12", "c13", "c23",
    "c44", "c55", "c66",
    "c14", "c15", 
    "c24", "c25",
    "c46",
    "c56"
]


@click.command()
@click.argument("fnames", nargs=-1, type=click.Path())
@click.option("--pve", type=click.Path(exists=True))
def main(fnames: str, pve: str):

    df = pandas.DataFrame(columns=columns, index=range(len(fnames)))

    for i, fname in enumerate(fnames):

        if not Path(fname).exists(): continue

        cij = numpy.loadtxt(fname)
        for col in columns:
            k, l = c_(col[1:]).v
            df.loc[i, col] = cij[k-1, l-1]
    
    if pve:
        df2 = pandas.read_table(pve, sep=r"\s+", header=0)
        df = pandas.concat([df2.loc[:, ["P", "V"]], df], sort=True, axis=1)
    
    sys.stdout.write(df.to_string(index=False))
    
if __name__ == "__main__":
    main()
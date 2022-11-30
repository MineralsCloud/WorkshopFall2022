import click
import sh
import numpy
import io
from pathlib import Path
from utils.units import _to_gpa
import sys
from utils.voigt import e_

import pandas

def get_stress_tensor(fname) -> numpy.ndarray:
    out = sh.grep("total   stress", "-A", 3, fname)
    out = sh.tail(out, "-3")
    out = sh.cut(out, "-c-40")
    tensor = out.stdout.decode()
    return numpy.loadtxt(io.StringIO(tensor))


@click.command()
@click.argument("dirname", type=click.Path(exists=True, file_okay=False))
@click.option("--strain", type=click.FLOAT, required=True)
def main(dirname: str, strain: float):

    dirname = Path(dirname)
    c = numpy.zeros((6, 6))

    for i in range(6):

        try:
            elast_out = dirname / f"e{i+1}" / f"{strain}" / "elast.out"
            if not elast_out.exists(): continue
            sp = get_stress_tensor(str(elast_out))

            elast_out = dirname / f"e{i+1}" / f"{-strain}" / "elast.out"
            if not elast_out.exists(): continue
            sm = get_stress_tensor(str(elast_out))

            for j in range(6):
                l, m = e_(j+1).s
                moduli = (sm[l-1, m-1] - sp[l-1, m-1]) / strain / 2

                if i in {3, 4, 5}:
                    moduli /= 2

                c[i, j] = moduli
                c[j, i] = moduli
        
        except Exception as e:
            raise e
        
    sys.stdout.write(pandas.DataFrame(_to_gpa(c)).to_string(header=False, index=False))
    sys.stdout.write("\n")

if __name__ == "__main__":
    main()

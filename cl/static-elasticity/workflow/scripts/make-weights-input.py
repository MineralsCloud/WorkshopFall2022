from utils import nml
import f90nml
import click
import sys
from io import StringIO 

def fmt(nk):
    def _fmt(nml, others) -> str:
        sio = StringIO()
        nml = f90nml.reads("".join(nml))

        # change verbosity to high
        nml["control"]["verbosity"] = "high"

        i = next(i for i, line in enumerate(others) if line.strip().upper().startswith("K_POINTS"))
        others[i] = "K_POINTS (automatic)\n"
        others[i+1] = "  ".join("%d" % x for x in (*nk, 0, 0, 0)) + "\n"

        f90nml.write(nml, sio)
        sio.writelines(others)
        return sio.getvalue()
    return _fmt


@click.command()
@click.argument("fname", type=click.Path(exists=True))
@click.option("--nk", required=True)
def main(fname: str, nk: str):
    with open(fname) as fp:
        nk = (float(x) for x in nk.strip().split(","))
        sys.stdout.write(nml.transform(fp, fmt(nk)))

if __name__ == "__main__":
    main()
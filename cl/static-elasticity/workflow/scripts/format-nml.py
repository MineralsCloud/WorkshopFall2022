from utils import nml
import f90nml
import click
import sys
from io import StringIO 

def fmt(nml, others) -> str:
    sio = StringIO()
    nml = f90nml.reads("".join(nml))
    f90nml.write(nml, sio)
    sio.writelines(others)
    return sio.getvalue()


@click.command()
@click.argument("fname", type=click.Path(exists=True))
def main(fname: str):
    with open(fname) as fp:
        sys.stdout.write(nml.transform(fp, fmt))

if __name__ == "__main__":
    main()
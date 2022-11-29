import click
from utils.qeout import find
import sys

@click.command()
@click.argument('fnames', nargs=-1, type=click.Path(exists=True))
def main(fnames: str):
    sys.stdout.write("%12s %12s %12s\n" % ("P", "V", "E"))
    for fname in fnames:
        E = find.find_final_energy(fname)
        P = find.find_final_pressure(fname)
        V = find.find_volume(fname)
        sys.stdout.write(f"{P:12.06f} {V:12.06f} {E:12.06f}\n")

if __name__ == "__main__":
    main()

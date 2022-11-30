import matplotlib.pyplot as plt
import click
import sh
import pathlib
from utils.units import _to_ev


def get_energy(fname):
    line = sh.grep("!", fname).stdout.decode()
    return float(line.strip().split()[-2])

@click.command()
@click.argument("input", nargs=-1)
@click.option("--output")
def main(input, output):
    names = []
    energies = []
    for fname in input:
        names.append(pathlib.Path(fname).parent.name)
        energies.append(_to_ev(get_energy(fname)))
    plt.plot(names, energies, marker="o")
    plt.ylabel("Total energy (eV)")
    plt.savefig(output)


if __name__ == "__main__":
    main()
    
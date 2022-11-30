import click
import pandas
from matplotlib import pyplot as plt

@click.command()
@click.argument("fname", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path())
@click.option("-k", "--keys")
def main(fname: str, output: str, keys: str):
    df = pandas.read_table(fname, sep=r"\s+")
    df.loc[:, "P"] /= 10
    if not keys:
        keys = df.columns[2:]
    else:
        keys = keys.split(",")
    df.plot(x="P", y=keys, ax=plt.gca(), marker="o")
    plt.xlabel("$P$ (GPa)")
    plt.ylabel("$C_{ij}$ (GPa)")
    plt.ylim(bottom=0)
    plt.xlim(left=0)
    plt.legend(ncol=2)
    plt.savefig(output)

if __name__ == "__main__":
    main()
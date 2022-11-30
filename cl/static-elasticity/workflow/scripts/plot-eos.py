import click
import pandas
from utils.static_eos import fit_f_of_v, get_p_of_v_from_f
from utils.units import _to_ang3, _to_ev, _to_gpa
from matplotlib import pyplot as plt
import numpy

@click.command()
@click.argument("fnames", nargs=-1, type=click.Path(exists=True))
def main(fnames: str):

    plt.figure()

    for fname in fnames:
        df = pandas.read_table(fname, sep="\s+", header=0, index_col=None)
        print(df)
        v_array = numpy.linspace(df['V'].min(), df['V'].max())
        f_of_v = fit_f_of_v(df["V"].values, df["E"].values)
        line, = plt.plot(_to_ang3(v_array), _to_ev(f_of_v(v_array)))
        plt.scatter(_to_ang3(df['V'].to_numpy()), _to_ev(df['E'].to_numpy()), color=line.get_color())
        
    plt.xlabel("$V$ (Å$^3$)")
    plt.ylabel("$F$ (eV)")
    plt.savefig("FxV.png", dpi=144)

    plt.figure()

    for fname in fnames:
        df = pandas.read_table(fname, sep="\s+", header=0, index_col=None)
        v_array = numpy.linspace(df['V'].min(), df['V'].max())
        p_of_v = get_p_of_v_from_f(df["V"].values, df["E"].values)
        line, = plt.plot(_to_gpa(p_of_v(v_array)), _to_ang3(v_array))
        plt.scatter(df['P'].to_numpy() / 10, _to_ang3(df['V'].to_numpy()), color=line.get_color())

    plt.xlabel("$P$ (GPa)")
    plt.ylabel("$V$ (Å$^3$)")
    plt.savefig("VxP.png", dpi=144)


if __name__ == "__main__":
    main()
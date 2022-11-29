import pandas
from utils.static_eos import get_p_of_v_from_f
from scipy.optimize import root
from utils.units import _to_ang3, _to_gpa
from scipy.misc import derivative
import click

@click.command()
@click.argument("fname", type=click.Path(exists=True))
@click.option("--order", type=click.IntRange(2, 4), default=3)
def main(fname, order):

    df = pandas.read_table(fname, sep="\s+", header=0, index_col=None)
    p_of_v = get_p_of_v_from_f(df["V"].values, df["E"].values, order=order)
    k_of_v = lambda v: - v * derivative(p_of_v, v, 1e-3)

    v0 = df["V"][0]

    v0 = root(lambda v: p_of_v(v), x0=v0).x[0]
    k0 = k_of_v(v0)
    kp0 = derivative(k_of_v, v0, 1e-3) / derivative(p_of_v, v0, 1e-3)

    print("%8.2f %8.1f %8.2f" % (_to_ang3(v0), _to_gpa(k0), kp0))

if __name__ == "__main__":
    main()

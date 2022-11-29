import click

def get_cmap(cmap: str = None, vmin=0, vmax=2000):
    import matplotlib
    from palettable.cartocolors.qualitative import Prism_10
    if cmap != None:
        cmap = Prism_10.mpl_colormap
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = matplotlib.cm.get_cmap(cmap)
    return matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)

@click.command()
@click.option("-T", "--transpose", is_flag=True)
@click.argument("fname", type=click.Path())
def main(fname, **kwargs):
    import matplotlib.pyplot as plt
    import pandas

    df = pandas.read_table(fname, sep=r"\s+", header=0, index_col=0)
    df.columns = [float(x) for x in df.columns]

    if kwargs.pop("transpose"): df = df.T

    cmap = get_cmap(vmin=df.index.min(), vmax=df.index.max())
    for idx, row in df.iterrows():
        # plt.plot(df.columns, row, label=idx, color=cmap.to_rgba(idx))
        plt.plot(df.columns, row, label=idx)

    plt.xlim(df.columns.min(), df.columns.max())
    plt.ylim(bottom=0)
    plt.ylim(2000, 5500)

    plt.axvline(1126.9719, c="k", lw=1)

    # plt.legend()
    plt.savefig(fname + ".png", dpi=300)

if __name__ == "__main__":
    main()
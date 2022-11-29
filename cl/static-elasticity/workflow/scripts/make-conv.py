import click
import jinja2
import sys

@click.command()
@click.argument("fname", required=True)
@click.option("--kpts", required=True)
@click.option("--ecutwfc", required=True, type=click.FLOAT)
def main(fname, kpts, ecutwfc):
    kpts = kpts.split("x")
    with open(fname) as fp:
        tp = jinja2.Template(fp.read())
    sys.stdout.write(tp.render(kpts=kpts, ecutwfc=ecutwfc))

if __name__ == "__main__":
    main()
import click
from pathlib import Path
import importlib

# with open(Path(__file__).parent / "../version.py") as fp: exec(fp.read())

@click.group()
@click.version_option(prog_name="Thermal toolset")
def main():
    pass

mdl = importlib.import_module("vasp2qe")
main.add_command(mdl.main, "convert-vasp-to-qe")

mdl = importlib.import_module("get-volumes")
main.add_command(mdl.main, "get-volume-list")



if __name__ == "__main__":
    main()
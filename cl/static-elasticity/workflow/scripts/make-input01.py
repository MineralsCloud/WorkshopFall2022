import jinja2
import f90nml
import click
import sys
import io
from utils.qeout import find
from pathlib import Path
import numpy

from utils.evec_load import evec_load
from utils.evec_sort import evec_sort

def dump_freqs(fname: str) -> str:
    sio = io.StringIO()
    with open(fname) as fp:
        info = fp.readline()
        nml = f90nml.reads(info)
        nbnd = int(nml["plot"]["nbnd"])
        nks = int(nml["plot"]["nks"])
        for ik in range(nks):
            # sio.write(f"#{ik}>\n")
            line = fp.readline().lstrip()
            sio.write(line)
            for ibnd in range(int(nbnd / 6)):
                # print(f"~{ibnd}~>\n")
                line = fp.readline()
                for i in range(6):
                    sio.write(line[(i * 10):((i + 1) * 10)] + "\n")
    sio.seek(0)
    return nbnd, nks, sio.read()

def find_volume(fname: str) -> float:
    lattice = numpy.loadtxt(fname, skiprows=1, max_rows=3)
    return numpy.linalg.det(lattice)

@click.command()
@click.argument("fnames", nargs=-1, type=click.Path())
@click.option("-s", "--sort-by", default="")
@click.option("-m", "--sort-amass", default="")
@click.option("-c", "--comment", default="")
def main(fnames: list, comment: str, sort_by: str, sort_amass: str):

    sys.stdout.write(f"{comment}\n\nnv  nk  np  nm  na\n")

    for ifile, fname in enumerate(reversed(fnames)):
        fscf=Path(fname).parent / "scf.out"
        fstct=Path(fname).parent / "init.qe"
        pressure=find.find_final_pressure(fscf)
        volume=find_volume(fstct)
        energy=find.find_final_energy(fscf)
        nbnd, nks, content = dump_freqs(fname)

        if ifile == 0:
            sys.stdout.write(f"{len(fnames)}  {nks}  {nbnd}   1  {int(nbnd / 3)}\n\n")

        sys.stdout.write(f"P= {pressure}  V= {volume:.4f}  E= {energy}\n")

        if sort_by == "":
            sys.stdout.write(content)
        else:
            evecs = evec_load(Path(fname).parent / sort_by, nks, nbnd)
            for iq, (q_coord, modes) in enumerate(evecs):
                sys.stdout.write(f"{q_coord[0]:11.8f} {q_coord[1]:11.8f} {q_coord[2]:11.8f}\n")
                if ifile != 0:
                    curr_eigs = numpy.array([            modes[ibnd][1] for ibnd in range(nbnd)]) 
                    prev_eigs = numpy.array([prev_evecs[iq][1][ibnd][1] for ibnd in range(nbnd)]) 
                    if sort_amass != "":
                        raise NotImplementedError
                    modes = evec_sort(modes, curr_eigs, prev_eigs)
                for (mode_id, thz, cm_1), _ in modes:
                    sys.stdout.write(f"{cm_1:10.4f}\n")
                evecs[iq] = (q_coord, modes)
            prev_evecs = evecs
 
if __name__ == "__main__":
    main()

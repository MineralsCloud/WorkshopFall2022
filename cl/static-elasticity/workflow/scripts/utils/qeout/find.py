import sh
import re
import io
import numpy

__all__ = ["find_energy", "find_pressure", "find_final_energy", "find_structure"]

def find_energy(fname):
    ret = sh.grep("!", fname)
    return float(re.search(r"(-?\d+\.?\d+)*\s+Ry", ret.stdout.decode()).group(1))

def find_final_energy(fname):
    ret = sh.grep("-m1", "!",fname)
    return float(re.search(r"(-?\d+\.?\d+)*\s+Ry", ret.stdout.decode()).group(1))

def find_pressure(fname):
    ret = sh.grep("P=", fname)
    return float(re.search(r"P=\s*(-?\d+\.?\d+)", ret.stdout.decode()).group(1))

def find_final_pressure(fname):
    ret = sh.grep("P=", "-m1",fname)
    return float(re.search(r"P=\s*(-?\d+\.?\d+)", ret.stdout.decode()).group(1))

def find_volume(fname):
    ret = sh.grep(sh.grep("Begin final coordinates", "-A", 1, fname), "new unit-cell volume")
    return float(re.search(r"=\s+(\S+)\s+a\.u\.\^3", ret.stdout.decode()).group(1))


def find_structure(fname, nat: int):
    ret = sh.grep("CELL_PARAMETERS", "-A", 3, fname)
    _ret = "\n".join(ret.stdout.decode().split("\n")[-5:])
    cell_unit = _ret.split("\n")[0].strip().split()[1][1:-1]
    lattice_parameter = numpy.loadtxt(io.StringIO(_ret), skiprows=1)
    ret = sh.grep("ATOMIC_POSITIONS", "-A", nat, fname)
    _ret = "\n".join(ret.stdout.decode().split("\n")[-nat-2:])
    atom_unit = _ret.split("\n")[0].strip().split()[1][1:-1]
    unit_cell = []
    for line in _ret.split("\n")[1:-1]:
        atom, x, y, z = line.strip().split()
        unit_cell.append((atom, float(x), float(y), float(z)))
    return lattice_parameter, unit_cell, cell_unit, atom_unit

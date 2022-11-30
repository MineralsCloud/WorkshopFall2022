from .find import find_structure
from crystals import Crystal, Atom
from .units import _to_ang

def read_qe(fname, nat: int):

    lattice_parameter, unit_cell, cell_unit, atom_unit = find_structure(fname, nat)

    if cell_unit == "bohr":
        lattice_parameter = _to_ang(lattice_parameter)
    else:
        raise RuntimeError(f"Unknown cell unit {cell_unit}")

    unit_cell = [
        Atom(atom, (x, y, z))
        for atom, x, y, z in unit_cell
    ]

    return Crystal(unit_cell,  lattice_parameter)

if __name__ == "__main__":
    import sys
    print(read_qe(sys.argv[1], int(sys.argv[2])))

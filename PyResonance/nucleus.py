from dataclasses import dataclass
from numpy import uint32
from pathlib import Path

U2MEV: float = 931.4940954
ELECTRON_MASS: float = 0.000548579909

@dataclass
class Nucleus:
    id: uint32 = 0
    z: int = 0
    a: int = 0
    mass: float = 0.0
    element: str = ""
    isotope: str = ""


def get_nucleus_uuid(z: uint32, a: uint32) -> uint32:
    return z*z + z + a if z > a else a*a + z

def get_symbol_latex(nuc: Nucleus) -> str:
    return f"$^{nuc.a}${nuc.element}"

def generate_nucleus_table(filename) -> dict[uint32, Nucleus]:
    massDict: dict[uint32, Nucleus] = {}
    with open(filename) as massfile:
        massfile.readline()
        massfile.readline()
        for line in massfile:
            nuc = Nucleus()
            entries = line.split()
            nuc.z = int(entries[1])
            nuc.a = int(entries[2])
            nuc.id = get_nucleus_uuid(nuc.z, nuc.a)
            nuc.mass = (float(entries[4])  + 1.0e-6 * float(entries[5]) - float(nuc.z) * ELECTRON_MASS) * U2MEV
            nuc.element = entries[3]
            nuc.isotope = f"{nuc.a}{nuc.element}"
            massDict[nuc.id] = nuc
    return massDict
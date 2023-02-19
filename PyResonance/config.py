from dataclasses import dataclass, field
from .nucleus import Nucleus, get_nucleus_uuid, generate_nucleus_table, get_symbol_latex
from typing import Optional
import json

@dataclass
class Parameters:
    target: Nucleus = Nucleus()
    projectile: Nucleus = Nucleus()
    ejectile: Nucleus = Nucleus()
    residual: Nucleus = Nucleus()
    resonance_energy: float = 0.0 #MeV
    width_in: float = 0.0 #MeV
    width_out: float = 0.0 #MeV
    width_total: float = 0.0 #MeV
    spin_target: float = 0
    spin_projectile: float = 0
    spin_resonance: float = 0
    name: str = ""

def get_reaction_equation_latex(params: Parameters) -> str:
    return f"{get_symbol_latex(params.target)}({get_symbol_latex(params.projectile)},{get_symbol_latex(params.ejectile)}){get_symbol_latex(params.residual)}"

def get_reaction_name(params: Parameters) -> str:
    return f"{params.name} {get_reaction_equation_latex(params)}"

@dataclass
class Config:
    parameter_list: list[Parameters] = field(default_factory=list)
    energy_min: float = 0.0
    energy_max: float = 0.0
    energy_npoints: int = 0

def read_config(filename: str, nucdatafile: str) -> Optional[Config]:
    nuc_dict = generate_nucleus_table(nucdatafile)
    config = Config()
    with open(filename) as parfile:
        data = json.load(parfile)
        config.energy_min = data["energy_min"]
        config.energy_max = data["energy_max"]
        config.energy_npoints = data["energy_npoints"]
        for res in data["resonances"]:
            params = Parameters()
            params.name = res["name"]
            params.target = nuc_dict[get_nucleus_uuid(res["Z_target"], res["A_target"])]
            params.projectile = nuc_dict[get_nucleus_uuid(res["Z_projectile"], res["A_projectile"])]
            params.ejectile = nuc_dict[get_nucleus_uuid(res["Z_ejectile"], res["A_ejectile"])]
            
            zr = params.target.z + params.projectile.z - params.ejectile.z
            ar = params.target.a + params.projectile.a - params.ejectile.a

            if zr < 0 or ar <= 0:
                print(f"Illegal residual nucleus ZR:{zr} AR:{ar}")
                return None
            params.residual = nuc_dict[get_nucleus_uuid(zr, ar)]

            params.resonance_energy = res["resonance_energy"]
            params.width_in = res["width_in"]
            params.width_out = res["width_out"]
            params.width_total = res["width_total"]
            params.spin_target = res["spin_target"]
            params.spin_projectile = res["spin_projectile"]
            params.spin_resonance = res["spin_resonance"]
            config.parameter_list.append(params)

    return config
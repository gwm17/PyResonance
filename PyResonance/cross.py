from .config import Parameters
import numpy as np
from numpy.typing import NDArray

HBAR_C: float = 197.3269804 #MeV*fm CODATA
FM2_TO_MBARN: float = 10.0 #mbarn/fm

def reduced_mass(params: Parameters) -> float:
    return params.target.mass * params.projectile.mass / (params.target.mass + params.projectile.mass)

def wavenumber_sq(params: Parameters, energy: float) -> float:
    return 2.0 * reduced_mass(params) * energy / (HBAR_C ** 2.0 * FM2_TO_MBARN)

def spin_factor(params: Parameters) -> float:
    resonance_factor = 2.0 * params.spin_resonance + 1
    target_factor = 2.0 * params.spin_target + 1
    projectile_factor = 2.0 * params.spin_projectile + 1
    return resonance_factor / (target_factor * projectile_factor)

def breit_wigner(params: Parameters, energy: float) -> float:
    energy_diff = energy - params.resonance_energy
    return params.width_in * params.width_out / (energy_diff ** 2.0 + (0.5 * params.width_total) ** 2.0)

def calculate_cross_section(params: Parameters, energy: float) -> float:
    wave_factor = 1.0/wavenumber_sq(params, energy)
    g = spin_factor(params)
    bw = breit_wigner(params, energy)
    return np.pi * wave_factor * g * bw

def calculate_cross_section_range(params: Parameters, energies: NDArray) -> NDArray:
    cs_array = np.zeros(len(energies))
    for index, e in enumerate(energies):
        cs_array[index] = calculate_cross_section(params, e)
    return cs_array

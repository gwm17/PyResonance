from PyResonance.config import read_config, get_reaction_equation_latex
from PyResonance.cross import calculate_cross_section_range
import PyResonance

import sys
import numpy as np
import matplotlib.pyplot as plt
import inspect
from pathlib import Path

def main(configfile: str, nucdatafile: Path):
    config = read_config(configfile, nucdatafile)
    if config is None or len(config.parameter_list) == 0:
        print("Config could not be parsed!")
        return
    
    energy_array = np.linspace(config.energy_min, config.energy_max, num=config.energy_npoints)
    resonances = [(get_reaction_equation_latex(params), calculate_cross_section_range(params, energy_array)) for params in config.parameter_list]
    fig, ax = plt.subplots(1, 1)
    total_cross_section = np.zeros(len(energy_array))
    for res in resonances:
        ax.scatter(energy_array, res[1], marker=".", linestyle="None", label=res[0])
        for idx, value in enumerate(res[1]):
            total_cross_section[idx] += value
    
    ax.scatter(energy_array, total_cross_section, marker=".", linestyle="None", label="Total Cross Section")
    ax.set_xlabel(r"$E_{CM}$ (MeV)")
    ax.set_ylabel(r"$\sigma$ (millibarn)")
    fig.legend()
    fig.tight_layout()

    plt.show()

main(sys.argv[1], Path(inspect.getfile(PyResonance)).parent / "data/mass.txt")


    
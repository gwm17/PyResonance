# PyResonance

PyResonance is a useful little tool for calculating resonance cross sections given a set of partial widths. Uses numpy and matplotlib.

## Use

Download the code and create a virtual environment using the requirements.txt file in the repository. Then can run as `python main.py config.json` (on some systems may need to use `python3` instead of python).
The json file is a configuration, with the energy range for the calculation (in the center of mass frame) and the reaction details. All energies and widths should be given in units of MeV. You can give PyResonance as many resonances to calculate as you want (the example in the repo has three different resonances). The default behavior is to calculate the cross section of all resonances over the given energy range and then make a plot containing each individual resonance as well as the total cross section. Currently it does not take into account any interference between resonances.

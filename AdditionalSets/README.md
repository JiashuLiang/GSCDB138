# Additional Test Sets

This directory contains supplementary test sets that are distributed separately from the core GSCDB benchmark. These data were used as development or post-development evaluation sets for the COACH functional and are provided to support transparent and reproducible testing beyond the main GSCDB benchmark.

## Included Sets

### `BigNC`

`L14` and `vL11` are two non-covalent interaction sets composed of large supramolecular complexes. They are intended to probe performance for sizable intermolecular interactions that are substantially more demanding than the typical systems represented in standard small-molecule benchmark collections.

### `GDB9-W1-F12`

`GDB9-W1-F12` is a broad atomization-energy test set derived from GDB9 molecules with high-level W1-F12 reference data. It provides a chemically diverse assessment of thermochemical performance across a wide range of small organic species.

### `3dCIPEA`

`3dCIPEA` contains 92 ionization-potential and electron-attachment-energy entries for first-row transition-metal atoms and complexes. The distributed inputs use def2-QZVPP.

### `H2X100`

`H2X100` contains 100 binding energies for sulfur-, selenium-, and tellurium-hydride clusters. References and stoichiometric coefficients are normalized per pairwise interaction. Monomer inputs use the full complex basis through Q-Chem ghost atoms for counterpoise correction.

### `ISOC7`

`ISOC7` contains 1,308 W1-F12 isomerization energies for C5--C7 hydrocarbons. The distributed inputs use def2-QZVPP.

### `TAE-PTComp`

`TAE-PTComp` contains 2,097 atom-scaled total atomization energies spanning 67 element-specific subsets. Both references and stoichiometric coefficients are divided by molecular atom count; def2-ECP is selected for species containing Rb or heavier elements.

### `TRIP50`

`TRIP50` contains 50 triplet-state reaction energies and 100 forward/reverse barrier heights. The distributed inputs use def2-QZVPP and preserve the charge and multiplicity of the original COACH calculations.

### `W1-SN2-BH`

`W1-SN2-BH` contains 1,881 W1w anionic S\(_\mathrm{N}\)2 barrier heights. Charges and multiplicities are taken from the source XYZ archive, and the distributed inputs use def2-TZVPPD.

### `atmospheric218`

`atmospheric218` contains 218 atmospheric-cluster binding energies reconstructed from the source study's CCSD(F12*)(T+)/cc-pVTZ-F12 total energies. The distributed inputs use def2-QZVPPD.

### `vL27`

`vL27` contains 27 large-complex binding energies based on converged local CCSD(T). Eleven systems overlap structurally with BigNC/vL11 but use newer 7/8 complete-PNO-space reference values. Monomer inputs use the full complex basis through Q-Chem ghost atoms for counterpoise correction.

### `OPT`

`W4-11-GEOM` and `SE` are two geometry optimization sets containing equilibrium molecular structures. It is intended to assess the quality of optimized geometries across a broad set of main-group molecules.

## File Organization

Each set is stored in its own subdirectory under `AdditionalSets/`. Depending on the set, the following files may be present:

- `qchem_inputs/`: Q-Chem input files used for the calculations.
- `DatasetEval.csv`: Tabulated reference values and reaction definitions, where applicable.
- `xyz_files/`: Derived XYZ geometries with compact metadata in the comment line.
- `Allmols_info.json`: Molecule metadata containing `molecule`, `charge`, `multiplicity`, and `basis`.

## References

```bibtex
@article{BigNC,
  title   = {Canonical coupled cluster binding benchmark for nanoscale noncovalent complexes at the hundred-atom scale},
  author  = {Lao, Ka Un},
  journal = {The Journal of Chemical Physics},
  year    = {2024},
  volume  = {161},
  number  = {23},
  pages   = {234103},
  doi     = {10.1063/5.0230456}
}

@article{GDB9_W1_F12,
  title={A highly diverse and accurate database of 3366 total atomization energies calculated at the CCSD(T)/CBS level by means of W1-F12 theory},
  author={Karton, Amir},
  journal={Chemical Physics Letters},
  volume={868},
  pages={142030},
  year={2025},
  publisher={Elsevier}
}

@article{W4_11_GEOM,
  title={Evaluation of density functional theory for a large and diverse set of organic and inorganic equilibrium structures},
  author={Karton, Amir and Spackman, Peter R},
  journal={Journal of Computational Chemistry},
  volume={42},
  number={22},
  pages={1590--1601},
  year={2021},
  publisher={Wiley Online Library}
}

@article{SE,
  title={Molecular structures with spectroscopic accuracy at DFT cost by the templating synthon approach and the PCS141 database},
  author={Lazzari, Federico and Di Grande, Silvia and Crisci, Luigi and Mendolicchio, Marco and Barone, Vincenzo},
  journal={The Journal of Chemical Physics},
  volume={162},
  number={11},
  year={2025},
  publisher={AIP Publishing}
}

@article{3dCIPEA,
  author={Galleni, Laura and Eversdijk, Stef and Escudero, Daniel and Jagau, Thomas-C. and van Setten, Michiel J. and Alessio, Maristella},
  title={Benchmarking the {GW} Approximation against Coupled-Cluster Theory for 3d Transition Metals},
  journal={Journal of Chemical Theory and Computation},
  volume={21},
  number={22},
  pages={11620--11631},
  year={2025},
  doi={10.1021/acs.jctc.5c01663}
}

@article{H2X100,
  author={Hoffman, Maxwell P. and Xantheas, Sotiris S.},
  title={{H2X100}: A Gold-Standard {CCSD(T)/CBS} Benchmark Dataset of Binding Energies, Structures, and Harmonic Frequencies for {(H2X)n}, {X = S, Se, Te}, {n = 2--4}, and Assessment of Lower-Scaling Density Functional Theory Methods},
  journal={Journal of Chemical Theory and Computation},
  volume={22},
  number={11},
  pages={5539--5554},
  year={2026},
  doi={10.1021/acs.jctc.6c00405}
}

@article{ISOC7,
  author={Karton, Amir and Semidalas, Emmanouil},
  title={Benchmarking Isomerization Energies for {C5--C7} Hydrocarbons: The {ISOC7} Database},
  journal={Journal of Computational Chemistry},
  volume={47},
  number={2},
  pages={e70296},
  year={2026},
  doi={10.1002/jcc.70296}
}

@misc{TAE_PTComp,
  author={Dahl, Robin and M{\"u}ller, Marcel and Kniebes, Vanessa and Werner, Hans-Joachim and Grimme, Stefan and Hansen, Andreas},
  title={An Element-Resolved Coupled Cluster Atomization Energy Data Set Ranging across the Periodic Table},
  year={2026},
  note={ChemRxiv preprint posted 10 July 2026},
  doi={10.26434/chemrxiv.15005940/v1}
}

@article{TRIP50,
  author={Hughes, William B. and Popescu, Mihai V. and Paton, Robert S.},
  title={Fundamental Study of Density Functional Theory Applied to Triplet State Reactivity: Introduction of the {TRIP50} Data Set},
  journal={Journal of Chemical Theory and Computation},
  volume={22},
  number={7},
  pages={3530--3542},
  year={2026},
  doi={10.1021/acs.jctc.6c00144}
}

@article{W1_SN2_BH,
  author={Karton, Amir},
  title={{W1-SN2-BH}: A Large-Scale {CCSD(T)/CBS} Kinetic Database},
  journal={The Journal of Physical Chemistry A},
  volume={130},
  number={14},
  pages={2929--2942},
  year={2026},
  doi={10.1021/acs.jpca.6c00424}
}

@article{atmospheric218,
  author={Knattrup, Yosef and Elm, Jonas},
  title={Extrapolating Local Coupled Cluster Calculations toward {CCSD(T)/CBS} Binding Energies of Atmospheric Molecular Clusters},
  journal={ACS Omega},
  volume={10},
  number={40},
  pages={46794--46808},
  year={2025},
  doi={10.1021/acsomega.5c04476}
}

@article{vL27,
  author={Lao, Ka Un},
  title={Benchmarking Nanoscale Noncovalent Complexes at the Two-Hundred-Atom Scale with Converged Local {CCSD(T)}},
  journal={The Journal of Physical Chemistry A},
  volume={130},
  number={22},
  pages={4136--4151},
  year={2026},
  doi={10.1021/acs.jpca.6c01097}
}
```

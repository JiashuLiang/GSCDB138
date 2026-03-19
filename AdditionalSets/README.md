# Additional Test Sets

This directory contains three supplementary test sets that are distributed separately from the core GSCDB benchmark. These data were used as external evaluation sets for the COACH functional and are provided to support transparent and reproducible testing beyond the main GSCDB benchmark.

## Included Sets

### `BigNC`

`L14` and `vL11` are two non-covalent interaction sets composed of large supramolecular complexes. They are intended to probe performance for sizable intermolecular interactions that are substantially more demanding than the typical systems represented in standard small-molecule benchmark collections.

### `GDB9-W1-F12`

`GDB9-W1-F12` is a broad atomization-energy test set derived from GDB9 molecules with high-level W1-F12 reference data. It provides a chemically diverse assessment of thermochemical performance across a wide range of small organic species.

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
```

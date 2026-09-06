# GSCDB: Gold-Standard Chemical Database

> **Note**: This is a developing branch. The standard errors might be not updated.
> 

GSCDB137 is a rigorously compiled benchmark database of 137 data sets (8377 entries) covering main-group and transition-metal reaction energies and barrier heights, non-covalent interactions, dipole moments, polarizabilities, electric-field response energies, and vibrational frequencies. Legacy data from GMTKN55 and MGCDB84 have been updated to today's best references; redundant, spin-contaminated, or low-quality points were removed, and many new, property-focused sets were added.

This comprehensive database provides a stringent platform for density functional approximation (DFA) validation and serves as a foundation for training the next generation of semi-empirical and machine-learned functionals. Testing across 29 popular density-functional approximations reveals the expected Jacob's-ladder hierarchy overall, yet shows key exceptions and provides insights into functional performance across diverse chemical properties.

## Changes in the Development Branch

1. `EA50_22` has been removed because this negative electron affinity is an artifact of basis-set incompleteness. The remaining subset has been renamed `EA49`, and `DatasetEval.csv` has been updated accordingly. `Datasets.csv` and the affected analysis results now reflect the 49-entry subset. The notebook reuses the published EA50 normalization baseline for EA49; `Standard_errors.csv` remains unchanged. The development evaluation contains 8,376 entries.


## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JiashuLiang/GSCDB.git
   cd GSCDB
   ```

2. **Run your calculations** using the provided input files

3. **Organize results** in `Molecule_Energies.csv` format

4. **Run analysis**:
   ```bash
   cd Analysis/
   jupyter notebook analyze.ipynb
   ```

## Molecule Data Formats

The database provides molecular geometries and calculation setups in three standardized formats to ensure compatibility with different quantum chemistry software packages:

### Available Formats

1. **Q-Chem input files** (`.in`)
   - Primary format used in the original calculations, ready for direct use in Q-Chem
   - All other formats are derived from these files and not validated

2. **JSON format** (`Allmols_info.json`)
   - Structured data containing geometry and calculation setup
   - **Necessary fields**: `charge`, `multiplicity`, `basis`, `multipole_field`, `molecule` (geometry, unit: Angstrom)
   - **Additional metadata**: `num_basis`, `num_pairs`, `xc_grid`, `SCF_ALGORITHM`, `mem_total`, `num_threads`, `AUX_BASIS_CORR` recommended for calculations

3. **XYZ format** (`.xyz`)
   - Standard geometry format with extended metadata (unit: Angstrom)
   - All information other than geometry is embedded in the comment line (line 2)

4. **ORCA Input Files**
   - Additional ORCA input files (converted from the primary Q-Chem inputs) are available upon request. Contact the primary author if needed.

### Important Notes

- **Electric field conventions**: Multipole fields use Q-Chem input format. Other software packages may have different sign conventions for electric fields.

- **Basis set**: 
  - The recommended basis sets can minimize basis set incompleteness errors
  - **Recommended basis sets by dataset**:
  
    | Data Set Name | Basis Set |
    |---------------|-----------|
    | G21IP, IP23, IP30, G21EA, EA50 | aug-pc-4 |
    | Dip146, HR46, Pol130, T144 | aug-pc-3 |
    | AE18 | aug-cc-pCV5Z |
    | RG10N, He3, excited He systems in O24x5 (O24_13, O24x4_49, O24x4_50, O24x4_51, O24x4_52) | d-aug-cc-pV5Z |
    | OEEF | aug-cc-pVQZ |
    | AE11 | Basis set from original paper (or see Q-Chem input files) |
    | BH876, MME52, MOBH28, TMD10, MOR13, TMB11, ROST61 | def2-QZVPP |
    | C60ISO7 | def2-TZVPD |
    | 3d4dIPSS | 3d: aug-cc-pwCVQZ; 4d: aug-cc-pwCVQZ-PP |
    | DAPD | aug-cc-pwCVQZ-PP for Pd; cc-pVQZ for H; aug-cc-pwCVQZ for other elements |
    | P34AE, P34EA, P34IP | aug-cc-pwCVQZ-PP for In, Sn, Sb, Te, I, Xe; def2-QZVPPD for all others |
    | All other datasets | def2-QZVPPD |
  
  - **Special cases requiring specific basis sets**: AE11 (custom basis from original authors), P34, DAPD, and 3d4dIPSS (mixed basis sets) may need manual work for setup.
  - **Easy-to-use replacements**: 
    - Small molecules: `def2-QZVPPD`
    - Larger molecules: `def2-TZVPP` or `def2-TZVPPD`
    - AE11 dataset: Must use original basis sets (available in paper supplementary materials or Q-Chem input files)
    - Excited Helium systems in O24 and O24x4 (O24_13, O24x4_49, O24x4_50, O24x4_51, O24x4_52): Use `d-aug-cc-pV5Z`. `def2-QZVPPD` is not recommended due to poor performance.
   
- **Numeric precision**: 
  - To ensure accuracy in energy differences, total energies may require up to 9 decimal places (in Hartree), particularly for the V30 dataset. It is recommended to use very tight SCF convergence thresholds and very dense integration grids to achieve this precision, especially when computing V30 properties.

## Analysis Workflow

We provide a comprehensive Jupyter notebook (`Analysis/analyze.ipynb`) for systematic evaluation of computational methods against the benchmark database. The analysis workflow processes molecular energies and converts them to the appropriate physical properties for comparison. The only input requirement is the `Molecule_Energies.csv` file, which should contain the results of your calculations (columns: different computational methods/functionals; rows: individual molecules from the database).

### Structured Database Files

Structured Excel files in the `Info/` directory provide comprehensive information about the database:

- **`DatasetEval.csv`**: Contains the complete definitions for all 8,377 energy differences, their reference values, and the dataset each entry belongs to; The weights used for calculating weighted errors in TMC34 and O24x5 datasets are also included in other sheets of this file
- **`Datasets.csv`**: Provides comprehensive information about each of the 137 datasets, including data source, system types, statistical summaries, and estimated accuracy
- **`Standard_errors.csv`**: Lists the reference uncertainties for each data point, enabling users to meaningfully compare results for newly tested functionals with the original publication
- **`FD_stepsize.csv`**: Documents the finite-difference step sizes used for the Pol130 and V30 datasets

These files enable users to easily access and utilize the benchmark data for custom analysis workflows.

## License
This database is openly licensed via CC BY 4.0.

## Citation

If you use this dataset in your research, please cite the following paper:

```bibtex
@article{liang2025gold,
   author = {Liang, Jiashu and Head-Gordon, Martin},
   title = {Gold-Standard Chemical Database 137 (GSCDB137): A Diverse Set of Accurate Energy Differences for Assessing and Developing Density Functionals},
   journal = {Journal of Chemical Theory and Computation},
   volume = {21},
   number = {24},
   pages = {12601-12621},
   year = {2025},
   doi = {10.1021/acs.jctc.5c01380},
   url={https://doi.org/10.1021/acs.jctc.5c01380}, 
}
```

## Contact

For questions, issues, or suggestions regarding the database:

- **Primary contact**: Jiashu Liang (jsliang@berkeley.edu)
- **Research group**: Martin Head-Gordon Group, UC Berkeley
- **Issues**: Please use the GitHub issue tracker for bug reports and feature requests
- **Contributions**: If you would like to contribute to validating or expanding the database or improving the analysis tools, please reach out!


## Acknowledgments

We thank the authors of MGCDB84, GMTKN55, and ACCDB for providing a solid foundation for this work. We are deeply grateful to Diptarka Hait for insightful discussions and valuable suggestions on refining the dipole moment and static polarizability data sets. We also thank Bun Chan for his generous guidance on the use of his benchmark sets and for providing so much highly accurate reference data. Our appreciation extends to Tarek Scheele and Tim Neudecker for clarifying details of the OEEF set. We also thank Klaas Giesbertz and Sebastian Ehlert for their suggestion on our preprint version of the database.

Most importantly, we thank all researchers who devote their time and effort to generating high-quality reference values, whether or not their work is included in this database. We fully recognize not only the substantial computational resources to complete high-level wavefunction calculations, as well as the human time required in the meticulous and often tedious process of evaluating the importance of each energy component and verifying the reliability of every data point. Such work can feel exhausting and thankless, lacking the allure of novelty, yet it is undeniably essential for progress. Without these efforts, we could neither rigorously assess the capabilities of current methods nor confidently guide the development of new ones. The creation of GSCDB137 thus also reflects the collective effort of a global community devoted to accuracy and reliability in computational chemistry; without their contributions, this database would simply not have been possible.


# GSCDB138: Gold-Standard Chemical Database

GSCDB138 is a rigorously compiled benchmark database of 138 data sets (8383 entries) covering main-group and transition-metal reaction energies and barrier heights, non-covalent interactions, dipole moments, polarizabilities, electric-field response energies, and vibrational frequencies. Legacy data from GMTKN55 and MGCDB84 have been updated to today's best references; redundant, spin-contaminated, or low-quality points were removed, and many new, property-focused sets were added.

This comprehensive database provides a stringent platform for density functional approximation (DFA) validation and serves as a foundation for training the next generation of semi-empirical and machine-learned functionals. Testing across 29 popular density-functional approximations reveals the expected Jacob's-ladder hierarchy overall, yet shows key exceptions and provides insights into functional performance across diverse chemical properties.

## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JiashuLiang/GSCDB138.git
   cd GSCDB138
   ```

2. **Run your calculations** using the provided input files

3. **Organize results** in `Molecule_Energies.xlsx` format

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
   - **Necessary fields**: `charge`, `multiplicity`, `basis`, `multipole_field`
   - **Additional metadata**: `num_basis`, `num_pairs`, `xc_grid`, `SCF_ALGORITHM`, `mem_total`, `num_threads`, `AUX_BASIS_CORR` recommended for calculations

3. **XYZ format** (`.xyz`)
   - Standard geometry format with extended metadata
   - All information other than geometry is embedded in the comment line (line 2)

### Important Notes

- **Electric field conventions**: Multipole fields use Q-Chem input format. Other software packages may have different sign conventions for electric fields.

- **Basis set**: 
  - The recommended basis sets can minimize basis set incompleteness errors
  - **Special cases requiring specific basis sets**: AE11 (custom basis from original authors), P34, DAPD, and 3d4dIPSS (mixed basis sets) may need manual work for setup.
  - **Easy-to-use replacements**: 
    - Small molecules: `def2-QZVPPD`
    - Larger molecules: `def2-TZVPP` or `def2-TZVPPD`
    - AE11 dataset: Must use original basis sets (available in paper supplementary materials or Q-Chem input files)

## Analysis Workflow

We provide a comprehensive Jupyter notebook (`Analysis/analyze.ipynb`) for systematic evaluation of computational methods against the benchmark database. The analysis workflow processes molecular energies and converts them to the appropriate physical properties for comparison. The only Input Requirements is the `Molecule_Energies.xlsx` file, which should contain the results of your calculations. (Columns: Different computational methods/functionals; Rows: Individual molecules from the database)

## License
This database is openly licensed via CC BY 4.0.

## Citation

If you use this dataset in your research, please cite the following paper:

```bibtex
@article{GSCDB138,
  title={Gold-Standard Chemical Database 138 (GSCDB138)},
  author={Jiashu Liang and Martin Head-Gordon},
  journal={arXiv preprint arXiv},
  year={2025}
}
```

## Contact

For questions, issues, or suggestions regarding the database:

- **Primary contact**: Jiashu Liang (jsliang@berkeley.edu)
- **Research group**: Martin Head-Gordon Group, UC Berkeley
- **Issues**: Please use the GitHub issue tracker for bug reports and feature requests
- **Contributions**: If you would like to contribute to validating or expanding the database or improving the analysis tools, please reach out!


## Acknowledgments

We thank the authors of MGCDB84, GMTKN55, and ACCDB for providing a solid foundation for this work. We are deeply grateful to Diptarka Hait for insightful discussions and valuable suggestions on refining the dipole moment and static polarizability data sets. We also thank Bun Chan for his generous guidance on the use of his benchmark sets and for providing so much highly accurate reference data. Our appreciation extends to Tarek Scheele and Tim Neudecker for clarifying details of the OEEF set.

Most importantly, we thank all researchers who devote their time and effort to generating high-quality reference values, whether or not their work is included in this database. We fully recognize not only the substantial computational resources to complete high-level wavefunction calculations, as well as the human time required in the meticulous and often tedious process of evaluating the importance of each energy component and verifying the reliability of every data point. Such work can feel exhausting and thankless, lacking the allure of novelty, yet it is undeniably essential for progress. Without these efforts, we could neither rigorously assess the capabilities of current methods nor confidently guide the development of new ones. The creation of GSCDB138 thus also reflects the collective effort of a global community devoted to accuracy and reliability in computational chemistry; without their contributions, this database would simply not have been possible.


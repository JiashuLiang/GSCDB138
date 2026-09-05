# C60ISO7 selection correction (#10)

Base: `f62f5d844d64b4ff451cbfc9320a39d830857099` (`main`).
Sources checked 2026-09-05: [issue #10](https://github.com/JiashuLiang/GSCDB/issues/10),
[paper](https://doi.org/10.1021/acs.jctc.5c01380),
[formal SI](https://ndownloader.figshare.com/files/60059371)
(Table S1, S-3; file MD5 `00bc3e43f4ccfbec17f3deabb3365ca1`).
The SI lists **structures** C60ISO_6 and C60ISO_8 (kOOMP2 S² 0.45364 and
1.00544). Reaction numbers differ from structure numbers:

| Reaction | Structures | Previous set | Correct set |
|---|---|---|---|
| C60ISO_4 | 1 → 5 | SC74 | C60ISO7 |
| C60ISO_5 | 1 → 6 | C60ISO7 | SC74 |
| C60ISO_7 | 1 → 8 | SC74 | SC74 |

Only two membership fields change. No reaction IDs, stoichiometries,
references, molecular energies, input files, or geometries change. Seven
reactions remain; structures 6 and 8 do not enter their stoichiometries.
The reference RMS changes from 105.8010478889 to **102.2220314898 kcal/mol**,
agreeing with Table 1 (102.22). `Info/Datasets.csv` is corrected; its count,
minimum and maximum remain valid. SC74 is excluded by the notebook.

## Analysis audit and update boundary

The unmodified notebook was executed cell-by-cell in a temporary copy using
Python 3.12, pandas 3.0.5, NumPy 2.5.2 and tqdm 4.70.0. All nine derived CSVs
retain their original dimensions and labels: 8377 reaction rows, 137 sets,
16 functional columns. Reaction energies agree to 7.46e-9 kcal/mol. One
unrelated finite-difference value (V30_91) differs by 6.43e-5 cm^-1, and
its aggregate MAE differs by 2.34e-7 cm^-1. This is consistent with numerical
sensitivity in converting a tiny energy difference to frequency, but the
original software environment is not recorded. Those unrelated rows are
preserved, rather than overwritten by the full rerun.

The maintenance script independently verifies the old C60ISO7 reaction
energies, MAE, MSE, RMSE, metric and normalized metric against the pinned
base (absolute tolerance 1e-8), and the existing overall aggregation
(tolerance 1e-9). It uses the notebook conversion factor 627.50947406 and
its unweighted C60ISO7 MAE/RMSE/MSE formulas. It updates the swapped reaction
in the three reaction/result tables, the C60ISO7 row in four error tables,
the C60ISO7 relative metric, and only its contribution to the overall and
Isomerization means. Unaffected rows retain their original text. The
functional ranking is unchanged. No quantum chemistry is rerun.

## Normalization limitation: published standards retained

The notebook reads `Info/Standard_errors.csv` as a fixed input. Its markdown
and paper §4.1 define standards as the mean of the second through fourth
lowest errors among the tested hybrid functionals. This file is an empirical
performance baseline, despite README wording suggesting reference uncertainty.
Its generation is not implemented in the notebook. The current energy table
contains 16 methods, versus 29 in the paper; dispersion variants in the paper
are not independently provided by this input table.

The existing C60ISO7 Metric/MAE standard is **1.97441912098719** and its RMSE
standard is **2.242918933970609**. Using the 14 available hybrids (excluding
the two double hybrids wB97M2 and revDSD-PBEP86-D4) instead yields
2.040066250301862 and 2.2112647179934686 for the **uncorrected** selection.
Thus rebuilding that baseline with the available panel is not reproducible.
No replacement standard is inferred. All official standards stay fixed and
the updated normalized/overall results use precisely the existing notebook
convention. A future rebaselining needs the original panel, dispersion
corrections and standard-generation provenance; it must be versioned and
must not be mixed silently into this membership fix. These updated scores
are explicitly comparisons to the retained published standard.

| Method | Old C60ISO7 MAE | New MAE | New overall NER |
|---|---:|---:|---:|
| wB97M2 | 2.1552149053 | 2.6584661187 | 0.9503929647 |
| wB97M-V | 11.3561818807 | 10.4130441594 | 1.0720517974 |
| CF22D | 4.2699738264 | 4.4970922747 | 1.2500967439 |

## Reproduction

From the repository root, with pandas and NumPy installed:

```sh
python3 Analysis/maintenance/fix_c60iso7.py          # verify corrected files
python3 Analysis/maintenance/fix_c60iso7.py --apply  # recreate from pinned base
```

The script computes and checks everything before writing. A dry run must
pass before committing. To repeat the full notebook audit, copy `Info/`
and `Analysis/` to a temporary directory, execute each code cell in sequence
with the temporary `Analysis/` as the working directory, and compare against
the pinned base by row/column label. Never run this full audit over the
production CSVs merely to refresh unrelated numerical formatting.

# Pd spin-gap investigation and locally selected reference (#9)

Base: `f62f5d844d64b4ff451cbfc9320a39d830857099` (`main`).
This branch is **local only**: no push or PR. It contains no C60ISO7 fix.

On 2026-09-05 the maintainer explicitly instructed: “Standard error 不要更新”
and “Pd 那个，就用21.85−0.46=21.39 kcal/mol”. Accordingly this local patch adopts
**21.39 kcal/mol = 0.034087134751299 Hartree** for `3d4dIPSS_35`, with the
repository conversion factor 627.50947406. This is a maintainer-selected
composite-minus-DKH–PP estimate, not a number directly tabulated as a final
PP reference. The unresolved provenance questions below remain visible.
`Info/Standard_errors.csv` is unchanged in every respect.

## Confirmed facts and origin audit

- `3d4dIPSS_35` is E(Pd_ES) − E(Pd_GS), originally 0.115886697 Hartree =
  72.72000028502 kcal/mol. No ID, membership, stoichiometry, molecular energy,
  input or geometry is changed. Its set retains 32 reactions.
- [GSCDB §3](https://pmc.ncbi.nlm.nih.gov/articles/PMC12746454/) specifies
  the lowest state per multiplicity, theoretical references first, and
  DKH-adjusted experiments when theory is unavailable. The intended gap is
  4d¹⁰ ¹S → 4d⁹5s ³D, not 4d⁸5s² ³F. The assignments are independently
  tabulated in [2025 SI Table S7](https://ndownloader.figshare.com/files/58130015).
- Git history locates the exact old value in the **first public release**,
  `4da0f73cb`, `Info/DatasetEval.xlsx`, sheet1. It survives the spreadsheet
  conversion (`474f97a81`) unchanged. No per-entry provenance or raw
  wavefunction reference calculation was found in the tracked history.
- [Figgen, Peterson and Stoll (2008)](https://doi.org/10.1063/1.2822992)
  studies 5s²/5s⁰ excitation energies, 4s4p correlation and DKH comparisons
  including 3d correlation. Its abstract supports the configuration-mismatch
  hypothesis, but **the exact source of 72.72 remains unverified**. Publisher
  PDF access returned HTTP 403, the DOI-filtered OSTI API returned no records,
  and the WSU institutional record exposed the abstract only. Neither the
  modern ³F AWQZ value (72.18) nor its composite value (76.43) equals 72.72;
  proximity is not evidence of a particular table or correction.
- [Issue #9](https://github.com/JiashuLiang/GSCDB/issues/9) reports
  CCSD(T)/aug-cc-pwCVQZ-PP = 0.032413365 Hartree = 20.3396936237 kcal/mol.
  This is a reporter-supplied finite-basis result; no raw output was supplied.
- [ACCDB source notes](https://github.com/peverati/ACCDB/blob/master/Databases/MetalsEE/4d-SSIP24/README.md)
  trace 0.029911874 Hartree = 18.7699843219 kcal/mol to Luo and Truhlar (2012),
  DOI 10.1021/ct300737t, using Moore experimental levels with spin–orbit
  coupling removed. Its scalar-relativistic correction is not documented
  there. There is also a **sign/label inconsistency**: its row 15 uses −HS+LS
  with a positive reference, while the current HS and LS geometry headers
  specify triplet and singlet, respectively. The positive magnitude cannot
  simply be transplanted with that reaction definition.

## ECP, correlation space, and correction meaning

Both repository Pd inputs have charge zero and multiplicities 1 (GS) and
3 (ES), `BASIS GEN`, `ECP GEN`, and `N_FROZEN_CORE FC`. Their full Pd ECP
blocks have 28 core electrons. All **13 radial terms in five angular channels**
were numerically matched for both inputs to the
[Basis Set Exchange aug-cc-pwCVQZ-PP definition, version 0, element 46](https://www.basissetexchange.org/api/basis/aug-cc-pwcvqz-pp/format/json/?elements=46).
BSE identifies a scalar Stuttgart–Koeln MCDHF RSC ECP, citing Peterson et al.
(2007). This leaves 18 electrons explicit, including 4s and 4p; the presence
of these electrons does not by itself establish which were correlated in
an external coupled-cluster calculation. `FC` alone, without the actual
output, is not a per-orbital correlation-space record.

[The 2025 main text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12498498/)
describes spin-free s-ccCA energies, an ROHF reference, high-order coupled
cluster increments through CCSDTQP, and core–valence corrections. It describes
the 4d DKH–PP term as a correction to a PP treatment that already includes
scalar relativity. Thus subtracting 0.46 here removes this **residual DKH–PP
increment**, not the whole scalar relativistic effect and not a spin–orbit
correction. The detailed composite implementation is referred to
DOI 10.1080/00268976.2021.1963001 (and the late-metal extension
10.1016/j.cplett.2024.141423). Exact orbital partitions, the DKH Hamiltonian
order and correspondence to the repository ECP for every increment have
not been established from raw inputs. This limits the claim of matched
Hamiltonians, even though the local value is now explicitly selected.

Table S13, Pd ¹S→³D column (kcal/mol):

| Contribution | Value |
|---|---:|
| CCSD(T), AWQZ | 20.32 |
| CCSD(T), AW5Z | 20.96 |
| CCSD(T), CBS | 21.85 |
| DKH–PP | +0.46 |
| CCSDT increment, CBS | −0.64 |
| Quadruples, TZ | +0.10 |
| Quintuples, DZ | −0.02 |
| Core–valence increment, TZ | +0.11 |
| Final s-ccCA excitation | 21.85 |

The CCSD(T)/CBS and final s-ccCA values happen to round to the same number;
they are distinct quantities. Summing the rounded components gives 21.86,
a 0.01 rounding inconsistency relative to the tabulated final result.
The selected 21.39 uses the **tabulated final** 21.85 minus 0.46; it retains
the net high-order/core–valence terms. It is neither the finite-basis QZ
result nor a bare CCSD(T)/CBS value. Do not assign more source precision
than these two-decimal inputs. The long Hartree representation preserves
unit conversion only.

## Local update and sensitivity analysis

`apply_pd_reference.py` changes only the reference row, the set reference
RMS, affected error rows, and the contribution of this set to the overall
and Transition Metal summaries. The three reaction/result tables carry the
new reference; their calculated energy columns remain unchanged. The set
reference RMS changes **138.9673690705 → 138.4231604292 kcal/mol**; its count,
minimum and maximum do not change. Overall functional ranking is unchanged.

The sensitivity script reads the **pinned original base**, independently
recomputes all 32 × 16 predictions from molecular energies, and checks
stored energies/errors/MAE/MSE/RMSE/NER within 1e-8. It writes only the
investigation CSVs. `sensitivity.csv` reports seven reference scenarios,
per-method gap/error, set MAE/MSE/RMSE, set NER, TM/overall means and ranks.
`normalization.csv` reports reference RMS and normalization sensitivity.
All predicted gaps are retained, even those below zero (range −6.4554 to
28.5188 kcal/mol); no claim of verified term identity is made for these SCF
solutions. No new electronic-structure calculations were performed.

The published Metric/MAE standard **5.193466247976917** (RMSE
**9.957303213535852**) remains fixed. Unlike C60ISO7, these particular old
Pd-set standards can be reproduced from the available 14 hybrids, excluding
the two double hybrids. If one hypothetically rebuilt the standard at 21.39,
it would become 3.77798534525 (MAE) and 4.78891675767 (RMSE). These values
appear **only as sensitivity results**; no official standard is updated.
The overall averages give each of 137 sets equal weight; the TM average
uses nine sets in this pinned checkout.

| Method | Old set MAE | New set MAE | New overall NER, fixed standard |
|---|---:|---:|---:|
| wB97M2 | 5.771957 | 4.250745 | 0.946394 |
| wB97M-V | 5.105711 | 3.713733 | 1.073582 |
| CF22D | 4.939023 | 3.409221 | 1.247107 |

## Reproduction and remaining evidence

```sh
python3 Analysis/investigations/pd_sensitivity.py --output docs/issue-9
python3 Analysis/investigations/apply_pd_reference.py --apply
python3 Analysis/investigations/apply_pd_reference.py
```

Requires Python 3, pandas and NumPy. The scripts were run with Python 3.12,
pandas 3.0.5 and NumPy 2.5.2. `provenance.json` fingerprints the pinned input
CSVs; `sources.json` records retrieval URLs, date and downloaded-byte hashes.
Production input/output row changes are verified independently of the
sensitivity CSV serialization.

Before a future release, resolve the exact original 72.72 provenance,
external ECP/correlation-space alignment and the DKH–PP definition at the
input level, ACCDB's sign/correction conventions, and the actual converged
Pd orbital states for each functional. The maintainer's numerical selection
does not establish these missing facts. This local branch keeps them explicit
and is not published.

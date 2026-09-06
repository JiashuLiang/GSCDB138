"""Issue #9: sensitivity only; never writes Info/ or official analysis tables.

Run from any directory with Python 3, pandas and numpy. Output goes only to
an explicitly chosen directory (outside Info/ and Analysis/).
"""
import argparse
import hashlib
import io
import subprocess
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
BASE = 'f62f5d844d64b4ff451cbfc9320a39d830857099'
KCAL = 627.50947406
TARGET = '3d4dIPSS_35'
SET = '3d4dIPSS'


def original(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)


def read(path):
    return pd.read_csv(io.BytesIO(original(path)), index_col=0)


def metrics(e):
    return {'MAE': e.abs().mean(), 'MSE': e.mean(), 'RMSE': np.sqrt((e**2).mean())}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    out = args.output.resolve()
    for protected in [ROOT/'Info',ROOT/'Analysis']:
        if out == protected or protected in out.parents:
            p.error('Choose an output directory outside Info/ and Analysis/.')
    definitions = read('Info/DatasetEval.csv')
    assert definitions.loc[TARGET,'Stoichiometry'] == '1,3d4dIPSS_Pd_ES,-1,3d4dIPSS_Pd_GS'
    assert definitions.loc[TARGET,'Reference'] == 0.115886697, 'Expected untouched issue #9 base'
    selected = definitions[definitions.Dataset == SET]
    assert len(selected) == 32
    energy = read('Analysis/Molecule_Energies.csv')
    funcs = energy.columns.tolist()
    hybrids = [f for f in funcs if f not in ['wB97M2','revDSD-PBEP86-D4']]
    predictions = pd.DataFrame(index=selected.index,columns=funcs,dtype=float)
    for idx,row in selected.iterrows():
        terms = row.Stoichiometry.split(',')
        predictions.loc[idx] = sum(float(c)*energy.loc[s] for c,s in zip(terms[::2],terms[1::2]))*KCAL
    assert np.isfinite(predictions.to_numpy()).all()
    refs = selected.Reference*KCAL
    olderrors = predictions.sub(refs,axis=0)
    oldmetrics = metrics(olderrors)
    np.testing.assert_allclose(predictions,read('Analysis/Reaction_Energies.csv').loc[selected.index,funcs],rtol=0,atol=1e-8)
    np.testing.assert_allclose(olderrors,read('Analysis/Results_errors.csv').loc[selected.index,funcs],rtol=0,atol=1e-8)
    for name,v in oldmetrics.items():
        np.testing.assert_allclose(v,read(f'Analysis/Errors_per_set_{name}.csv').loc[SET,funcs].astype(float),rtol=0,atol=1e-8)
    standards = read('Info/Standard_errors.csv')
    frozen = standards.loc[SET,'Metric']
    relative = read('Analysis/Relative_metric_per_set.csv')
    oldrelative = relative.loc[SET,funcs].astype(float)
    np.testing.assert_allclose(oldmetrics['MAE']/frozen,oldrelative,rtol=0,atol=1e-8)
    summary = read('Analysis/Statistical_errors.csv')
    nsets = len(relative)
    ntm = sum(relative.Datatype == 'Transition Metal')
    assert nsets == 137
    scenarios = {
        'current_official': (0.115886697*KCAL,'Unchanged production reference'),
        'issue_QZ': (0.032413365*KCAL,'Reporter finite-basis CCSD(T); not approved'),
        'ACCDB_experiment': (0.029911874*KCAL,'SOC-removed experiment; convention unresolved'),
        'SI_AWQZ': (20.32,'SI finite-basis component; not a final reference'),
        'SI_AW5Z': (20.96,'SI finite-basis component; not a final reference'),
        'PP_composite_inference': (21.39,'21.85 minus DKH-PP 0.46; selected by maintainer on 2026-09-05; source alignment still provisional'),
        'SI_CBS_or_sccCA': (21.85,'Same rounded number for distinct CBS and full composite quantities'),
    }
    rows, panelrows = [], []
    gaps = predictions.loc[TARGET]
    baseline_panel = oldmetrics['MAE'][hybrids].sort_values().iloc[1:4].mean()
    baseline_panel_mean = summary.loc['Mean',funcs] + (oldmetrics['MAE']/baseline_panel-oldrelative)/nsets
    for label,(reference,note) in scenarios.items():
        newrefs = refs.copy(); newrefs.loc[TARGET] = reference
        errors = predictions.sub(newrefs,axis=0)
        m = metrics(errors)
        panel = m['MAE'][hybrids].sort_values()
        panelstandard = panel.iloc[1:4].mean()
        panelrmse = m['RMSE'][hybrids].sort_values().iloc[1:4].mean()
        ner = m['MAE']/frozen
        nerpanel = m['MAE']/panelstandard
        overall = summary.loc['Mean',funcs] + (ner-oldrelative)/nsets
        tm = summary.loc['Mean Transition Metal',funcs] + (ner-oldrelative)/ntm
        overallpanel = summary.loc['Mean',funcs] + (nerpanel-oldrelative)/nsets
        tmpanel = summary.loc['Mean Transition Metal',funcs] + (nerpanel-oldrelative)/ntm
        rank = overall.rank(method='min')
        rankpanel = overallpanel.rank(method='min')
        panelrows.append(dict(scenario=label,reference_kcal=reference,reference_hartree=reference/KCAL,
            reference_RMS_kcal=np.sqrt(np.mean(newrefs**2)),published_metric_standard=frozen,
            exploratory_panel_metric_standard=panelstandard,
            published_RMSE_standard=standards.loc[SET,'RMSE'],exploratory_panel_RMSE_standard=panelrmse,
            panel_second_to_fourth=';'.join(panel.index[1:4]),status=note))
        for f in funcs:
            rows.append(dict(scenario=label,functional=f,predicted_Pd_gap_kcal=gaps[f],
                Pd_signed_error_kcal=gaps[f]-reference,set_MAE=m['MAE'][f],set_MSE=m['MSE'][f],
                set_RMSE=m['RMSE'][f],delta_set_MAE=m['MAE'][f]-oldmetrics['MAE'][f],
                NER_frozen=ner[f],overall_NER_frozen=overall[f],TM_NER_frozen=tm[f],
                delta_overall_NER_frozen=overall[f]-summary.loc['Mean',f],overall_rank_frozen=int(rank[f]),
                NER_exploratory_panel=nerpanel[f],overall_NER_exploratory_panel=overallpanel[f],
                TM_NER_exploratory_panel=tmpanel[f],overall_rank_exploratory_panel=int(rankpanel[f]),
                delta_overall_NER_vs_current_exploratory_panel=overallpanel[f]-baseline_panel_mean[f]))
    provenance = {
        'status':'Sensitivity analysis of pinned original base; 21.39 kcal/mol selected separately by maintainer',
        'base':'f62f5d844d64b4ff451cbfc9320a39d830857099',
        'hartree_to_kcal_mol':KCAL,'sets':nsets,'TM_sets':int(ntm),'set_reactions':len(selected),
        'hybrids_available':hybrids,'excluded_double_hybrids':['wB97M2','revDSD-PBEP86-D4'],
        'normalization':'Frozen published standard plus explicitly exploratory available-panel rebaselining',
        'validated':'All 32 reactions x 16 functionals and stored MAE/MSE/RMSE/NER; absolute tolerance 1e-8',
        'input_sha256':{str(f.relative_to(ROOT)):hashlib.sha256(original(str(f.relative_to(ROOT)))).hexdigest()
                        for folder in ['Info','Analysis'] for f in sorted((ROOT/folder).glob('*.csv'))},
    }
    out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(out/'sensitivity.csv',index=False,float_format='%.12g')
    pd.DataFrame(panelrows).to_csv(out/'normalization.csv',index=False,float_format='%.12g')
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    print('Validated baseline; wrote sensitivity only to',out)
    print(pd.DataFrame(panelrows)[['scenario','reference_kcal','reference_RMS_kcal','exploratory_panel_metric_standard']].to_string(index=False))
    print('Existing Pd gaps range:',gaps.min(),gaps.max(),'kcal/mol')


if __name__ == '__main__':
    main()

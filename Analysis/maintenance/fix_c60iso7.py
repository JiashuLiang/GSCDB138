"""Reproduce issue #10 from its pinned base; only --apply writes production files.

Run with Python 3 + pandas/numpy. Existing normalization standards are frozen:
the published hybrid-panel standards cannot be reconstructed from this checkout.
"""
import argparse
import io
from pathlib import Path
import subprocess

import numpy as np
import pandas as pd

BASE = 'f62f5d844d64b4ff451cbfc9320a39d830857099'
ROOT = Path(__file__).resolve().parents[2]
KCAL = 627.50947406


def original(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT).decode()


def frame(path):
    return pd.read_csv(io.StringIO(original(path)), index_col=0)


def replace_rows(path, replacements, remove=()):
    # Keep all unrelated rows byte-for-byte (Git's LF representation).
    lines = original(path).splitlines(keepends=True)
    seen = set()
    out = [lines[0]]
    for line in lines[1:]:
        key = line.split(',', 1)[0]
        if key in remove:
            continue
        if key in replacements:
            out.append(replacements[key]); seen.add(key)
        else:
            out.append(line)
    out.extend(v for k, v in replacements.items() if k not in seen)
    return ''.join(out)


def serialized(df, keys):
    return {k: df.loc[[k]].to_csv(header=False, lineterminator='\n') for k in keys}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    definitions = frame('Info/DatasetEval.csv')
    old = definitions[definitions.Dataset == 'C60ISO7']
    assert len(old) == 7
    for reaction, structure, dataset in [('C60ISO_4',5,'SC74'),('C60ISO_5',6,'C60ISO7'),('C60ISO_7',8,'SC74')]:
        assert definitions.loc[reaction,'Stoichiometry'] == f'-1,C60ISO_1,1,C60ISO_{structure}'
        assert definitions.loc[reaction,'Dataset'] == dataset
    definitions.loc['C60ISO_4','Dataset'] = 'C60ISO7'
    definitions.loc['C60ISO_5','Dataset'] = 'SC74'
    selected = definitions[definitions.Dataset == 'C60ISO7']
    assert len(selected) == 7
    species = {s for v in selected.Stoichiometry for s in v.split(',')[1::2]}
    assert not species.intersection({'C60ISO_6','C60ISO_8'})
    rms = np.sqrt(np.mean((selected.Reference*KCAL)**2))
    assert abs(rms-102.2220315) < 1e-7
    energies = frame('Analysis/Molecule_Energies.csv')
    funcs = energies.columns.tolist()

    def calculate(rows):
        values = pd.DataFrame(index=rows.index, columns=funcs, dtype=float)
        for idx, row in rows.iterrows():
            terms = row.Stoichiometry.split(',')
            values.loc[idx] = sum(float(c)*energies.loc[s] for c,s in zip(terms[::2],terms[1::2]))*KCAL
        assert np.isfinite(values.to_numpy()).all()
        return values

    oldvalues, values = calculate(old), calculate(selected)
    stored = frame('Analysis/Reaction_Energies.csv')
    np.testing.assert_allclose(oldvalues, stored.loc[old.index,funcs], rtol=0, atol=1e-8)
    errors = values.sub(selected.Reference*KCAL,axis=0)
    olderrors = oldvalues.sub(old.Reference*KCAL,axis=0)
    updates = {}
    updates['Info/DatasetEval.csv'] = replace_rows('Info/DatasetEval.csv',serialized(definitions,['C60ISO_4','C60ISO_5']))
    info = frame('Info/Datasets.csv')
    info.loc['C60ISO7','RMS energy(kcal/mol)'] = rms
    assert info.loc['C60ISO7','#datapoints'] == 7
    np.testing.assert_allclose([info.loc['C60ISO7','min'],info.loc['C60ISO7','max']], [selected.Reference.min()*KCAL,selected.Reference.max()*KCAL],atol=1e-9)
    updates['Info/Datasets.csv'] = replace_rows('Info/Datasets.csv',serialized(info,['C60ISO7']))
    # Existing retained reaction rows do not change, only the swapped row does.
    for name in ['Reaction_Energies','Results_values','Results_errors']:
        path = f'Analysis/{name}.csv'
        df = frame(path)
        row = pd.DataFrame(index=['C60ISO_4'],columns=df.columns)
        row.loc['C60ISO_4','Dataset'] = 'C60ISO7'
        row.loc['C60ISO_4','Reference'] = selected.loc['C60ISO_4','Reference']*KCAL
        row.loc['C60ISO_4',funcs] = (errors if name=='Results_errors' else values).loc['C60ISO_4']
        updates[path] = replace_rows(path,serialized(row,['C60ISO_4']),remove=['C60ISO_5'])
    reducers = {'MAE':lambda e:e.abs().mean(), 'Metric':lambda e:e.abs().mean(), 'RMSE':lambda e:np.sqrt((e**2).mean()), 'MSE':lambda e:e.mean()}
    for metric, reduce in reducers.items():
        path = f'Analysis/Errors_per_set_{metric}.csv'
        df = frame(path)
        np.testing.assert_allclose(reduce(olderrors),df.loc['C60ISO7',funcs].astype(float),rtol=0,atol=1e-8)
        df.loc['C60ISO7',funcs] = reduce(errors)
        updates[path] = replace_rows(path,serialized(df,['C60ISO7']))
    standards = frame('Info/Standard_errors.csv')
    relative = frame('Analysis/Relative_metric_per_set.csv')
    np.testing.assert_allclose(olderrors.abs().mean()/standards.loc['C60ISO7','Metric'],relative.loc['C60ISO7',funcs].astype(float),rtol=0,atol=1e-8)
    summary = frame('Analysis/Statistical_errors.csv')
    np.testing.assert_allclose(relative[funcs].mean(),summary.loc['Mean',funcs],rtol=0,atol=1e-9)
    previous_relative = relative.loc['C60ISO7',funcs].astype(float).copy()
    relative.loc['C60ISO7',funcs] = errors.abs().mean()/standards.loc['C60ISO7','Metric']
    delta = relative.loc['C60ISO7',funcs].astype(float) - previous_relative
    updates['Analysis/Relative_metric_per_set.csv'] = replace_rows('Analysis/Relative_metric_per_set.csv',serialized(relative,['C60ISO7']))
    summary.loc['Mean',funcs] += delta / len(relative)
    summary.loc['Mean Isomerization',funcs] += delta / sum(relative.Datatype=='Isomerization')
    assert summary.columns.tolist() == summary.loc['Mean'].sort_values().index.tolist(), 'Ranking changed; explicitly reorder columns before publishing'
    updates['Analysis/Statistical_errors.csv'] = replace_rows('Analysis/Statistical_errors.csv',serialized(summary,['Mean','Mean Isomerization']))
    print(f'Reactions: 7; reference RMS: {np.sqrt(np.mean((old.Reference*KCAL)**2)):.10f} -> {rms:.10f} kcal/mol')
    print('Frozen normalization Metric:',standards.loc['C60ISO7','Metric'])
    for func in ['wB97M2','wB97M-V','CF22D']:
        print(func,'MAE',olderrors[func].abs().mean(),'->',errors[func].abs().mean(),'overall NER',summary.loc['Mean',func])
    for path, content in updates.items():
        if args.apply:
            (ROOT/path).write_text(content)
        else:
            assert (ROOT/path).read_text() == content, f'{path}: differs from expected correction (use --apply)'
    print('Validated',len(updates),'files; normalization, molecules, geometry, IDs and references preserved.')


if __name__ == '__main__':
    main()

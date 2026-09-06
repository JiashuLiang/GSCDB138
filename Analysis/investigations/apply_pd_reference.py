"""Reproduce the maintainer-selected 21.39 kcal/mol Pd reference on issue #9.

Default: verify corrected files. --apply: recreate affected rows from the pinned
base. Standard_errors.csv is always preserved. No quantum chemistry is run.
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
TARGET = '3d4dIPSS_35'
SET = '3d4dIPSS'
REFERENCE = float(f'{21.39/KCAL:.15f}')


def original(path):
    return subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT).decode()


def read(path):
    return pd.read_csv(io.StringIO(original(path)),index_col=0)


def patch(path, df, keys):
    rows = {key:df.loc[[key]].to_csv(header=False,lineterminator='\n') for key in keys}
    lines = original(path).splitlines(keepends=True)
    return lines[0]+''.join(rows.get(line.split(',',1)[0],line) for line in lines[1:])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--apply',action='store_true')
    args=p.parse_args()
    definitions=read('Info/DatasetEval.csv')
    before=definitions.copy()
    assert definitions.loc[TARGET,'Reference']==0.115886697
    assert definitions.loc[TARGET,'Stoichiometry']=='1,3d4dIPSS_Pd_ES,-1,3d4dIPSS_Pd_GS'
    definitions.loc[TARGET,'Reference']=REFERENCE
    pd.testing.assert_frame_equal(definitions.drop(columns='Reference'),before.drop(columns='Reference'))
    selected=definitions[definitions.Dataset==SET]
    assert len(selected)==32
    updates={'Info/DatasetEval.csv':patch('Info/DatasetEval.csv',definitions,[TARGET])}
    info=read('Info/Datasets.csv')
    rms=np.sqrt(np.mean((selected.Reference*KCAL)**2))
    info.loc[SET,'RMS energy(kcal/mol)']=rms
    np.testing.assert_allclose([info.loc[SET,'min'],info.loc[SET,'max']],
                               [selected.Reference.min()*KCAL,selected.Reference.max()*KCAL],atol=1e-9)
    updates['Info/Datasets.csv']=patch('Info/Datasets.csv',info,[SET])
    energy=read('Analysis/Molecule_Energies.csv')
    funcs=energy.columns.tolist()
    predictions=(energy.loc['3d4dIPSS_Pd_ES']-energy.loc['3d4dIPSS_Pd_GS'])*KCAL
    np.testing.assert_allclose(predictions,read('Analysis/Reaction_Energies.csv').loc[TARGET,funcs].astype(float),rtol=0,atol=1e-8)
    for name in ['Reaction_Energies','Results_values','Results_errors']:
        path=f'Analysis/{name}.csv';df=read(path)
        df.loc[TARGET,'Reference']=REFERENCE*KCAL
        if name=='Results_errors':df.loc[TARGET,funcs]=predictions-REFERENCE*KCAL
        updates[path]=patch(path,df,[TARGET])
    olderrors=read('Analysis/Results_errors.csv')
    olderrors=olderrors.loc[olderrors.Dataset==SET,funcs]
    errors=olderrors.copy();errors.loc[TARGET]=predictions-REFERENCE*KCAL
    reducers={'MAE':lambda e:e.abs().mean(),'Metric':lambda e:e.abs().mean(),
              'RMSE':lambda e:np.sqrt((e**2).mean()),'MSE':lambda e:e.mean()}
    for metric,reduce in reducers.items():
        path=f'Analysis/Errors_per_set_{metric}.csv';df=read(path)
        np.testing.assert_allclose(reduce(olderrors),df.loc[SET,funcs].astype(float),rtol=0,atol=1e-8)
        df.loc[SET,funcs]=reduce(errors)
        updates[path]=patch(path,df,[SET])
    standards=read('Info/Standard_errors.csv')
    relative=read('Analysis/Relative_metric_per_set.csv')
    previous=relative.loc[SET,funcs].astype(float).copy()
    relative.loc[SET,funcs]=errors.abs().mean()/standards.loc[SET,'Metric']
    delta=relative.loc[SET,funcs].astype(float)-previous
    updates['Analysis/Relative_metric_per_set.csv']=patch('Analysis/Relative_metric_per_set.csv',relative,[SET])
    summary=read('Analysis/Statistical_errors.csv')
    summary.loc['Mean',funcs]+=delta/len(relative)
    summary.loc['Mean Transition Metal',funcs]+=delta/sum(relative.Datatype=='Transition Metal')
    assert summary.columns.tolist()==summary.loc['Mean'].sort_values().index.tolist(), 'Explicit ranking update required'
    updates['Analysis/Statistical_errors.csv']=patch('Analysis/Statistical_errors.csv',summary,['Mean','Mean Transition Metal'])
    assert (ROOT/'Info/Standard_errors.csv').read_text()==original('Info/Standard_errors.csv')
    assert abs(REFERENCE*KCAL-21.39)<1e-10
    for path,content in updates.items():
        if args.apply:(ROOT/path).write_text(content)
        else:assert (ROOT/path).read_text()==content,path
    print(f'Pd reference: {REFERENCE:.15f} Hartree = {REFERENCE*KCAL:.12f} kcal/mol')
    print('32 reactions; RMS reference:',rms,'; frozen standard:',standards.loc[SET,'Metric'])
    print('Verified',len(updates),'affected files; no standard, molecular-energy, geometry, ID or stoichiometry change.')


if __name__=='__main__':
    main()

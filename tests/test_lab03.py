import numpy as np
import pytest
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from inf8239_u01.lab03 import approved_split, configurations, pareto_mask


def test_split_matches_exercise_01():
    bunch=load_breast_cancer(as_frame=True)
    expected=train_test_split(bunch.data,bunch.target,test_size=.2,stratify=bunch.target,random_state=42)
    actual=approved_split()
    assert all(a.equals(b) for a,b in zip(actual,expected))
    assert set(actual[0].index).isdisjoint(actual[1].index)


def test_pareto_dominance_ties_and_tradeoffs():
    values=[[1,1],[2,2],[1,1],[.5,3],[3,.5]]
    assert pareto_mask(values).tolist()==[True,False,True,True,True]


def test_pareto_rejects_missing_measurements():
    with pytest.raises(ValueError):
        pareto_mask([[1,np.nan]])


def test_pca_scaler_learns_only_training_rows():
    Xtr,Xte,ytr,_=approved_split()
    model=configurations()['PCA + SVM'].fit(Xtr,ytr)
    np.testing.assert_allclose(model.named_steps['scale'].mean_,Xtr.mean())
    assert model.named_steps['scale'].n_samples_seen_==455
    assert model.named_steps['pca'].n_components_<30
    assert len(model.predict(Xte))==114

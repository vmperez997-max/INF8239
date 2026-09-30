import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from inf8239_u02.corpus import ROOT, normalized
from inf8239_u02.text_model import pipelines

def test_all_models_keep_vectorizer_in_pipeline():
    for model in pipelines().values():
        assert list(model.named_steps)==['tfidf','model']
        assert isinstance(model.named_steps['tfidf'],TfidfVectorizer)

def test_saved_model_predicts_one_label_per_text():
    model=joblib.load(ROOT/'models/text_model.joblib')
    pred=model.predict(['Good service and food.','Terrible product, waste of money.'])
    assert len(pred)==2 and set(pred)<={0,1}

def test_split_has_no_text_overlap():
    frame=pd.read_csv(ROOT/'data/processed/dataset.csv')
    split=pd.read_csv(ROOT/'reports/text_split.csv')
    tr=set(frame.iloc[split.loc[split.split=='train','row']].text.map(normalized))
    te=set(frame.iloc[split.loc[split.split=='test','row']].text.map(normalized))
    assert tr.isdisjoint(te)

def test_vectorizer_has_not_seen_test_only_token():
    model=pipelines()['LogisticRegression']
    model.fit(['great good product','nice good service','awful bad product','terrible bad service'],[1,1,0,0])
    model.predict(['unseenholdouttoken'])
    assert 'unseenholdouttoken' not in model.named_steps['tfidf'].vocabulary_

def test_streamlit_handles_domain_example_and_unknown_text():
    from streamlit.testing.v1 import AppTest
    app=AppTest.from_file(str(ROOT/'app/streamlit_app.py')).run()
    assert not app.exception
    app.text_area[0].input('The service was excellent.')
    app.button[0].click().run()
    assert not app.exception
    app.text_area[0].input('Excelente servicio')
    app.button[0].click().run()
    assert not app.exception
    assert any('términos conocidos' in w.value for w in app.warning)


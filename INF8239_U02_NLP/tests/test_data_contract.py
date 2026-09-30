import json
from collections import Counter
from inf8239_u02.corpus import ROOT, read_rows, normalized, sha

def raw():
    return read_rows(ROOT/'data/raw/dataset.csv')

def test_size_and_schema():
    columns, rows = raw()
    assert len(rows) == 3000
    assert set(columns) == {'text','label','source','source_row'}

def test_nonempty_text_and_valid_labels():
    _,rows=raw()
    assert all(r['text'].strip() and r['label'] in {'0','1'} for r in rows)

def test_domains_and_balance():
    _,rows=raw()
    assert Counter((r['source'],r['label']) for r in rows) == {
        (d,l):500 for d in ['amazon','imdb','yelp'] for l in ['0','1']}

def test_download_hash():
    meta=json.loads((ROOT/'reports/download_manifest.json').read_text())
    assert sha((ROOT/'data/raw/dataset.csv').read_bytes())==meta['csv_sha256']

def test_processed_unique_text():
    _,rows=read_rows(ROOT/'data/processed/dataset.csv')
    keys=[normalized(r['text']) for r in rows]
    assert rows and all(keys) and len(keys)==len(set(keys))


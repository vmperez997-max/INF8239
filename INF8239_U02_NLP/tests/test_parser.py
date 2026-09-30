import io, zipfile
import pytest
from inf8239_u02.corpus import parse_archive, quantile

def archive(label='1'):
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w') as z:
        for name in ['amazon_cells','imdb','yelp']:
            z.writestr(name+'_labelled.txt','A "quoted" review.\t'+label+'\n')
    return buf.getvalue()

def test_quotes_do_not_merge_rows():
    rows=parse_archive(archive())
    assert len(rows)==3
    assert all(r['text']=='A "quoted" review.' for r in rows)

def test_bad_labels_rejected():
    with pytest.raises(ValueError):
        parse_archive(archive('7'))

def test_quantiles():
    assert quantile([1,2,3,4],.5)==2.5

def test_unicode_line_separator_is_part_of_text():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        for name in ['amazon_cells', 'imdb', 'yelp']:
            z.writestr(name+'_labelled.txt', 'One\u0085sentence.\t1\n')
    rows = parse_archive(buf.getvalue())
    assert len(rows) == 3
    assert all(r['text'] == 'One\u0085sentence.' for r in rows)


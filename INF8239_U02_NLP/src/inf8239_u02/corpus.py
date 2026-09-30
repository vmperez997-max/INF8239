from pathlib import Path
import csv, hashlib, io, json, os, urllib.request, zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]

def settings():
    path = ROOT / '.env'
    if not path.exists():
        path = ROOT / '.env.example'
    result = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip() and not line.lstrip().startswith('#'):
            key, value = line.split('=', 1)
            result[key.strip()] = os.getenv(key.strip(), value.strip())
    return result

def sha(data):
    return hashlib.sha256(data).hexdigest()

def parse_archive(data):
    rows = []
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for suffix, domain in [('amazon_cells_labelled.txt','amazon'), ('imdb_labelled.txt','imdb'), ('yelp_labelled.txt','yelp')]:
            matches = [n for n in z.namelist() if n.endswith('/'+suffix) or n == suffix]
            if len(matches) != 1:
                raise ValueError('Archivo esperado no encontrado: '+suffix)
            for number, line in enumerate(z.read(matches[0]).decode('utf-8-sig').split('\n'), 1):
                line = line.rstrip('\r')
                if not line:
                    continue
                text, label = line.rsplit('\t', 1)
                if label not in {'0','1'} or not text.strip():
                    raise ValueError('Etiqueta o texto inválido')
                rows.append(dict(text=text, label=label, source=domain, source_row=str(number)))
    return rows

def read_rows(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        rows = list(reader)
    return fields, rows

def download():
    c = settings()
    path = ROOT / c['DATASET_PATH']
    path.parent.mkdir(parents=True, exist_ok=True)
    report = ROOT / 'reports'
    report.mkdir(exist_ok=True)
    meta = dict(retrieved_utc=datetime.now(timezone.utc).isoformat(), mode=c['DATA_SOURCE'])
    if c['DATA_SOURCE'] == 'local':
        if not path.exists():
            raise FileNotFoundError('No existe el archivo local configurado')
        meta['source'] = 'Archivo local: documentar procedencia'
    elif c['DATA_SOURCE'] == 'url':
        url = c['DATASET_URL']
        if not url.startswith(('https://','http://')):
            raise ValueError('Se requiere URL HTTP(S)')
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
        if not data:
            raise ValueError('Descarga vacía')
        meta.update(source=url, source_sha256=sha(data), source_bytes=len(data))
        if zipfile.is_zipfile(io.BytesIO(data)):
            (path.parent/'source.zip').write_bytes(data)
            rows = parse_archive(data)
            with path.open('w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['text','label','source','source_row'])
                writer.writeheader()
                writer.writerows(rows)
        else:
            data.decode('utf-8-sig')
            path.write_bytes(data)
    else:
        raise ValueError('DATA_SOURCE debe ser local o url')
    fields, rows = read_rows(path)
    if not rows or not {c['TEXT_COLUMN'],c['TARGET_COLUMN']} <= set(fields):
        raise ValueError('Corpus vacío o columnas ausentes')
    meta.update(csv_sha256=sha(path.read_bytes()), rows=len(rows), columns=fields)
    (report/'download_manifest.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(meta, indent=2, ensure_ascii=False))

def normalized(text):
    return ' '.join(text.casefold().split())

def quantile(values, q):
    ordered = sorted(values)
    if not ordered:
        return None
    at = (len(ordered)-1)*q
    lo = int(at)
    hi = min(lo+1,len(ordered)-1)
    return ordered[lo]+(ordered[hi]-ordered[lo])*(at-lo)

def audit():
    c = settings()
    path = ROOT/c['DATASET_PATH']
    fields, rows = read_rows(path)
    tc, yc = c['TEXT_COLUMN'], c['TARGET_COLUMN']
    if not rows or not {tc,yc} <= set(fields):
        raise ValueError('Corpus vacío o esquema inválido')
    groups = defaultdict(set)
    for row in rows:
        groups[normalized(row.get(tc) or '')].add(row.get(yc))
    conflicts = {k for k,v in groups.items() if len(v)>1}
    seen, clean = set(), []
    for row in rows:
        key = normalized(row.get(tc) or '')
        if not key or not row.get(yc) or key in conflicts or key in seen:
            continue
        seen.add(key)
        clean.append(row)
    target = ROOT/'data/processed/dataset.csv'
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(clean)
    lengths = [len(row.get(tc) or '') for row in rows]
    nulls = {k:sum(not (row.get(k) or '').strip() for row in rows) for k in fields}
    result = dict(rows=len(rows), columns=fields, nulls=nulls,
        duplicate_rows=len(rows)-len({tuple(row[k] for k in fields) for row in rows}),
        duplicate_texts=len(rows)-len({row[tc] for row in rows}),
        normalized_duplicate_texts=len(rows)-len(groups),
        conflicting_groups=len(conflicts),
        conflicting_rows=sum(normalized(row.get(tc) or '') in conflicts for row in rows),
        classes=dict(Counter(row[yc] for row in rows)),
        sources=dict(Counter(row.get('source','unknown') for row in rows)),
        length_chars={str(q):quantile(lengths,q) for q in [.5,.9,.99]},
        min_chars=min(lengths), max_chars=max(lengths),
        processed_rows=len(clean), processed_classes=dict(Counter(row[yc] for row in clean)),
        csv_sha256=sha(path.read_bytes()))
    report = ROOT/'reports'
    report.mkdir(exist_ok=True)
    (report/'audit.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    with (report/'audit_columns.csv').open('w', encoding='utf-8', newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['column','nulls','unique'])
        writer.writerows((k,nulls[k],len({row[k] for row in rows})) for k in fields)
    (report/'audit.md').write_text('# Auditoría\n\n'+json.dumps(result,indent=2,ensure_ascii=False), encoding='utf-8')
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


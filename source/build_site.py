"""Build the site from build/data.json (Thai, from the harness) + translation overlays.

Adds   lesson['tr'][lang], unit['tr'][lang], block['text'][lang]   for lang in en, lo.
Thai stays in the base fields. A translation whose shape does not match the Thai is
dropped (the page falls back to Thai) and reported, so a missing line can never
shift notes or quiz answers out of place.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import tr_en, tr_lo, tr_en_blocks, tr_lo_blocks

ROOT = '/home/claude/site'
d = json.load(open(ROOT + '/build/data.json', encoding='utf-8'))
TR = {'en': (tr_en, tr_en_blocks), 'lo': (tr_lo, tr_lo_blocks)}
problems = []


def check_lesson(lang, th, t):
    """Return a cleaned overlay dict, or None if the shape differs from the Thai lesson."""
    p = lambda m: problems.append(f'{lang} {th["id"]}: {m}')
    ok = True
    for k in ('title', 'intro'):
        if not t.get(k): p(f'missing {k}'); ok = False
    if len(t.get('goals', [])) != len(th['goals']): p('goals count'); ok = False
    if len(t.get('arduino', [])) != len(th.get('arduino', [])): p('arduino count'); ok = False
    if bool(t.get('arduinoTitle')) != bool(th.get('arduinoTitle')): p('arduinoTitle presence'); ok = False
    exs = t.get('examples', [])
    if len(exs) != len(th['examples']): p('examples count'); ok = False
    else:
        for i, (a, b) in enumerate(zip(th['examples'], exs)):
            if len(a.get('notes', [])) != len(b.get('notes', [])): p(f'example {i+1} notes {len(a.get("notes", []))}≠{len(b.get("notes", []))}'); ok = False
            if not b.get('title'): p(f'example {i+1} title'); ok = False
            if bool(a.get('desc')) != bool(b.get('desc')): p(f'example {i+1} desc'); ok = False
    trs = t.get('tries', [])
    if len(trs) != len(th.get('tries', [])): p('tries count'); ok = False
    else:
        for i, (a, b) in enumerate(zip(th['tries'], trs)):
            if bool(a.get('answer')) != bool(b.get('answer')): p(f'try {i+1} answer presence'); ok = False
    qz = t.get('quiz', [])
    if len(qz) != len(th.get('quiz', [])): p('quiz count'); ok = False
    else:
        for i, (a, b) in enumerate(zip(th['quiz'], qz)):
            if len(a['choices']) != len(b.get('choices', [])): p(f'quiz {i+1} choices'); ok = False
            if not b.get('q') or not b.get('why'): p(f'quiz {i+1} text'); ok = False
    if not ok: return None
    return dict(title=t['title'], intro=t['intro'], goals=t['goals'], arduino=t.get('arduino', []), arduinoTitle=t.get('arduinoTitle', ''),
                examples=[dict(title=e['title'], desc=e.get('desc', ''), notes=e.get('notes', [])) for e in exs],
                tries=[dict(task=x['task'], answer=x.get('answer', '')) for x in trs],
                quiz=[dict(q=x['q'], choices=x['choices'], why=x['why']) for x in qz])


def check_block(lang, typ, th, t):
    if not t:
        problems.append(f'{lang} block {typ}: missing'); return None
    if len(t.get('params', [])) != len(th.get('params') or []):
        problems.append(f'{lang} block {typ}: params count'); return None
    if bool(t.get('warn')) != bool(th.get('warn')):
        problems.append(f'{lang} block {typ}: warn presence'); return None
    return dict(name=t['name'], desc=t['desc'], params=[list(x) for x in t.get('params', [])], warn=t.get('warn', ''))


for u in d['units']:
    u['tr'] = {lang: mod.UNITS[u['id']] for lang, (mod, _) in TR.items() if u['id'] in mod.UNITS}
for les in d['lessons']:
    les['tr'] = {}
    for lang, (mod, _) in TR.items():
        t = mod.L.get(les['id'])
        if t is None: problems.append(f'{lang} {les["id"]}: missing lesson'); continue
        c = check_lesson(lang, les, t)
        if c: les['tr'][lang] = c
for typ, b in d['blocks'].items():
    b['text'] = {}
    for lang, (_, bm) in TR.items():
        c = check_block(lang, typ, b, bm.BLOCKS.get(typ))
        if c: b['text'][lang] = c
extra = {lang: sorted(set(bm.BLOCKS) - set(d['blocks'])) for lang, (_, bm) in TR.items()}
for lang, ks in extra.items():
    if ks: problems.append(f'{lang} blocks not in site: {ks}')

if problems:
    print('TRANSLATION PROBLEMS (these fall back to Thai):'); print('\n'.join('  ' + x for x in problems))
else:
    print('translations: all lessons, units and blocks match the Thai shape')

recs = [dict(kind='units', units=d['units'])] + [dict(kind='lesson', lesson=l) for l in d['lessons']] + [dict(kind='block', type=t, block=b) for t, b in d['blocks'].items()]
t = open(ROOT + '/src/template.html', encoding='utf-8').read()
assert '__DATA__' in t
# หน้า "ติดตั้งโปรแกรม": ข้อความ 3 ภาษา + โค้ดทดสอบ (คอมไพล์ผ่านแล้ว) + รูปหน้าจอ
sys.path.insert(0, ROOT + '/src/install')
import install_text, shutil
inst = {'th': install_text.TH, 'en': install_text.EN, 'lo': install_text.LO}
test_code = open(ROOT + '/src/install/test_mini_r4.ino', encoding='utf-8').read()
t = t.replace('__INSTALL__', json.dumps(inst, ensure_ascii=False).replace('</', '<\\/'))
t = t.replace('__INSTALL_TEST__', json.dumps(test_code))
os.makedirs(ROOT + '/out/web/img', exist_ok=True)
for f in sorted(os.listdir(ROOT + '/src/install/img')):
    shutil.copy(ROOT + '/src/install/img/' + f, ROOT + '/out/web/img/' + f)
os.makedirs(ROOT + '/out/web', exist_ok=True)
# hosted version: page + data.json (one record per line)
open(ROOT + '/out/web/index.html', 'w', encoding='utf-8').write(t.replace('__DATA__', ''))
with open(ROOT + '/out/web/data.json', 'w', encoding='utf-8') as f:
    f.write('[\n' + ',\n'.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) for r in recs) + '\n]\n')
# offline single file
inline = json.dumps(recs, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
open(ROOT + '/out/KrubankR4-lessons-offline.html', 'w', encoding='utf-8').write(t.replace('__DATA__', inline))
for p in ['web/index.html', 'web/data.json', 'KrubankR4-lessons-offline.html']:
    print(p, round(os.path.getsize(ROOT + '/out/' + p) / 1024), 'KB')
sys.exit(1 if problems else 0)

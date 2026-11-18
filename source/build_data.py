"""Run every lesson example / try-solution through MATRIXblock's own generator and save site data."""
import json, sys, re
sys.path.insert(0, '/home/claude/site/src')
from playwright.sync_api import sync_playwright
import lessons_src as LS
from blocks_th import BLOCKS

cat = json.load(open('/home/claude/mbx/catalog.json', encoding='utf-8'))

def attach_ids(en, th):
    """copy ids from the english tree to the thai tree (same structure, different words)"""
    th['id'] = en.get('id')
    ve = [it['b'] for r in en['rows'] for it in r.get('items', []) if it['k'] == 'val']
    vt = [it['b'] for r in th['rows'] for it in r.get('items', []) if it['k'] == 'val']
    assert len(ve) == len(vt), (en['type'], len(ve), len(vt))
    for a, b in zip(ve, vt): attach_ids(a, b)
    se = [r for r in en['rows'] if 'stmt' in r]; st = [r for r in th['rows'] if 'stmt' in r]
    for re_, rt in zip(se, st):
        for be, bt in zip(re_['blocks'], rt['blocks']): attach_ids(be, bt)

def shorten(trees, ranges):
    m = {}
    def walk(n):
        old = n.get('id')
        if old is not None:
            m.setdefault(old, 'b%d' % len(m)); n['id'] = m[old]
        for r in n['rows']:
            for it in r.get('items', []):
                if it['k'] == 'val': walk(it['b'])
            for b in r.get('blocks', []): walk(b)
    for stack in trees:
        for n in stack: walk(n)
    return {m[k]: v for k, v in ranges.items() if k in m}

def strip_opts(n):
    for r in n['rows']:
        for it in r.get('items', []):
            it.pop('opts', None); it.pop('v', None)
            if it['k'] == 'val': strip_opts(it['b'])
        for b in r.get('blocks', []): strip_opts(b)
    for k in ('c2', 'c3'):
        pass
    return n

with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = br.new_page(viewport={'width': 1300, 'height': 1000})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:18200/harness/index.html'); pg.wait_for_function('window.ready === true')

    def program(xml, names):
        pg.evaluate("RX.setLocale('en')")
        pg.evaluate('n => RX.vars(n)', names or [])
        r = pg.evaluate('x => RX.runMapped(x)', xml)
        pg.evaluate("RX.setLocale('th')")
        pg.evaluate('n => RX.vars(n)', names or [])
        t = pg.evaluate('x => RX.runMapped(x)', xml)
        pg.evaluate("RX.setLocale('en')")
        assert t['code'] == r['code'], 'locale changed the code?!'
        for se, st in zip(r['trees'], t['trees']):
            for a, b in zip(se, st): attach_ids(a, b)
        ranges = shorten(r['trees'], r['ranges'])
        shorten(t['trees'], {})
        return dict(code=r['code'].rstrip() + '\n', ranges=ranges, en=[[strip_opts(n) for n in s] for s in r['trees']], th=[[strip_opts(n) for n in s] for s in t['trees']])

    lessons = []
    for les in LS.L:
        out = {k: v for k, v in les.items() if k not in ('examples', 'tries')}
        out['examples'] = []
        for ex in les.get('examples', []):
            e = {k: v for k, v in ex.items() if k != 'xml'}
            e.update(program(ex['xml'], ex.get('vars')))
            out['examples'].append(e)
        out['tries'] = []
        for tr in les.get('tries', []):
            e = {k: v for k, v in tr.items() if k != 'solution'}
            e.update(program(tr['solution'], tr.get('vars')))
            out['tries'].append(e)
        lessons.append(out)
        print('ok', les['id'], len(out['examples']), 'examples', len(out['tries']), 'tries')
    br.close()
print('page errors:', errs[:3])

blocks = {}
for c in cat:
    d = BLOCKS.get(c['type'], {})
    blocks[c['type']] = dict(cat=c['cat'], section=c['section'], shape=c['shape'], en=c['tree_en'], th=c['tree_th'],
                             value=c['value'], program=c['program'], variants=c.get('variants', []), defs=c['defs'],
                             name=d.get('name', c['type']), desc=d.get('desc', ''), params=d.get('params', []), warn=d.get('warn', ''))
missing = [c['type'] for c in cat if c['type'] not in BLOCKS]
print('blocks without Thai text:', missing)
json.dump(dict(units=LS.UNITS, lessons=lessons, blocks=blocks), open('/home/claude/site/build/data.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('data.json', round(len(open('/home/claude/site/build/data.json', encoding='utf-8').read()) / 1024), 'KB')

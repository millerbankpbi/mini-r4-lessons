"""Run every lesson example / try-solution through MATRIXblock's own generator and save site data."""
import html, json, sys, re
sys.path.insert(0, '/home/claude/site/src')
from playwright.sync_api import sync_playwright
import lessons_src as LS
from blocks_th import BLOCKS

cat = json.load(open('/home/claude/mbx/catalog.json', encoding='utf-8'))
RC_PRESETS = json.load(open('/home/claude/site/src/rc/presets.json', encoding='utf-8'))
# code-only sketches are shown as written in every site language, and code cannot be translated: no Thai / Lao text in them
NATIVE = re.compile(r'[\u0E00-\u0EFF]')


def code_only(lid, what, code):
    assert not NATIVE.search(code), (lid, what, 'code-only sketch has Thai/Lao text (comments?): explain it in notes/tips instead',
                                     [l for l in code.split('\n') if NATIVE.search(l)][:3])
    return dict(code=code.rstrip() + '\n', ranges={}, en=[], th=[])

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

HAT_FN = {'mini_ble_on_received': 'void onBLEWritten(', 'mini_mqtt_on_message': 'void mqttCallback('}

def hat_ranges(trees, code, ranges):
    """a hat block becomes a whole function above setup(); the harness gives it no line range, so map the function"""
    lines = code.split('\n')
    for stack in trees:
        n = stack[0] if stack else None
        head = n and HAT_FN.get(n['type'])
        if not head or not n.get('id') or n['id'] in ranges: continue
        a = next((i for i, l in enumerate(lines) if l.startswith(head)), None)
        b = next((i for i in range(a, len(lines)) if lines[i] == '}'), None) if a is not None else None
        assert b is not None, (n['type'], 'function not found in code')
        ranges[n['id']] = [a, b]

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
        hat_ranges(r['trees'], r['code'], ranges)
        return dict(code=r['code'].rstrip() + '\n', ranges=ranges, en=[[strip_opts(n) for n in s] for s in r['trees']], th=[[strip_opts(n) for n in s] for s in t['trees']])

    def check_notes(lid, e):
        """every note chip must name text from one line of the code (the page highlights that line).
        Chips are set with innerHTML, so a raw '<' that starts a tag (<ArduinoBLE.h>) would vanish: write &lt; instead."""
        raw = [n[0] for n in e.get('notes', []) if re.search(r'<[A-Za-z/!?]', n[0])]
        assert not raw, (lid, e['title'], 'note code has a raw <, write &lt; and &gt;', raw)
        lines = e['code'].split('\n')
        bad = [n[0] for n in e.get('notes', []) if not any(html.unescape(n[0]) in l for l in lines)]
        assert not bad, (lid, e['title'], 'note not in code', bad)

    lessons = []
    for les in LS.L:
        out = {k: v for k, v in les.items() if k not in ('examples', 'tries')}
        if les.get('rc'):
            # the controller link type picks the hint under the lesson's controller button (Bluefy for BLE, any browser for MQTT)
            assert les['rc'] in RC_PRESETS, (les['id'], 'unknown controller preset', les['rc'])
            out['rcLink'] = RC_PRESETS[les['rc']]['link']
        out['examples'] = []
        for ex in les.get('examples', []):
            e = {k: v for k, v in ex.items() if k != 'xml'}
            if 'xml' in ex:
                e.update(program(ex['xml'], ex.get('vars')))
            else:
                # code-only example: a whole C++ sketch with no blocks (nothing in MATRIXblock makes it), kept as written
                assert ex.get('codeOnly') is True and ex.get('code'), (les['id'], ex.get('title'), 'needs xml, or codeOnly=True with code')
                e.update(code_only(les['id'], ex.get('title'), ex['code']))
            check_notes(les['id'], e)
            out['examples'].append(e)
        out['tries'] = []
        for tr in les.get('tries', []):
            e = {k: v for k, v in tr.items() if k != 'solution'}
            if 'solution' in tr:
                e.update(program(tr['solution'], tr.get('vars')))
            else:
                # code-only answer (a C++ lesson with no blocks): the whole sketch as written
                assert tr.get('codeOnly') is True and tr.get('code'), (les['id'], tr.get('task', '')[:40], 'needs solution, or codeOnly=True with code')
                e.update(code_only(les['id'], tr.get('task', '')[:40], tr['code']))
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

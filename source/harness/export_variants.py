import json
from playwright.sync_api import sync_playwright
cat = json.load(open('/home/claude/mbx/catalog.json', encoding='utf-8'))
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = br.new_page(); pg.goto('http://127.0.0.1:18200/harness/index.html'); pg.wait_for_function('window.ready === true')
    pg.evaluate("RX.setLocale('en')")
    for c in cat:
        pg.evaluate("RX.vars(['score'])")
        v = pg.evaluate('x => RX.variants(x)', '<xml>' + c['xml'] + '</xml>')
        c['variants'] = [f for f in v['fields'] if len(f['rows']) > 1]
    br.close()
json.dump(cat, open('/home/claude/mbx/catalog.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for c in cat:
    for f in c['variants']:
        if c['cat'] in ('move', 'core', 'looks', 'sensing') or c['type'] in ('operator_mathop',):
            rows = f['rows'] if len(f['rows']) <= 8 else f['rows'][:4] + [['…', '', '']] + f['rows'][-2:]
            print(c['type'], f['field'], ' || '.join('%s => %s' % (r[0], r[2].replace('\n', ' ')[:70]) for r in rows))

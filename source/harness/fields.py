import json
from playwright.sync_api import sync_playwright
cat = json.load(open('/home/claude/mbx/catalog.json', encoding='utf-8'))
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = br.new_page(); pg.goto('http://127.0.0.1:18200/harness/index.html'); pg.wait_for_function('window.ready === true')
    for c in cat:
        pg.evaluate("RX.vars(['score'])")
        info = pg.evaluate("""x => { const b = RX.load(x)[0]; const out = [];
          for (const inp of b.inputList) { const fs = inp.fieldRow.filter(f => f.name).map(f => f.name + '=' + f.getValue());
            out.push((inp.type === 1 ? 'V:' : inp.type === 3 ? 'S:' : '') + (inp.name || '') + (fs.length ? '{' + fs.join(',') + '}' : '')); }
          return out.filter(s => s && s !== '').join(' '); }""", '<xml>' + c['xml'] + '</xml>')
        c['inputs'] = info
        print('%-34s %s' % (c['type'], info))
    br.close()
json.dump(cat, open('/home/claude/mbx/catalog.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

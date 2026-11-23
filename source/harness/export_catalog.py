import json, re, xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
src = re.sub(r'<\?xml[^>]*>', '', open('/home/claude/mbx/blockly-core/_Toolbox.xml', encoding='utf-8').read())
src = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;|#)', '&amp;', src)
root = ET.fromstring(src)
WANT = {'%{BKY_CATEGORY__MINI}': 'core', '%{BKY_CATEGORY__MOVEMENT}': 'move', '%{BKY_CATEGORY__MINI_LOOKS}': 'looks',
        '%{BKY_CATEGORY__MINI_SERIAL}': 'serial', '%{BKY_CATEGORY__MINI_SENSORS}': 'sensing',
        '%{BKY_CATEGORY__MINI_IOT}': 'iot', '%{BKY_CATEGORY_CONTROL}': 'control', '%{BKY_CATEGORY_OPERATORS}': 'ops'}
SENSE_KEEP = {'mini_motion_reset', 'mini_motion_getAccel', 'mini_motion_getGyro', 'mini_motion_getEuler', 'mini_MXGrayscale_getGrayscale',
              'mini_MXPot_getPot', 'mini_i2c_MXcolorV3_begin', 'mini_i2c_MXcolorV3_getColor', 'mini_i2c_MXLaserV2_begin', 'mini_i2c_MXLaserV2_getDistance'}
items = []
for cat in root.iter('category'):
    key = WANT.get(cat.get('name'))
    if not key: continue
    section = ''
    for el in cat:
        if el.tag == 'label': section = (el.get('text') or '').strip(' ·'); continue
        if el.tag != 'block': continue
        if key == 'sensing' and el.get('type') not in SENSE_KEEP: continue
        items.append({'cat': key, 'section': section, 'type': el.get('type'), 'xml': ET.tostring(el, encoding='unicode')})
# variables (dynamic flyout)
for t, x in [('data_variable', '<block type="data_variable"><field name="VARIABLE" id="v_score" variabletype="">score</field></block>'),
             ('data_setvariableto', '<block type="data_setvariableto"><field name="VARIABLE" id="v_score" variabletype="">score</field><value name="VALUE"><shadow type="text"><field name="TEXT">0</field></shadow></value></block>'),
             ('data_changevariableby', '<block type="data_changevariableby"><field name="VARIABLE" id="v_score" variabletype="">score</field><value name="VALUE"><shadow type="math_number"><field name="NUM">1</field></shadow></value></block>')]:
    items.append({'cat': 'vars', 'section': '', 'type': t, 'xml': x})
print(len(items), 'blocks')
SETUP = '<xml><block type="mini_setup" x="10" y="10"><statement name="SUBSTACK2">%s</statement></block></xml>'
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = br.new_page(viewport={'width': 1300, 'height': 1000})
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:18200/harness/index.html'); pg.wait_for_function('window.ready === true')
    out = []
    for loc in ['en', 'th']:
        pg.evaluate('l => RX.setLocale(l)', loc)
        for it in items:
            pg.evaluate("RX.vars(['score'])")
            x = '<xml>' + it['xml'] + '</xml>'
            v = pg.evaluate('x => RX.valueCode(x)', x)
            rec = out[[o['type'] for o in out].index(it['type'])] if loc == 'th' else dict(it)
            rec['tree_' + loc] = v['tree'][0]
            if loc == 'en':
                shape = v['tree'][0]['shape']
                rec['shape'] = shape
                rec['value'] = v['code'] if shape in ('rep', 'bool') else None
                rec['defs'] = v['defs']; rec['setups'] = v['setups']
                if shape == 'hat' and v['defs']:  # hat blocks only add a callback definition: show that function as their code
                    rec['value'] = '\n'.join(l for l in v['defs'][-1].splitlines() if l.strip())
                if shape in ('stack', 'cap'):
                    body = it['xml']
                elif shape in ('rep', 'bool'):
                    body = '<block type="mini_Serial_println"><value name="STRING">%s</value></block>' % it['xml']
                else:
                    body = ''
                if it['type'] == 'mini_setup':
                    rec['program'] = pg.evaluate('x => RX.run(x).code', '<xml>' + it['xml'] + '</xml>')
                else:
                    pg.evaluate("RX.vars(['score'])")
                    rec['program'] = pg.evaluate('x => RX.run(x).code', SETUP % body)
                out.append(rec)
    br.close()
json.dump(out, open('/home/claude/mbx/catalog.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('errors', errs[:3])
for o in out:
    print('%-8s %-34s %-5s %s' % (o['cat'], o['type'], o['shape'], (o['value'] or o['program'].split('void loop()\n{\n')[-1].strip().replace('\n', ' '))[:110]))

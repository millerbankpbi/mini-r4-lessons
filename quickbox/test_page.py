# ทดสอบหน้าเว็บ Quick Dun Dun ด้วยเบราว์เซอร์จริง (Playwright)
# วิธีรัน: เปิดเซิร์ฟเวอร์ในโฟลเดอร์นี้ก่อน  python3 -m http.server 8765  แล้ว  python3 test_page.py
import asyncio, sys
from playwright.async_api import async_playwright

URL = 'http://localhost:8765/index.html'
FULL = 'F33 R F30 R F32 B32 U F63 B32 L F30 R F32 B32 R F60 L F32 B32 R F29 L F32 B32 U F63 B32 R F29 L F32'
passed = failed = 0
def ok(cond, name, extra=''):
    global passed, failed
    if cond: passed += 1; print('ผ่าน  ' + name)
    else: failed += 1; print('ไม่ผ่าน  ' + name + ('  → ' + str(extra) if extra else ''))

# หุ่นปลอมที่ตอบตามโปรโตคอลเดียวกับเฟิร์มแวร์ QuickBox.ino
def start_with(block): return {'blocks': {'languageVersion': 0, 'blocks': [{'type': 'qb_start', 'x': 24, 'y': 24, 'deletable': False, 'next': {'block': block}}]}}
num = lambda n: {'shadow': {'type': 'math_number', 'fields': {'NUM': n}}}
# ทำซ้ำ 2 ครั้ง [ดันกระป๋อง] · เริ่มนับระยะใหม่ · ทำซ้ำจนกว่า ระยะที่วิ่ง ≥ 30 [เดินหน้า 10]   ฟังก์ชัน ดันกระป๋อง = เดินหน้า 20, ถอยหลัง 20
LOOP_STATE = start_with({'type': 'controls_repeat_ext', 'inputs': {'TIMES': num(2), 'DO': {'block': {'type': 'procedures_callnoreturn', 'extraState': {'name': 'ดันกระป๋อง'}}}},
  'next': {'block': {'type': 'qb_dist_reset', 'next': {'block': {'type': 'controls_whileUntil', 'fields': {'MODE': 'UNTIL'},
    'inputs': {'BOOL': {'block': {'type': 'logic_compare', 'fields': {'OP': 'GTE'}, 'inputs': {'A': {'block': {'type': 'qb_dist'}}, 'B': num(30)}}},
               'DO': {'block': {'type': 'qb_forward', 'fields': {'CM': 10}}}}}}}}})
LOOP_STATE['blocks']['blocks'].append({'type': 'procedures_defnoreturn', 'x': 420, 'y': 40, 'fields': {'NAME': 'ดันกระป๋อง'},
  'inputs': {'STACK': {'block': {'type': 'qb_forward', 'fields': {'CM': 20}, 'next': {'block': {'type': 'qb_back', 'fields': {'CM': 20}}}}}}})
RECURSE_STATE = start_with({'type': 'procedures_callnoreturn', 'extraState': {'name': 'วน'}})
RECURSE_STATE['blocks']['blocks'].append({'type': 'procedures_defnoreturn', 'x': 420, 'y': 40, 'fields': {'NAME': 'วน'},
  'inputs': {'STACK': {'block': {'type': 'qb_forward', 'fields': {'CM': 5}, 'next': {'block': {'type': 'procedures_callnoreturn', 'extraState': {'name': 'วน'}}}}}}})

FAKE_ROBOT = r"""
(() => {
  const listeners = [];
  const robot = { steps: [], log: [], tooLong: 0 };
  window.__robot = robot;
  const notify = (text) => setTimeout(() => listeners.forEach((f) => f({ target: { value: new TextEncoder().encode(text) } })), 5);
  const listen = { startNotifications: async () => {}, addEventListener: (t, f) => listeners.push(f) };
  const handle = (t) => {
    if (t === 'P') notify('R');
    else if (t === 'N') { robot.steps = []; notify('OK0'); }
    else if (t[0] === '+') { robot.steps.push(...t.slice(1).split(' ')); notify('OK' + robot.steps.length); }
    else if (t[0] === 'E') notify(Number(t.slice(1)) === robot.steps.length ? 'READY' + robot.steps.length : 'ERR' + robot.steps.length);
    else if (t === 'G') {
      notify('RUN');
      robot.steps.forEach((s, i) => setTimeout(() => notify('S' + i), 40 * (i + 1)));
      setTimeout(() => notify('DONE 12.3'), 40 * (robot.steps.length + 2));
    } else if (t === 'X') notify('STOP');
  };
  const toRobot = { writeValueWithResponse: async (data) => {
    if (data.length > 20) robot.tooLong++;
    const t = new TextDecoder().decode(data); robot.log.push(t); handle(t);
  } };
  const device = { name: 'QB-T01', addEventListener() {}, gatt: { connected: false,
    async connect() { this.connected = true; return { getPrimaryService: async () => ({ getCharacteristic: async (u) => u.startsWith('6e400002') ? toRobot : listen }) }; },
    disconnect() { this.connected = false; } } };
  Object.defineProperty(navigator, 'bluetooth', { value: { requestDevice: async () => device } });
})();
"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 1366, 'height': 860})
        await ctx.route('**/fonts.googleapis.com/**', lambda r: r.abort())
        await ctx.add_init_script(FAKE_ROBOT)
        pg = await ctx.new_page()
        errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))
        await pg.goto(URL); await pg.evaluate('localStorage.clear()'); await pg.reload()
        await pg.wait_for_timeout(500)

        ok(await pg.text_content('#progText') == 'F33' and await pg.text_content('#count') == '1 คำสั่ง', 'เปิดครั้งแรกมีตัวอย่าง เดินหน้า 33 ซม.')
        cats = await pg.evaluate("ws.getToolbox().getToolboxItems().map((c) => c.getName())")
        ok(cats == ['เคลื่อนที่', 'ทำซ้ำ', 'ระยะทาง', 'เปรียบเทียบ', 'ฟังก์ชัน'], 'มีหมวดบล็อก เคลื่อนที่ ทำซ้ำ ระยะทาง เปรียบเทียบ ฟังก์ชัน', cats)
        ok(not await pg.evaluate("document.body.classList.contains('sim-open')") and not await pg.is_visible('#run'),
           'เปิดมา ตัวจำลองย่ออยู่ (พื้นที่ต่อบล็อกใหญ่)')
        ok(await pg.evaluate("$('blockly').clientWidth") > 900, 'พื้นที่ต่อบล็อกกว้างเกิน 900 px บนจอคอม', await pg.evaluate("$('blockly').clientWidth"))

        # แก้เป็นตัวอักษร → สร้างบล็อก
        await pg.click('#textToggle')
        await pg.fill('#textIn', 'F33 X R')
        await pg.click('#textApply')
        ok('ไม่รู้จักคำสั่ง' in await pg.text_content('#textErr'), 'พิมพ์คำสั่งผิด แจ้งเตือนภาษาไทย', await pg.text_content('#textErr'))
        await pg.fill('#textIn', FULL.lower())
        await pg.click('#textApply'); await pg.wait_for_timeout(400)
        ok(await pg.text_content('#progText') == FULL, 'สร้างบล็อกจากข้อความได้ครบ (ตัวพิมพ์เล็กก็ได้)')
        ok(await pg.evaluate("ws.getAllBlocks(false).length") == len(FULL.split()) + 1, 'จำนวนบล็อกบนพื้นที่ตรงกับคำสั่ง + บล็อกเริ่ม')

        # จำลองแบบแอนิเมชัน (กดขยายก่อน)
        await pg.click('#simToggle'); await pg.wait_for_timeout(300)
        ok(await pg.is_visible('#run') and await pg.text_content('#simToggle') == 'ย่อ', 'กดขยาย ตัวจำลองกว้างขึ้นและมีปุ่มจำลอง')
        await pg.click('.seg button[data-x="4"]')
        await pg.click('#run'); await pg.wait_for_timeout(1500)
        mid = int(await pg.text_content('#total'))
        lit = await pg.evaluate('lit')
        ok(0 < mid < 200, 'ระหว่างจำลอง คะแนนขึ้นทีละขั้น', mid)
        ok(lit is not None and await pg.evaluate("ws.getBlockById(lit) && ws.getBlockById(lit).type.startsWith('qb_')"), 'ระหว่างจำลอง บล็อกที่กำลังทำถูกไฮไลต์')
        await pg.click('#skip'); await pg.wait_for_timeout(200)
        ok(await pg.text_content('#total') == '200' and await pg.text_content('#clock') == '48.6', 'ดูผลทันที: ได้ 200 เวลา 48.6 วินาที',
           (await pg.text_content('#total'), await pg.text_content('#clock')))
        ok(await pg.evaluate("document.querySelectorAll('.tile.reached.out').length") == 7, 'ช่อง 2–8 ขึ้นว่าถึงแล้วและดันออกแล้วครบ 7 ช่อง')
        ok('โบนัส' in await pg.text_content('#log'), 'บันทึกเหตุการณ์มีโบนัส')
        await pg.click('#reset')
        ok(await pg.text_content('#total') == '0', 'กดเริ่มใหม่ คะแนนกลับเป็น 0')

        # วนซ้ำ ฟังก์ชัน และระยะที่วิ่ง
        await pg.evaluate('(s) => loadState(s)', LOOP_STATE); await pg.wait_for_timeout(400)
        ok(await pg.text_content('#progText') == 'P2 Q5 F20 B20 J1 Z Yd<30@9 F10 J6', 'ทำซ้ำ + ฟังก์ชัน + ทำซ้ำจนกว่า แปลงเป็นโปรแกรมถูก',
           await pg.text_content('#progText'))
        await pg.click('#skip'); await pg.wait_for_timeout(200)
        res = await pg.evaluate("sim.result")
        ok(res['odo'] == 30 and abs(res['robot']['y'] - (108.5 - 30)) < 0.01, 'จำลอง: เริ่มนับระยะใหม่แล้วเดินหน้าจนระยะ ≥ 30 หยุดห่างจุดเริ่ม 30 ซม.', res['robot'])
        ok(not await pg.evaluate("Blockly.icons.MutatorIcon && ws.getBlocksByType('procedures_defnoreturn')[0].hasIcon(Blockly.icons.MutatorIcon.TYPE)"),
           'บล็อกฟังก์ชันไม่มีปุ่มเพิ่มตัวแปร')
        flyout = await pg.evaluate("ws.getToolboxCategoryCallback('QB_FUNCS')(ws).map((i) => i.type || i.kind)")
        ok(flyout == ['label', 'procedures_defnoreturn', 'label', 'procedures_callnoreturn'], 'หมวดฟังก์ชันมีบล็อกเรียกฟังก์ชันที่สร้างไว้', flyout)
        # ลากบล็อกฟังก์ชันใหม่ออกมา 2 อัน ได้ชื่อไม่ซ้ำกัน
        names = await pg.evaluate("""(() => { for (let i = 0; i < 2; i++) { const b = ws.newBlock('procedures_defnoreturn'); b.setFieldValue(Blockly.Msg.PROCEDURES_DEFNORETURN_PROCEDURE, 'NAME'); b.initSvg(); b.render(); }
          return ws.getBlocksByType('procedures_defnoreturn').map((d) => d.getFieldValue('NAME')); })()""")
        ok(len(set(names)) == len(names) and all(names), 'ฟังก์ชันใหม่มีชื่อ และชื่อไม่ซ้ำกัน', names)
        # ทำซ้ำจนกว่า แต่ไม่ใส่เงื่อนไข
        await pg.evaluate("(() => { const b = ws.getBlocksByType('controls_whileUntil')[0]; b.getInputTargetBlock('BOOL').dispose(); })()")
        await pg.wait_for_timeout(400)
        ok(await pg.evaluate("$('orphan').classList.contains('err')") and 'ใส่บล็อกเปรียบเทียบ' in await pg.text_content('#orphan'),
           'ทำซ้ำจนกว่าไม่มีเงื่อนไข: แจ้งเตือนสีแดงบอกวิธีแก้', await pg.text_content('#orphan'))
        ok(await pg.evaluate("marked === ws.getBlocksByType('controls_whileUntil')[0].id"), 'ป้ายเตือนติดที่บล็อกที่ผิด')
        await pg.click('#run'); await pg.wait_for_timeout(200)
        ok('แก้บล็อกที่มีป้ายเตือนก่อน' in await pg.text_content('#log'), 'มีบล็อกผิด กดจำลองแล้วบอกให้แก้ก่อน')
        # ฟังก์ชันเรียกตัวเอง
        await pg.evaluate("(s) => loadState(s)", RECURSE_STATE); await pg.wait_for_timeout(400)
        ok('เรียกตัวเอง' in await pg.text_content('#orphan'), 'ฟังก์ชันเรียกตัวเอง แจ้งเตือน', await pg.text_content('#orphan'))
        await pg.evaluate("(t) => loadState(chainState(QB.parse(t)))", FULL)
        await pg.wait_for_timeout(300)

        # จำโปรแกรมไว้ในเครื่อง
        await pg.reload(); await pg.wait_for_timeout(500)
        ok(await pg.text_content('#progText') == FULL, 'รีเฟรชหน้าแล้วบล็อกยังอยู่')

        # บล็อกลอย และบล็อกเริ่มซ้ำ
        await pg.evaluate("(() => { const b = ws.newBlock('qb_left'); b.initSvg(); b.render(); b.moveBy(400, 300); })()")
        await pg.wait_for_timeout(400)
        ok(await pg.is_visible('#orphan') and 'ไม่ได้ต่อ' in await pg.text_content('#orphan'), 'บล็อกที่ไม่ได้ต่อกับ "เมื่อเริ่ม" มีคำเตือน')
        ok(await pg.text_content('#progText') == FULL, 'บล็อกลอยไม่ถูกนับเป็นโปรแกรม')
        await pg.evaluate("(() => { const b = ws.newBlock('qb_start'); b.initSvg(); b.render(); })()")
        await pg.wait_for_timeout(400)
        ok(await pg.evaluate("ws.getBlocksByType('qb_start', false).length") == 1, 'บล็อก "เมื่อเริ่ม" มีได้อันเดียว')

        # ลิงก์โปรแกรม ?p=
        await pg.goto(URL + '?p=F33+R+F30+Z'); await pg.wait_for_timeout(500)
        ok(await pg.text_content('#progText') == 'F33 R F30 Z', 'เปิดลิงก์ ?p= แล้วได้บล็อกตามลิงก์')

        # Bluetooth กับหุ่นปลอม
        ok('next' in await pg.get_attribute('#btConnect', 'class'), 'ยังไม่เชื่อมต่อ: ปุ่มเชื่อมต่อหุ่นมีวงแสงบอกให้กดก่อน')
        await pg.click('#btConnect'); await pg.wait_for_timeout(300)
        ok('next' in await pg.get_attribute('#btSend', 'class') and 'next' not in await pg.get_attribute('#btConnect', 'class'), 'เชื่อมต่อแล้ว: วงแสงย้ายไปที่ปุ่มส่งโค้ด')
        ok(await pg.text_content('#btConnectLabel') == 'QB-T01', 'ปุ่มเชื่อมต่อแสดงชื่อหุ่นที่ต่ออยู่')
        ok('เชื่อมต่อ QB-T01 แล้ว' in await pg.text_content('#btStatus'), 'เชื่อมต่อหุ่นได้', await pg.text_content('#btStatus'))
        ok(await pg.is_disabled('#btGo'), 'ยังไม่ได้ส่งโปรแกรม ปุ่มเริ่มวิ่งกดไม่ได้')
        await pg.click('#textToggle'); await pg.fill('#textIn', FULL); await pg.click('#textApply'); await pg.wait_for_timeout(400)
        await pg.click('#btSend'); await pg.wait_for_timeout(800)
        robot = await pg.evaluate('window.__robot')
        ok(' '.join(robot['steps']) == FULL, 'หุ่นได้รับคำสั่งครบและเรียงถูก', ' '.join(robot['steps']))
        ok(robot['tooLong'] == 0, 'ทุกข้อความที่ส่งยาวไม่เกิน 20 ไบต์')
        ok('next' in await pg.get_attribute('#btGo', 'class'), 'ส่งโค้ดแล้ว: วงแสงย้ายไปที่ปุ่มหุ่นยนต์ เริ่มวิ่ง')
        ok('หุ่นได้รับ %d คำสั่งแล้ว' % len(FULL.split()) in await pg.text_content('#btStatus'), 'แจ้งว่าหุ่นได้รับกี่คำสั่ง', await pg.text_content('#btStatus'))
        await pg.click('#btGo'); await pg.wait_for_timeout(300)
        ok('running' in await pg.get_attribute('#btGo', 'class') and await pg.evaluate("getComputedStyle($('btGo')).opacity") == '1' and 'วิ' in await pg.text_content('#btGoLabel'),
           'ระหว่างหุ่นวิ่ง ปุ่มหุ่นยนต์เป็นสีเขียวสด ไม่จาง และเดินเวลา', await pg.text_content('#btGoLabel'))
        ok('หุ่นกำลังทำ: ' in await pg.text_content('#btStatus'), 'ระหว่างหุ่นวิ่ง บอกว่ากำลังทำคำสั่งอะไร', await pg.text_content('#btStatus'))
        ok(await pg.evaluate('lit') is not None, 'ระหว่างหุ่นวิ่ง ไฮไลต์บล็อกที่หุ่นกำลังทำ')
        await pg.wait_for_timeout(1600)
        ok('12.3 วินาที' in await pg.text_content('#btStatus'), 'หุ่นวิ่งจบ แสดงเวลาจากหุ่น', await pg.text_content('#btStatus'))
        ok(await pg.text_content('#btGoLabel') == 'เริ่มวิ่ง' and 'running' not in await pg.get_attribute('#btGo', 'class'), 'วิ่งจบแล้ว ปุ่มกลับเป็น เริ่มวิ่ง')
        await pg.fill('#textIn', 'F40'); await pg.click('#textApply'); await pg.wait_for_timeout(400)
        ok('ชุดเก่า' in await pg.text_content('#btStatus'), 'แก้บล็อกหลังส่ง เตือนว่าโปรแกรมในหุ่นยังเป็นชุดเก่า', await pg.text_content('#btStatus'))
        await pg.click('#btStop'); await pg.wait_for_timeout(200)
        ok(await pg.evaluate("window.__robot.log.includes('X')"), 'ปุ่มหยุดส่ง X ไปหุ่น')
        # หุ่นถูกกด UP ตอนเว็บเพิ่งต่อใหม่ (เว็บไม่รู้ว่าในหุ่นมีกี่คำสั่ง) ต้องไม่ error
        await pg.evaluate("window.__robot.steps = ['F33','R']")
        await pg.click('#btConnect'); await pg.wait_for_timeout(300)
        await pg.evaluate("fromRobot('RUN'); fromRobot('S1')")
        ok('คำสั่งที่ 2' in await pg.text_content('#btStatus'), 'หุ่นวิ่งจากปุ่ม UP ก็แสดงขั้นที่กำลังทำ', await pg.text_content('#btStatus'))
        await pg.evaluate("fromRobot('STOP'); fromRobot('NOPROG')")
        ok('ยังไม่มีโปรแกรม' in await pg.text_content('#btStatus'), 'หุ่นไม่มีโปรแกรมแล้วกดวิ่ง เว็บบอกให้ส่งก่อน')
        # ส่งโปรแกรมที่มีวนซ้ำและฟังก์ชันไปหุ่น
        await pg.evaluate('(s) => loadState(s)', LOOP_STATE); await pg.wait_for_timeout(400)
        await pg.click('#btSend'); await pg.wait_for_timeout(600)
        ok(' '.join(await pg.evaluate('window.__robot.steps')) == 'P2 Q5 F20 B20 J1 Z Yd<30@9 F10 J6', 'ส่งโปรแกรมที่มีวนซ้ำ/ฟังก์ชันไปหุ่นได้ครบ')
        await pg.evaluate("fromRobot('RUN'); fromRobot('S3')")
        ok('ถอยหลัง 20 ซม.' in await pg.text_content('#btStatus') and await pg.evaluate("ws.getBlockById(lit).type") == 'qb_back',
           'หุ่นทำคำสั่งในฟังก์ชัน: เว็บไฮไลต์บล็อกข้างในฟังก์ชัน', await pg.text_content('#btStatus'))
        await pg.evaluate("fromRobot('DONE 3.0')")

        # มือถือ
        m = await b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        await m.goto(URL + '?p=' + FULL.replace(' ', '+')); await m.wait_for_timeout(600)
        h = await m.evaluate("$('blockly').getBoundingClientRect().height")
        ok(h > 844 * 0.55, 'มือถือ: พื้นที่ต่อบล็อกสูงเกินครึ่งจอ', h)
        strip = await m.evaluate("(() => { const r = $('arena').getBoundingClientRect(); return [Math.round(r.bottom), Math.round(r.height)]; })()")
        ok(strip[0] == 844 and strip[1] < 100, 'มือถือ: ตัวจำลองเป็นแถบเล็กด้านล่าง', strip)
        await m.click('#simToggle'); await m.wait_for_timeout(300)
        full = await m.evaluate("(() => { const r = $('arena').getBoundingClientRect(); return [Math.round(r.top), Math.round(r.height)]; })()")
        ok(full == [0, 844] and await m.text_content('#simToggle') == 'กลับไปต่อบล็อก', 'มือถือ: กดขยายแล้วตัวจำลองเต็มจอ', full)
        top = await m.evaluate("(() => { const r = $('run').getBoundingClientRect(); return document.elementFromPoint(r.left + 10, r.top + 10).closest('#run') !== null; })()")
        ok(top, 'มือถือ: ปุ่มจำลองไม่ถูกแถบหมวดบล็อกบัง')
        await m.click('#skip'); await m.wait_for_timeout(200)
        await m.screenshot(path='/home/claude/qb-build/mobile.png', full_page=True)
        ok(await m.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'จอมือถือไม่มีแถบเลื่อนแนวนอน')
        await m.click('#simToggle'); await m.wait_for_timeout(300)
        ok(not await m.evaluate("document.body.classList.contains('sim-open')") and await m.is_visible('#blockly'), 'มือถือ: กดกลับไปต่อบล็อกได้')

        ok(not errors, 'ไม่มี error ในหน้าเว็บ', errors)
        await b.close()
    print('\n%d ผ่าน, %d ไม่ผ่าน' % (passed, failed))
    sys.exit(1 if failed else 0)

asyncio.run(main())

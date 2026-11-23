# ทดสอบหน้าเว็บ Quick Box Drop ด้วยเบราว์เซอร์จริง (Playwright)
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
        ok(await pg.evaluate("document.querySelectorAll('.blocklyFlyout .blocklyDraggable').length") == 6, 'แถบบล็อกมี 6 แบบเท่านั้น',
           await pg.evaluate("document.querySelectorAll('.blocklyFlyout .blocklyDraggable').length"))

        # แก้เป็นตัวอักษร → สร้างบล็อก
        await pg.click('#textToggle')
        await pg.fill('#textIn', 'F33 X R')
        await pg.click('#textApply')
        ok('ไม่รู้จักคำสั่ง' in await pg.text_content('#textErr'), 'พิมพ์คำสั่งผิด แจ้งเตือนภาษาไทย', await pg.text_content('#textErr'))
        await pg.fill('#textIn', FULL.lower())
        await pg.click('#textApply'); await pg.wait_for_timeout(400)
        ok(await pg.text_content('#progText') == FULL, 'สร้างบล็อกจากข้อความได้ครบ (ตัวพิมพ์เล็กก็ได้)')
        ok(await pg.evaluate("ws.getAllBlocks(false).length") == len(FULL.split()) + 1, 'จำนวนบล็อกบนพื้นที่ตรงกับคำสั่ง + บล็อกเริ่ม')

        # จำลองแบบแอนิเมชัน
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
        await pg.goto(URL + '?p=F33+R+F30'); await pg.wait_for_timeout(500)
        ok(await pg.text_content('#progText') == 'F33 R F30', 'เปิดลิงก์ ?p= แล้วได้บล็อกตามลิงก์')

        # Bluetooth กับหุ่นปลอม
        await pg.click('#btConnect'); await pg.wait_for_timeout(300)
        ok('เชื่อมต่อ QB-T01 แล้ว' in await pg.text_content('#btStatus'), 'เชื่อมต่อหุ่นได้', await pg.text_content('#btStatus'))
        ok(await pg.is_disabled('#btGo'), 'ยังไม่ได้ส่งโปรแกรม ปุ่มเริ่มวิ่งกดไม่ได้')
        await pg.click('#textToggle'); await pg.fill('#textIn', FULL); await pg.click('#textApply'); await pg.wait_for_timeout(400)
        await pg.click('#btSend'); await pg.wait_for_timeout(800)
        robot = await pg.evaluate('window.__robot')
        ok(' '.join(robot['steps']) == FULL, 'หุ่นได้รับคำสั่งครบและเรียงถูก', ' '.join(robot['steps']))
        ok(robot['tooLong'] == 0, 'ทุกข้อความที่ส่งยาวไม่เกิน 20 ไบต์')
        ok('หุ่นได้รับ %d คำสั่งแล้ว' % len(FULL.split()) in await pg.text_content('#btStatus'), 'แจ้งว่าหุ่นได้รับกี่คำสั่ง', await pg.text_content('#btStatus'))
        await pg.click('#btGo'); await pg.wait_for_timeout(300)
        ok('กำลังทำคำสั่งที่' in await pg.text_content('#btStatus'), 'ระหว่างหุ่นวิ่ง บอกว่ากำลังทำคำสั่งที่เท่าไร', await pg.text_content('#btStatus'))
        ok(await pg.evaluate('lit') is not None, 'ระหว่างหุ่นวิ่ง ไฮไลต์บล็อกที่หุ่นกำลังทำ')
        await pg.wait_for_timeout(1600)
        ok('12.3 วินาที' in await pg.text_content('#btStatus'), 'หุ่นวิ่งจบ แสดงเวลาจากหุ่น', await pg.text_content('#btStatus'))
        await pg.fill('#textIn', 'F40'); await pg.click('#textApply'); await pg.wait_for_timeout(400)
        ok('ชุดเก่า' in await pg.text_content('#btStatus'), 'แก้บล็อกหลังส่ง เตือนว่าโปรแกรมในหุ่นยังเป็นชุดเก่า', await pg.text_content('#btStatus'))
        await pg.click('#btStop'); await pg.wait_for_timeout(200)
        ok(await pg.evaluate("window.__robot.log.includes('X')"), 'ปุ่มหยุดส่ง X ไปหุ่น')
        # หุ่นถูกกด UP ตอนเว็บเพิ่งต่อใหม่ (เว็บไม่รู้ว่าในหุ่นมีกี่คำสั่ง) ต้องไม่ error
        await pg.evaluate("window.__robot.steps = ['F33','R']")
        await pg.click('#btConnect'); await pg.wait_for_timeout(300)
        await pg.evaluate("fromRobot('RUN'); fromRobot('S1')")
        ok('กำลังทำคำสั่งที่ 2' in await pg.text_content('#btStatus'), 'หุ่นวิ่งจากปุ่ม UP ก็แสดงขั้นที่กำลังทำ', await pg.text_content('#btStatus'))
        await pg.evaluate("fromRobot('STOP'); fromRobot('NOPROG')")
        ok('ยังไม่มีโปรแกรม' in await pg.text_content('#btStatus'), 'หุ่นไม่มีโปรแกรมแล้วกดวิ่ง เว็บบอกให้ส่งก่อน')

        # มือถือ
        m = await b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        await m.goto(URL + '?p=' + FULL.replace(' ', '+')); await m.wait_for_timeout(600)
        await m.click('#skip'); await m.wait_for_timeout(200)
        await m.screenshot(path='/home/claude/qb-build/mobile.png', full_page=True)
        ok(await m.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'จอมือถือไม่มีแถบเลื่อนแนวนอน')

        ok(not errors, 'ไม่มี error ในหน้าเว็บ', errors)
        await b.close()
    print('\n%d ผ่าน, %d ไม่ผ่าน' % (passed, failed))
    sys.exit(1 if failed else 0)

asyncio.run(main())

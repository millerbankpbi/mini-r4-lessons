# ทดสอบแดชบอร์ดกรรมการ Quick Dun Dun ด้วยเบราว์เซอร์จริง (Playwright)
# วิธีรัน: ในโฟลเดอร์ quickbox เปิด  python3 -m http.server 8765  แล้ว  QDD_PASS=รหัสผ่าน python3 dashboard/test_dashboard.py
import asyncio, sys, os
from playwright.async_api import async_playwright

URL = 'http://localhost:8765/dashboard/index.html'
PASSWORD = os.environ.get('QDD_PASS')   # รหัสผ่านจริงไม่เก็บในไฟล์นี้: QDD_PASS=รหัสผ่าน python3 dashboard/test_dashboard.py
if not PASSWORD: sys.exit('ตั้งรหัสผ่านก่อน: QDD_PASS=รหัสผ่าน python3 dashboard/test_dashboard.py')
passed = failed = 0
def ok(cond, name, extra=''):
    global passed, failed
    if cond: passed += 1; print('ผ่าน  ' + name)
    else: failed += 1; print('ไม่ผ่าน  ' + name + ('  → ' + str(extra) if extra else ''))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 1366, 'height': 860}, accept_downloads=True)
        await ctx.route('**/fonts.googleapis.com/**', lambda r: r.abort())
        pg = await ctx.new_page()
        errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))
        dialogs = []
        async def on_dialog(d):
            dialogs.append(d.message); await d.accept()
        pg.on('dialog', lambda d: asyncio.ensure_future(on_dialog(d)))
        text = lambda sel: pg.text_content(sel)

        # ---------- รหัสผ่าน ----------
        await pg.goto(URL); await pg.evaluate('localStorage.clear(); sessionStorage.clear()'); await pg.reload()
        ok(await pg.is_visible('#gate') and not await pg.is_visible('#app'), 'เปิดมาต้องใส่รหัสก่อน ไม่เห็นแดชบอร์ด')
        src = await (await pg.request.get(URL)).text()
        ok(PASSWORD not in src, 'ในโค้ดหน้าเว็บไม่มีรหัสผ่านตัวจริง')
        await pg.fill('#pw', 'abc123'); await pg.click('#loginForm button'); await pg.wait_for_timeout(200)
        ok(await text('#pwErr') == 'รหัสผ่านไม่ถูกต้อง' and not await pg.is_visible('#app'), 'รหัสผิด เข้าไม่ได้')
        await pg.fill('#pw', PASSWORD); await pg.press('#pw', 'Enter'); await pg.wait_for_timeout(200)
        ok(await pg.is_visible('#app') and not await pg.is_visible('#gate'), 'รหัสถูก เข้าแดชบอร์ดได้')
        await pg.reload(); await pg.wait_for_timeout(300)
        ok(await pg.is_visible('#app'), 'รีเฟรชหน้า (แท็บเดิม) ไม่ต้องใส่รหัสใหม่')

        # ---------- ทีม ----------
        ok('ยังไม่มีทีม' in await text('#rows'), 'ยังไม่มีทีม: ตารางบอกให้เพิ่มทีม')
        await pg.fill('#teamIn', 'ทีมหมาป่า'); await pg.click('#addForm button')
        await pg.fill('#teamIn', '  ทีมหมาป่า '); await pg.click('#addForm button'); await pg.wait_for_timeout(100)
        ok(await pg.evaluate('data.teams.length') == 1 and 'มีทีมชื่อ' in await text('#toast'), 'ชื่อทีมซ้ำ เพิ่มไม่ได้')
        await pg.click('#bulkToggle')
        await pg.fill('#bulkIn', 'ทีมเสือ\nทีมนกฮูก\n\nทีมหมาป่า\nทีมจระเข้')
        await pg.click('#bulkAdd'); await pg.wait_for_timeout(100)
        names = await pg.evaluate('data.teams.map((t) => t.name)')
        ok(names == ['ทีมหมาป่า', 'ทีมเสือ', 'ทีมนกฮูก', 'ทีมจระเข้'], 'วางรายชื่อหลายทีม: ข้ามบรรทัดว่างและชื่อซ้ำ', names)
        ok('4 ทีม · แข่งแล้ว 0 · รอแข่ง 4' in await text('#teamCount'), 'นับจำนวนทีม แข่งแล้ว/รอแข่ง')

        # ---------- สุ่มทีม ----------
        await pg.click('#spinBtn'); await pg.wait_for_timeout(150)
        ok(await pg.is_disabled('#spinBtn') and 'กำลังสุ่ม' in await text('#curInfo'), 'ระหว่างสุ่ม ชื่อทีมหมุน ปุ่มสุ่มกดซ้ำไม่ได้')
        await pg.wait_for_timeout(3500)
        cur = await pg.evaluate('current() && current().name')
        ok(cur in names and await text('#curName') == cur, 'สุ่มเสร็จ ได้ 1 ทีมขึ้นจอใหญ่', cur)
        ok('กำลังแข่ง' in await pg.text_content('tr.current'), 'ทีมที่สุ่มได้ ไฮไลต์ในตาราง')

        # ---------- จับเวลา ----------
        await pg.click('body', position={'x': 5, 'y': 5})
        await pg.keyboard.press('Space'); await pg.wait_for_timeout(1300)
        ok(await pg.evaluate('running') and await pg.is_disabled('#spinBtn'), 'กด Space เริ่มจับเวลา (ระหว่างนั้นสุ่มทีมไม่ได้)')
        await pg.keyboard.press('Space'); await pg.wait_for_timeout(100)
        ms = await pg.evaluate('elapsed')
        tin = await pg.input_value('#timeIn')
        ok(not await pg.evaluate('running') and 1200 < ms < 1700 and tin.startswith('00:01.'), 'กด Space อีกครั้ง หยุดเวลา แล้วเวลาเข้าไปที่ช่องบันทึกผลเอง', (ms, tin))
        ok('หยุดเวลา' in await text('#toast'), 'หยุดเวลาแล้วบอกให้ใส่คะแนน')
        # Space ตอนพิมพ์ในช่อง ไม่เริ่มนาฬิกา
        await pg.click('#teamIn'); await pg.keyboard.press('Space'); await pg.wait_for_timeout(100)
        ok(not await pg.evaluate('running'), 'พิมพ์ในช่องข้อความ กด Space ไม่ไปเริ่มนาฬิกา')
        await pg.fill('#teamIn', '')
        # ปุ่มก็ใช้ได้
        await pg.click('#startStop'); await pg.wait_for_timeout(300)
        ok('หยุดเวลา' in await text('#startStop'), 'ปุ่มเริ่มกลายเป็นปุ่มหยุดเวลาสีแดง')
        await pg.click('#startStop'); await pg.wait_for_timeout(100)
        ok(await pg.evaluate('elapsed') > ms, 'จับเวลาต่อจากเดิมได้')

        # ---------- คะแนน ----------
        await pg.click('.tog[data-k="zone"][data-n="2"]'); await pg.click('.tog[data-k="can"][data-n="2"]')
        ok(await pg.input_value('#scoreIn') == '50', 'ตัวช่วยคิดคะแนน: ถึงช่อง 2 + ดันกระป๋อง 2 = 50 (ออกตัวให้เอง)', await pg.input_value('#scoreIn'))
        for n in range(3, 9):
            await pg.click('.tog[data-k="zone"][data-n="%d"]' % n); await pg.click('.tog[data-k="can"][data-n="%d"]' % n)
        ok(await pg.input_value('#scoreIn') == '200' and 'ได้โบนัส' in await text('#padBonus'), 'ครบทุกช่องทุกกระป๋อง ได้ 200 พร้อมโบนัส')
        await pg.click('.tog[data-k="can"][data-n="8"]')
        ok(await pg.input_value('#scoreIn') == '160', 'เอากระป๋องช่อง 8 ออก เหลือ 160 (ไม่มีโบนัส)', await pg.input_value('#scoreIn'))
        await pg.fill('#timeIn', '41.27')
        await pg.click('#saveBtn'); await pg.wait_for_timeout(100)
        r = await pg.evaluate('current().result')
        ok(r['score'] == 160 and r['ms'] == 41270 and len(r['parts']['cans']) == 6, 'บันทึกผล: คะแนน เวลาที่พิมพ์แก้ และรายละเอียดคะแนน เข้าไปที่ทีมนั้น', r)
        ok('อันดับ 1' in await text('#savedNote'), 'บันทึกแล้วบอกอันดับ', await text('#savedNote'))
        first = cur

        # ทีมต่อไป: เลือกจากตาราง แล้วพิมพ์คะแนนเอง
        others = [n for n in names if n != first]
        await pg.click('tr:has-text("%s") button[data-a="pick"]' % others[0]); await pg.wait_for_timeout(100)
        ok(await text('#curName') == others[0] and await pg.input_value('#timeIn') == '' and await pg.evaluate('elapsed') == 0,
           'กดเลือกทีมจากตาราง: นาฬิกาและช่องบันทึกผลเริ่มใหม่')
        await pg.fill('#timeIn', '1:05.5'); await pg.fill('#scoreIn', '160'); await pg.click('#saveBtn'); await pg.wait_for_timeout(100)
        r2 = await pg.evaluate('byId(data.currentId).result')
        ok(r2['ms'] == 65500 and r2['parts'] is None, 'พิมพ์เวลา 1:05.5 = 65.5 วินาที และพิมพ์คะแนนเองได้', r2)
        ranks = await pg.evaluate("[...document.querySelectorAll('#rows tr')].map((tr) => tr.querySelector('.rank').textContent + ' ' + tr.querySelector('.name, td:nth-child(2)').textContent)")
        ok(ranks[0].startswith('1 ' + first) and ranks[1].startswith('2 ' + others[0]), 'คะแนนเท่ากัน เวลาน้อยกว่าได้อันดับดีกว่า', ranks)

        # ผิดพลาด
        await pg.click('tr:has-text("%s") button[data-a="pick"]' % others[1]); await pg.wait_for_timeout(100)
        await pg.fill('#timeIn', 'abc'); await pg.fill('#scoreIn', '10'); await pg.click('#saveBtn')
        ok('เวลาไม่ถูกต้อง' in await text('#saveErr'), 'พิมพ์เวลาผิดรูปแบบ แจ้งวิธีพิมพ์')
        await pg.fill('#timeIn', '30'); await pg.fill('#scoreIn', ''); await pg.click('#saveBtn')
        ok('ใส่คะแนน' in await text('#saveErr'), 'ไม่ใส่คะแนน แจ้งให้ใส่')
        await pg.fill('#scoreIn', '160'); await pg.fill('#timeIn', '41.27'); await pg.click('#saveBtn'); await pg.wait_for_timeout(100)
        ok(await pg.evaluate("ranked().ranks.get(data.currentId)") == 1, 'คะแนนและเวลาเท่ากันทุกอย่าง ได้อันดับร่วม')

        # บันทึกทับ ต้องถาม
        dialogs.clear()
        await pg.fill('#scoreIn', '170'); await pg.click('#saveBtn'); await pg.wait_for_timeout(200)
        ok(dialogs and 'บันทึกทับ' in dialogs[-1] and await pg.evaluate('current().result.score') == 170, 'ทีมที่มีผลแล้ว บันทึกใหม่ต้องถามก่อนทับ')

        # ---------- แก้ไขในตาราง ----------
        await pg.click('tr:has-text("%s") button[data-a="edit"]' % first)
        await pg.fill('tr.editing input[data-f="time"]', '00:39.90')
        await pg.fill('tr.editing input[data-f="name"]', 'ทีมดาวเหนือ')
        await pg.click('button[data-a="ok"]'); await pg.wait_for_timeout(100)
        t1 = await pg.evaluate("data.teams.find((t) => t.name === 'ทีมดาวเหนือ')")
        ok(t1 and t1['result']['ms'] == 39900 and t1['result']['edited'], 'แก้ไขชื่อทีมและพิมพ์เวลาใหม่ในตารางได้', t1)
        await pg.click('tr:has-text("ทีมดาวเหนือ") button[data-a="edit"]')
        await pg.fill('tr.editing input[data-f="time"]', '9:99')
        await pg.press('tr.editing input[data-f="time"]', 'Enter'); await pg.wait_for_timeout(100)
        ok('เวลาไม่ถูกต้อง' in await text('#toast') and await pg.evaluate("data.teams.find((t) => t.name === 'ทีมดาวเหนือ').result.ms") == 39900,
           'แก้เวลาผิดรูปแบบ (9:99) ไม่ยอมบันทึก')
        await pg.keyboard.press('Escape')

        # ---------- CSV ----------
        async with pg.expect_download() as dl:
            await pg.click('#csvBtn')
        d = await dl.value
        path = await d.path()
        raw = open(path, 'rb').read()
        csv = raw.decode('utf-8-sig')
        lines = csv.strip().split('\r\n')
        ok(raw.startswith(b'\xef\xbb\xbf'), 'CSV มี BOM ให้ Excel อ่านภาษาไทยได้')
        ok(d.suggested_filename.startswith('quick-dun-dun-') and d.suggested_filename.endswith('.csv'), 'ชื่อไฟล์ CSV มีวันที่', d.suggested_filename)
        ok(lines[0].startswith('อันดับ,ทีม,คะแนน,เวลา') and len(lines) == 5, 'CSV มีหัวตารางและครบทุกทีม', lines)
        ok(any(l.startswith('2,ทีมดาวเหนือ,160,00:39.90,39.90') for l in lines), 'CSV: อันดับ ทีม คะแนน เวลา ตรงกับตาราง', lines)
        ok(any('ยังไม่แข่ง' in l for l in lines), 'CSV: ทีมที่ยังไม่แข่งก็อยู่ในไฟล์')

        # ---------- จำข้อมูล ----------
        await pg.reload(); await pg.wait_for_timeout(300)
        ok(await pg.evaluate('data.teams.filter((t) => t.result).length') == 3, 'รีเฟรชหน้าแล้วผลแข่งยังอยู่')

        # ---------- สุ่มทีมเฉพาะที่ยังไม่แข่ง ----------
        left = await pg.evaluate("data.teams.filter((t) => !t.result).map((t) => t.name)")
        await pg.emulate_media(reduced_motion='reduce')
        await pg.click('#spinBtn'); await pg.wait_for_timeout(200)
        ok(await pg.evaluate('current().name') in left and len(left) == 1, 'สุ่มเฉพาะทีมที่ยังไม่ได้แข่ง', left)
        await pg.evaluate("current().result = { score: 1, ms: 1000, parts: null, at: new Date().toISOString() }; save(); render()")
        await pg.click('#spinBtn'); await pg.wait_for_timeout(200)
        ok('ครบแล้ว' in await text('#toast'), 'ทุกทีมแข่งครบ กดสุ่มแล้วบอกว่าครบแล้ว')

        # ---------- ลบ / ล้าง ----------
        await pg.click('tr:has-text("ทีมจระเข้") button[data-a="del"]'); await pg.wait_for_timeout(200)
        ok(await pg.evaluate("!data.teams.some((t) => t.name === 'ทีมจระเข้')"), 'ลบทีมได้ (ถามยืนยันก่อน)')
        await pg.click('#clearResults'); await pg.wait_for_timeout(200)
        ok(await pg.evaluate('data.teams.length') == 3 and await pg.evaluate('data.teams.every((t) => !t.result)'), 'ล้างผลทั้งหมด ชื่อทีมยังอยู่')

        # ---------- ล็อก ----------
        await pg.click('#lockBtn'); await pg.wait_for_timeout(100)
        ok(await pg.is_visible('#gate') and not await pg.is_visible('#app'), 'กดล็อกหน้าจอ กลับไปหน้าใส่รหัส')
        await pg.reload(); await pg.wait_for_timeout(200)
        ok(await pg.is_visible('#gate'), 'ล็อกแล้วรีเฟรช ยังต้องใส่รหัส')
        await pg.keyboard.press('Space'); await pg.wait_for_timeout(100)
        ok(not await pg.evaluate('running'), 'หน้าใส่รหัส กด Space ไม่ไปเริ่มนาฬิกา')

        # ---------- จอเล็ก ----------
        m = await b.new_page(viewport={'width': 390, 'height': 844})
        await m.goto(URL); await m.fill('#pw', PASSWORD); await m.press('#pw', 'Enter'); await m.wait_for_timeout(300)
        await m.evaluate("addTeams(['ทีมหมาป่าสายฟ้าแลบ', 'ทีมเสือ', 'ทีมนกฮูก']); data.teams[1].result = { score: 160, ms: 41270, parts: null, at: new Date().toISOString() }; data.currentId = data.teams[0].id; save(); render()")
        await m.wait_for_timeout(200)
        ok(await m.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'มือถือ: มีทีมในตารางแล้วก็ไม่มีแถบเลื่อนแนวนอน',
           await m.evaluate('document.documentElement.scrollWidth'))
        await m.click('#rows tr:first-child button[data-a="edit"]'); await m.wait_for_timeout(100)
        ok(await m.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'มือถือ: ตอนแก้ไขแถวก็ไม่ล้นจอ')

        ok(not errors, 'ไม่มี error ในหน้าเว็บ', errors)
        await b.close()
    print('\n%d ผ่าน, %d ไม่ผ่าน' % (passed, failed))
    sys.exit(1 if failed else 0)

asyncio.run(main())

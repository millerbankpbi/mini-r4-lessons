# ทดสอบแดชบอร์ดกรรมการ 2 (แข่งหลายรอบ) ด้วยเบราว์เซอร์จริง (Playwright)
# วิธีรัน: ในโฟลเดอร์ quickbox เปิด  python3 -m http.server 8765  แล้ว  QDD_PASS=รหัสผ่าน python3 dashboard2/test_dashboard2.py
import asyncio, sys, os, csv, io
from playwright.async_api import async_playwright

URL = 'http://localhost:8765/dashboard2/index.html'
PASSWORD = os.environ.get('QDD_PASS')   # รหัสผ่านจริงไม่เก็บในไฟล์นี้
if not PASSWORD: sys.exit('ตั้งรหัสผ่านก่อน: QDD_PASS=รหัสผ่าน python3 dashboard2/test_dashboard2.py')
passed = failed = 0
def ok(cond, name, extra=''):
    global passed, failed
    if cond: passed += 1; print('ผ่าน  ' + name)
    else: failed += 1; print('ไม่ผ่าน  ' + name + ('  → ' + str(extra) if extra else ''))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        # ลดการเคลื่อนไหว: สุ่มทีมเสร็จทันที ทดสอบสุ่มหลายครั้งได้เร็ว
        ctx = await b.new_context(viewport={'width': 1366, 'height': 900}, accept_downloads=True, reduced_motion='reduce')
        await ctx.route('**/fonts.googleapis.com/**', lambda r: r.abort())
        pg = await ctx.new_page()
        errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))
        dialogs = []
        answer = {'v': True}
        async def on_dialog(d):
            dialogs.append(d.message)
            await (d.accept() if answer['v'] else d.dismiss())
        pg.on('dialog', lambda d: asyncio.ensure_future(on_dialog(d)))
        text = lambda sel: pg.text_content(sel)
        ev = pg.evaluate

        # ---------- รหัสผ่าน ----------
        await pg.goto(URL); await ev('localStorage.clear(); sessionStorage.clear()'); await pg.reload()
        ok(await pg.is_visible('#gate') and not await pg.is_visible('#app'), 'เปิดมาต้องใส่รหัสก่อน')
        src = await (await pg.request.get(URL)).text()
        ok(PASSWORD not in src, 'ในโค้ดหน้าเว็บไม่มีรหัสผ่านตัวจริง')
        await pg.fill('#pw', 'abc123'); await pg.click('#loginForm button'); await pg.wait_for_timeout(200)
        ok(not await pg.is_visible('#app'), 'รหัสผิด เข้าไม่ได้')
        await pg.fill('#pw', PASSWORD); await pg.press('#pw', 'Enter'); await pg.wait_for_timeout(200)
        ok(await pg.is_visible('#app'), 'รหัสถูก (ชุดเดียวกับแดชบอร์ดเดิม) เข้าได้')

        # ---------- ค่าเริ่มต้น 2 รอบ ----------
        rb = await ev("[...document.querySelectorAll('#roundBtns button')].map((b) => b.textContent + ':' + b.getAttribute('aria-pressed'))")
        ok(rb == ['รอบที่ 1:true', 'รอบที่ 2:false'], 'เริ่มต้น 2 รอบ อยู่ที่รอบ 1', rb)
        head = await text('#headRow')
        ok('รอบ 1 (กำลังแข่ง)' in head and 'รอบ 2' in head and 'ดีที่สุด' in head, 'หัวตารางมีรอบ 1 รอบ 2 และคอลัมน์ดีที่สุด', head)

        # ---------- ทีม ----------
        await pg.click('#bulkToggle'); await pg.fill('#bulkIn', 'ทีมเสือ\nทีมนกฮูก\n\nทีมหมาป่า\nทีมจระเข้\nทีมเสือ'); await pg.click('#bulkAdd'); await pg.wait_for_timeout(100)
        names = await ev('data.teams.map((t) => t.name)')
        ok(names == ['ทีมเสือ', 'ทีมนกฮูก', 'ทีมหมาป่า', 'ทีมจระเข้'], 'วางรายชื่อหลายทีม ข้ามบรรทัดว่างและชื่อซ้ำ', names)
        ok('รอบ 1 แข่งแล้ว 0/4 ทีม' in await text('#roundProg'), 'จอใหญ่บอกความคืบหน้าของรอบ', await text('#roundProg'))

        # ---------- เลือกทีมเองแบบเจาะจง ----------
        opts = await ev("[...document.querySelectorAll('#pickSel optgroup')].map((g) => g.label + '=' + g.children.length)")
        ok(opts == ['ยังไม่แข่งรอบ 1=4'], 'รายการเลือกทีมเอง แยกกลุ่มยังไม่แข่งรอบนี้', opts)
        nok = await ev("data.teams[1].id")
        await pg.select_option('#pickSel', nok); await pg.wait_for_timeout(100)
        ok(await ev('current() && current().name') == 'ทีมนกฮูก' and await text('#curName') == 'ทีมนกฮูก', 'เลือกทีมเองจากรายการ ขึ้นจอใหญ่')
        ok(await ev("document.activeElement !== $('pickSel')") and await ev("$('pickSel').value") == '', 'เลือกแล้วรายการกลับเป็นค่าว่าง กด Space ต่อได้')
        ok('รอบ 1' in await text('#forTeam') and 'บันทึกผลรอบ 1 ให้ทีม ทีมนกฮูก' == await text('#saveBtn'), 'ช่องบันทึกผลบอกทีมและรอบ')

        # ---------- จับเวลา + บันทึกรอบ 1 ----------
        await pg.keyboard.press('Space'); await pg.wait_for_timeout(400)
        ok(await ev('running'), 'Space เริ่มจับเวลา (หลังเลือกทีมจากรายการ)')
        ok(await pg.is_disabled('#pickSel') and await pg.is_disabled('#roundBtns button'), 'ระหว่างจับเวลา เปลี่ยนทีม/รอบไม่ได้')
        await pg.keyboard.press('Space'); await pg.wait_for_timeout(100)
        t1 = await pg.input_value('#timeIn')
        ok(not await ev('running') and t1.startswith('00:00.'), 'Space หยุด เวลาเข้าช่องบันทึกผล', t1)
        await pg.click('.tog[data-k="zone"][data-n="2"]'); await pg.click('.tog[data-k="cube"][data-n="2"]')
        ok(await pg.input_value('#scoreIn') == '50', 'ตัวช่วยคิดคะแนน: ออกตัว+ช่อง 2+ลูกบาศก์ 2 = 50')
        await pg.fill('#timeIn', '30.00'); await pg.click('#saveBtn'); await pg.wait_for_timeout(100)
        r1 = await ev('current().results[1]')
        ok(r1 and r1['score'] == 50 and r1['ms'] == 30000 and r1['parts']['cubes'] == [2], 'บันทึกผลลงรอบ 1', r1)
        ok('รอบ 1 ได้ 50 คะแนน 00:30.00' in await text('#savedNote'), 'ข้อความยืนยันบอกรอบ', await text('#savedNote'))
        ok('ยังไม่แข่ง' in await text('#curChips') and 'ดีที่สุด: รอบ 1' in await text('#curChips'), 'จอใหญ่โชว์ผลแต่ละรอบและผลดีที่สุด', await text('#curChips'))

        # ---------- สุ่มเฉพาะทีมที่ยังไม่แข่งรอบนี้ ----------
        await ev("for (const n of ['ทีมเสือ', 'ทีมหมาป่า']) { const t = data.teams.find((x) => x.name === n); t.results[1] = { score: 70, ms: 40000, parts: null, at: new Date().toISOString() }; } save(); render()")
        picks = set()
        for _ in range(6):
            await pg.click('#spinBtn'); await pg.wait_for_timeout(60)
            picks.add(await ev('current().name'))
        ok(picks == {'ทีมจระเข้'}, 'สุ่มรอบ 1: ได้เฉพาะทีมที่ยังไม่แข่งรอบ 1', picks)
        await ev("current().results[1] = { score: 30, ms: 20000, parts: null, at: new Date().toISOString() }; save(); render()")
        dialogs.clear()
        await pg.click('#spinBtn'); await pg.wait_for_timeout(300)
        ok(any('ครบแล้ว ไปรอบที่ 2' in d for d in dialogs) and await ev('data.round') == 2, 'ครบทุกทีมรอบ 1 กดสุ่ม ถามแล้วไปรอบ 2 ให้', dialogs)
        ok(await ev('current() && !current().results[2]'), 'ไปรอบ 2 แล้วสุ่มทีมให้ทันที')
        ok('รอบ 2 (กำลังแข่ง)' in await text('#headRow') and await ev("document.querySelector('#roundBtns [data-r=\"2\"]').getAttribute('aria-pressed')") == 'true', 'ปุ่มรอบและหัวตารางเปลี่ยนเป็นรอบ 2')
        picks2 = set()
        await ev("data.teams.find((x) => x.name === 'ทีมเสือ').results[2] = { score: 100, ms: 50000, parts: null, at: new Date().toISOString() }; save(); render()")
        for _ in range(12):
            await pg.click('#spinBtn'); await pg.wait_for_timeout(50)
            picks2.add(await ev('current().name'))
        ok('ทีมเสือ' not in picks2 and len(picks2) >= 2, 'สุ่มรอบ 2: ไม่ซ้ำทีมที่แข่งรอบ 2 แล้ว', picks2)

        # ---------- ผลดีที่สุด ----------
        async def save_r2(name, score, time):
            tid = await ev("data.teams.find((x) => x.name === '%s').id" % name)
            await ev("setCurrent('%s')" % tid)
            await pg.fill('#scoreIn', str(score)); await pg.fill('#timeIn', time); await pg.click('#saveBtn'); await pg.wait_for_timeout(80)
        await save_r2('ทีมนกฮูก', 110, '45.00')      # ดีกว่ารอบ 1
        ok(await ev("bestOf(data.teams.find((x) => x.name === 'ทีมนกฮูก')).round") == 2, 'รอบ 2 คะแนนมากกว่า ผลดีที่สุดเป็นรอบ 2')
        ok('ผลดีที่สุดคือรอบ 2 (110 คะแนน 00:45.00)' in await text('#savedNote'), 'ข้อความยืนยันบอกว่าผลดีที่สุดมาจากรอบไหน', await text('#savedNote'))
        ok('อันดับรอบ 2: 1' in await text('#savedNote'), 'ข้อความยืนยันบอกอันดับของรอบที่เพิ่งแข่งด้วย', await text('#savedNote'))
        await save_r2('ทีมหมาป่า', 40, '25.00')      # แย่กว่ารอบ 1
        bw = await ev("bestOf(data.teams.find((x) => x.name === 'ทีมหมาป่า'))")
        ok(bw['round'] == 1 and bw['score'] == 70, 'รอบ 2 คะแนนน้อยกว่า ผลดีที่สุดยังเป็นรอบ 1', bw)
        await save_r2('ทีมจระเข้', 30, '15.50')      # คะแนนเท่า เวลาน้อยกว่า
        ok(await ev("bestOf(data.teams.find((x) => x.name === 'ทีมจระเข้')).round") == 2, 'คะแนนเท่ากัน รอบที่เร็วกว่าเป็นผลดีที่สุด')
        same = await ev("(() => { const t = { results: { 1: { score: 60, ms: 30000 }, 2: { score: 60, ms: 30000 } } }; return bestOf(t).round; })()")
        ok(same == 1, 'คะแนนและเวลาเท่ากันทั้งคู่ ใช้รอบที่มาก่อน')

        # ---------- ตารางอันดับใช้ผลดีที่สุด ----------
        order = await ev("[...document.querySelectorAll('#rows tr')].map((tr) => tr.querySelector('.name').firstChild.textContent)")
        ok(order == ['ทีมนกฮูก', 'ทีมเสือ', 'ทีมหมาป่า', 'ทีมจระเข้'], 'เรียงอันดับตามผลดีที่สุด (110 > 100 > 70 > 30)', order)
        nrow = 'tr[data-id="%s"]' % await ev("data.teams.find((x) => x.name === 'ทีมนกฮูก').id")
        ok(await pg.text_content(nrow + ' td.best') == '110 รอบ 200:45.00', 'คอลัมน์ดีที่สุดโชว์คะแนน เวลา และป้ายรอบ', await pg.text_content(nrow + ' td.best'))
        stars = await ev("[...document.querySelectorAll('%s td.rd')].map((td) => td.classList.contains('isbest'))" % nrow)
        ok(stars == [False, True], 'ดาวอยู่ที่ช่องรอบที่ดีที่สุด', stars)
        ok(await ev("document.querySelectorAll('#rows tr:first-child td.rd.now').length") == 1, 'คอลัมน์รอบที่กำลังแข่งมีพื้นสีให้เห็น')

        # ---------- จัดอันดับเฉพาะรอบ 1 หรือรอบ 2 ----------
        names_now = "[...document.querySelectorAll('#rows tr')].map((tr) => tr.querySelector('.name').firstChild.textContent)"
        ranks_now = "[...document.querySelectorAll('#rows td.rank')].map((td) => td.textContent)"
        segs = await ev("[...document.querySelectorAll('#rankBy button')].map((b) => b.textContent + ':' + b.getAttribute('aria-pressed'))")
        ok(segs == ['ผลดีที่สุด:true', 'รอบ 1:false', 'รอบ 2:false'], 'มีปุ่มจัดอันดับตาม ผลดีที่สุด / รอบ 1 / รอบ 2 เริ่มที่ผลดีที่สุด', segs)
        await ev("data.teams.push({ id: 'xhorse', name: 'ทีมม้า', results: { 1: { score: 200, ms: 60000, parts: null, at: new Date().toISOString() } } }); save(); render()")
        await pg.click('#rankBy [data-v="1"]'); await pg.wait_for_timeout(80)
        o1, r1s = await ev(names_now), await ev(ranks_now)
        ok(o1 == ['ทีมม้า', 'ทีมเสือ', 'ทีมหมาป่า', 'ทีมนกฮูก', 'ทีมจระเข้'] and r1s == ['1', '2', '2', '4', '5'], 'จัดอันดับเฉพาะรอบ 1: ใช้คะแนนและเวลารอบ 1 อย่างเดียว เท่ากันได้อันดับร่วม', (o1, r1s))
        ok(await text('#boardMode') == 'อันดับรอบ 1' and (await text('#headRow th.rankcol')).startswith('รอบ 1'), 'หัวการ์ดและหัวคอลัมน์บอกว่าจัดอันดับจากรอบ 1')
        await pg.click('#rankBy [data-v="2"]'); await pg.wait_for_timeout(80)
        o2, r2s = await ev(names_now), await ev(ranks_now)
        ok(o2 == ['ทีมนกฮูก', 'ทีมเสือ', 'ทีมหมาป่า', 'ทีมจระเข้', 'ทีมม้า'] and r2s == ['1', '2', '3', '4', '–'], 'จัดอันดับเฉพาะรอบ 2: ทีมที่ยังไม่แข่งรอบ 2 อยู่ท้ายตาราง ไม่มีอันดับ', (o2, r2s))
        ok('ใช้ผลรอบ 2 อย่างเดียว' in await text('#rankNote'), 'คำอธิบายใต้ปุ่มเปลี่ยนตามแบบที่เลือก', await text('#rankNote'))
        await pg.reload(); await pg.wait_for_timeout(300)
        ok(await ev('data.rankBy') == 2 and await ev(names_now) == o2, 'รีเฟรชแล้วยังจัดอันดับตามรอบ 2')
        await pg.click('#rankBy [data-v="best"]'); await pg.wait_for_timeout(80)
        ok(await ev(names_now) == ['ทีมม้า', 'ทีมนกฮูก', 'ทีมเสือ', 'ทีมหมาป่า', 'ทีมจระเข้'], 'กลับมาจัดอันดับจากผลดีที่สุด', await ev(names_now))
        await ev("data.teams = data.teams.filter((x) => x.id !== 'xhorse'); save(); render()")
        tid = await ev("data.teams.find((x) => x.name === 'ทีมนกฮูก').id")
        await ev("setCurrent('%s')" % tid)

        # ---------- บันทึกทับต้องยืนยัน ----------
        answer['v'] = False; dialogs.clear()
        await save_r2('ทีมนกฮูก', 5, '10.00')
        ok(any('มีผลรอบ 2 อยู่แล้ว' in d for d in dialogs) and await ev("data.teams.find((x) => x.name === 'ทีมนกฮูก').results[2].score") == 110, 'บันทึกทับรอบเดิมต้องยืนยัน กดยกเลิกผลเดิมอยู่')
        answer['v'] = True

        # ---------- เปลี่ยนรอบ ----------
        await pg.click('#roundBtns [data-r="1"]'); await pg.wait_for_timeout(80)
        ok(await ev('data.round') == 1 and 'รอบ 1' in await text('#curLabel'), 'กดปุ่มรอบที่ 1 กลับไปรอบ 1 ได้')
        await pg.keyboard.press('Space'); await pg.wait_for_timeout(100)
        await ev("setRound(2)"); await pg.wait_for_timeout(50)
        ok(await ev('data.round') == 1, 'นาฬิกาเดินอยู่ เปลี่ยนรอบไม่ได้')
        await pg.keyboard.press('Space'); await pg.wait_for_timeout(50)
        await pg.click('#roundBtns [data-r="2"]'); await pg.wait_for_timeout(80)
        ok(await ev('data.round') == 2 and await pg.input_value('#timeIn') == '', 'หยุดแล้วเปลี่ยนรอบได้ ช่องเวลาเคลียร์ให้')

        # ---------- แก้ไขในตาราง ----------
        await pg.click(nrow + ' button[data-a="edit"]'); await pg.wait_for_timeout(80)
        await pg.fill(nrow + ' [data-f="s2"]', '120'); await pg.press(nrow + ' [data-f="s2"]', 'Enter'); await pg.wait_for_timeout(80)
        r2 = await ev("data.teams.find((x) => x.name === 'ทีมนกฮูก').results[2]")
        ok(r2['score'] == 120 and r2['ms'] == 45000 and r2['edited'], 'แก้คะแนนรอบ 2 ในตารางได้ เวลาเดิมอยู่', r2)
        await pg.click(nrow + ' button[data-a="edit"]'); await pg.wait_for_timeout(80)
        await pg.fill(nrow + ' [data-f="s2"]', ''); await pg.fill(nrow + ' [data-f="t2"]', ''); dialogs.clear()
        await pg.click(nrow + ' button[data-a="ok"]'); await pg.wait_for_timeout(80)
        ok(any('ลบผลรอบ 2' in d for d in dialogs) and await ev("!data.teams.find((x) => x.name === 'ทีมนกฮูก').results[2]"), 'ลบช่องรอบ 2 ให้ว่าง = ลบผลรอบนั้น (ถามก่อน)')
        ok(await ev("bestOf(data.teams.find((x) => x.name === 'ทีมนกฮูก')).round") == 1, 'ลบผลรอบ 2 แล้ว ผลดีที่สุดกลับเป็นรอบ 1')
        await pg.click(nrow + ' button[data-a="edit"]'); await pg.wait_for_timeout(80)
        await pg.fill(nrow + ' [data-f="t1"]', '1:75'); await pg.click(nrow + ' button[data-a="ok"]'); await pg.wait_for_timeout(80)
        ok('เวลารอบ 1 ไม่ถูกต้อง' in await text('#toast') and await ev('editing') is not None, 'เวลาผิดรูปแบบ แก้ไม่ผ่าน บอกว่ารอบไหน')
        await pg.press(nrow + ' [data-f="t1"]', 'Escape'); await pg.wait_for_timeout(50)

        # ---------- จำนวนรอบ ----------
        await pg.select_option('#roundsSel', '3'); await pg.wait_for_timeout(80)
        ok(await ev("document.querySelectorAll('#roundBtns button').length") == 3 and 'รอบ 3' in await text('#headRow'), 'ตั้ง 3 รอบได้')
        ok(await ev("document.querySelectorAll('#rankBy button').length") == 4, '3 รอบ: ปุ่มจัดอันดับมีรอบ 3 เพิ่ม')
        await pg.click('#rankBy [data-v="3"]'); await pg.wait_for_timeout(50)
        await pg.select_option('#roundsSel', '1'); await pg.wait_for_timeout(80)
        ok(await ev('data.rounds') == 3 and 'ลบผลรอบนั้นก่อน' in await text('#toast'), 'มีผลรอบ 2 อยู่ ลดเหลือ 1 รอบไม่ได้ (กันผลหาย)')
        await pg.select_option('#roundsSel', '2'); await pg.wait_for_timeout(80)
        ok(await ev('data.rounds') == 2, 'กลับเป็น 2 รอบ')
        ok(await ev('data.rankBy') == 'best' and await text('#boardMode') == 'อันดับผลดีที่สุด', 'ลดเหลือ 2 รอบตอนดูอันดับรอบ 3 อยู่ กลับไปใช้ผลดีที่สุดเอง')

        # ---------- เก็บข้อมูลข้ามการรีเฟรช ----------
        before = await ev('JSON.stringify([data.round, data.rounds, data.teams.map((t) => [t.name, t.results])])')
        await pg.reload(); await pg.wait_for_timeout(300)
        ok(await ev('JSON.stringify([data.round, data.rounds, data.teams.map((t) => [t.name, t.results])])') == before, 'รีเฟรชแล้วรอบและผลทุกรอบยังอยู่')

        # ---------- CSV ----------
        async with pg.expect_download() as dl:
            await pg.click('#csvBtn')
        d = await dl.value
        raw = open(await d.path(), encoding='utf-8-sig').read()
        rows = list(csv.reader(io.StringIO(raw)))
        ok(rows[0][:12] == ['อันดับ (ผลดีที่สุด)', 'อันดับรอบ 1', 'อันดับรอบ 2', 'ทีม', 'รอบ 1 คะแนน', 'รอบ 1 เวลา', 'รอบ 2 คะแนน', 'รอบ 2 เวลา', 'ดีที่สุด คะแนน', 'ดีที่สุด เวลา', 'ดีที่สุด เวลา (วินาที)', 'ดีที่สุดจากรอบ'], 'CSV: มีอันดับทั้ง 3 แบบ ผลทุกรอบ และผลดีที่สุด', rows[0])
        cro = next(r for r in rows if r[3] == 'ทีมจระเข้')
        ok(cro[:12] == ['4', '4', '3', 'ทีมจระเข้', '30', '00:20.00', '30', '00:15.50', '30', '00:15.50', '15.50', '2'], 'CSV: แถวทีมบอกอันดับแต่ละแบบ ผลแต่ละรอบ และดีที่สุดจากรอบ 2', cro)
        nok_row = next(r for r in rows if r[3] == 'ทีมนกฮูก')
        ok(nok_row[2] == '', 'CSV: ทีมที่ยังไม่มีผลรอบ 2 ช่องอันดับรอบ 2 ว่าง', nok_row)
        ok('2rounds' in d.suggested_filename and 'rank-best' in d.suggested_filename, 'ชื่อไฟล์ CSV บอกจำนวนรอบและแบบจัดอันดับ', d.suggested_filename)
        await pg.click('#rankBy [data-v="1"]'); await pg.wait_for_timeout(50)
        async with pg.expect_download() as dl1:
            await pg.click('#csvBtn')
        d1 = await dl1.value
        rows1 = list(csv.reader(io.StringIO(open(await d1.path(), encoding='utf-8-sig').read())))
        ok([r[3] for r in rows1[1:]] == ['ทีมเสือ', 'ทีมหมาป่า', 'ทีมนกฮูก', 'ทีมจระเข้'] and 'rank-round1' in d1.suggested_filename, 'CSV ตอนเลือกรอบ 1: เรียงแถวตามอันดับรอบ 1', [r[3] for r in rows1[1:]])
        await pg.click('#rankBy [data-v="best"]'); await pg.wait_for_timeout(50)

        # ---------- นำเข้าจากแดชบอร์ดเดิม ----------
        await ev("""localStorage.setItem('qdd-dashboard-v1', JSON.stringify({ currentId: null, teams: [
            { id: 'a', name: 'ทีมเสือ', result: null },
            { id: 'b', name: 'ทีมกระต่าย', result: { score: 90, ms: 22600, parts: { start: true, zones: [2, 3], cans: [2] }, at: new Date().toISOString() } },
            { id: 'c', name: 'ทีมแมว', result: null } ] })); render()""")
        await pg.wait_for_timeout(80)
        ok(await pg.is_visible('#importBox') and 'พบ 2 ทีม' in await text('#importText'), 'เห็นปุ่มนำเข้าทีมจากแดชบอร์ดเดิม (ไม่นับชื่อที่มีแล้ว)', await text('#importText'))
        await pg.click('#importBtn'); await pg.wait_for_timeout(80)
        rab = await ev("data.teams.find((x) => x.name === 'ทีมกระต่าย')")
        ok(len(await ev('data.teams')) == 6 and rab['results']['1']['score'] == 90 and rab['results']['1']['parts']['cubes'] == [2], 'นำเข้าแล้ว ผลเดิมเป็นรอบ 1', rab)
        ok(not await pg.is_visible('#importBox'), 'นำเข้าแล้วปุ่มนำเข้าหายไป')

        # ---------- ล็อก ----------
        await pg.click('#lockBtn'); await pg.wait_for_timeout(100)
        ok(await pg.is_visible('#gate'), 'กดล็อกหน้าจอ กลับไปหน้าใส่รหัส')

        # ---------- จอเล็ก ----------
        m = await b.new_page(viewport={'width': 390, 'height': 844})
        merr = []
        m.on('pageerror', lambda e: merr.append(str(e)))
        await m.route('**/fonts.googleapis.com/**', lambda r: r.abort())
        await m.goto(URL); await m.fill('#pw', PASSWORD); await m.press('#pw', 'Enter'); await m.wait_for_timeout(300)
        await m.evaluate("data.teams.push({ id: 'long1', name: 'ทีมหมาป่าสายฟ้าแลบแห่งสมุทรสาคร', results: {} }); data.currentId = 'long1'; save(); render()")
        await m.wait_for_timeout(200)
        ok(await m.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'มือถือ: ไม่มีแถบเลื่อนแนวนอน', await m.evaluate('document.documentElement.scrollWidth'))
        await m.click('#rows tr:first-child button[data-a="edit"]'); await m.wait_for_timeout(100)
        ok(await m.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'มือถือ: ตอนแก้ไขแถวก็ไม่ล้นจอ', await m.evaluate('document.documentElement.scrollWidth'))

        ok(not errors and not merr, 'ไม่มี error ในหน้าเว็บ', errors + merr)
        await b.close()
    print('\n%d ผ่าน, %d ไม่ผ่าน' % (passed, failed))
    sys.exit(1 if failed else 0)

asyncio.run(main())

// ทดสอบตัวจำลองและตัวนับคะแนน Quick Dun Dun:  node test-engine.js
const QB = require('./quickbox-engine.js');
let pass = 0, fail = 0;
function ok(cond, name, extra) {
  if (cond) { pass++; console.log('ผ่าน  ' + name); }
  else { fail++; console.log('ไม่ผ่าน  ' + name + (extra ? '  → ' + extra : '')); }
}
const run = (text) => QB.run(QB.parse(text)).result;

ok(QB.FULL === 200, 'คะแนนเต็มรวมได้ 200 (ออกตัว 30 + ช่องเขียว 70 + กระป๋อง 70 + โบนัส 30)', QB.FULL);

// โปรแกรมเป็นข้อความ
const steps = QB.parse('F30 R b20 L U S50');
ok(QB.toText(steps) === 'F30 R B20 L U S50', 'แปลงโปรแกรมไป-กลับได้ตรงกัน', QB.toText(steps));
for (const [bad, word] of [['F', 'ต้องมีตัวเลข'], ['R90', 'ไม่ต้องมีตัวเลข'], ['F500', 'ระหว่าง'], ['X3', 'ไม่รู้จัก'], ['S5', 'ระหว่าง']]) {
  let msg = '';
  try { QB.parse(bad); } catch (e) { msg = e.message; }
  ok(msg.includes(word), 'คำสั่งผิด "' + bad + '" แจ้งเตือนเป็นภาษาไทย', msg);
}

// จุดเริ่ม
const r0 = run('');
ok(r0.total === 0 && r0.touches === 0 && !r0.started, 'ยังไม่วิ่ง: 0 คะแนน ไม่แตะเส้น', JSON.stringify(r0.rows));
ok(!QB.FIELD.lines.some((q) => QB.robotHitsRect(QB.START, q)), 'จุดเริ่มในช่อง 1 ไม่ทับเส้นดำ');

// ออกตัว
const r1 = run('F33');
ok(r1.started && r1.total === 30, 'เดินหน้า 33 ซม. ออกจากช่อง 1 ได้ 30 คะแนน', r1.total);
const r1b = run('F5');
ok(!r1b.started && r1b.total === 0, 'เดินหน้าแค่ 5 ซม. ยังอยู่ในช่อง 1 ยังไม่ได้คะแนนออกตัว', r1b.total);

// ไปช่อง 2 แล้วดันกระป๋องตกขอบล่าง
const r2 = run('F33 R F30 R F32');
ok(r2.started && r2.visited.join() === '2' && r2.cansOut === 1 && r2.touches === 0 && r2.total === 50,
  'ช่อง 2: ออกตัว + ถึงช่อง 2 + ดันกระป๋องออก = 50 คะแนน ไม่แตะเส้น', JSON.stringify({ v: r2.visited, c: r2.cansOut, t: r2.touches, s: r2.total }));
const r2b = run('F33 R F30 R F12');
ok(r2b.cansOut === 0 && r2b.visited.length === 0, 'หยุดก่อนถึงกระป๋องช่อง 2: ยังไม่ได้คะแนนช่องและกระป๋อง', JSON.stringify(r2b.rows));

// แตะเส้นดำ
const r3 = run('F60');
ok(r3.touches === 1, 'เดินหน้า 60 ซม. ชนเส้นนอนซ้าย นับแตะเส้น 1 ครั้ง (ทับต่อเนื่องไม่นับซ้ำ)', r3.touches);
ok(r3.total === 30, 'แตะเส้นดำไม่หักคะแนน (ตามกติกาตอนนี้)', r3.total);
const ev = QB.run(QB.parse('F60')).events.find((e) => e.type === 'line');
ok(ev && /เส้นดำ/.test(ev.msg) && /ระยะ|เลี้ยว/.test(ev.msg), 'ข้อความแตะเส้นบอกวิธีแก้', ev && ev.msg);

// ตกขอบสนาม
const r4 = QB.run(QB.parse('B20 F50'));
ok(r4.result.fell && r4.events.some((e) => e.type === 'end' && /ตกขอบ/.test(e.msg)), 'ถอยหลังตกขอบล่าง: จบรอบทันที', JSON.stringify(r4.result.fell));
ok(!r4.events.some((e) => e.type === 'start'), 'ตกขอบแล้วคำสั่งที่เหลือไม่ทำต่อ');

// เวลา
const t40 = run('F48').time, t80 = run('S80 F48').time;
ok(t80 < t40, 'ความเร็ว 80 ใช้เวลาน้อยกว่าความเร็ว 40', t40 + ' / ' + t80);
ok(Math.abs(run('R').time - 1.0) < 0.05 && Math.abs(run('U').time - 1.6) < 0.05, 'เลี้ยว 90° ≈ 1.0 วินาที กลับหลัง ≈ 1.6 วินาที');

// โบนัส: ต้องครบทั้งช่องและกระป๋อง
ok(!r2.bonus && !r2.rows.find((r) => r.label === 'โบนัสครบทุกช่อง').points, 'ยังไม่ครบทุกช่อง ไม่ได้โบนัส');

// เส้นทางอ้างอิง (ไม่แสดงบนหน้าเว็บ): ยืนยันว่าสนามนี้ทำคะแนนเต็มได้จริงโดยไม่แตะเส้น
const FULL_RUN = 'F33 R F30 R F32 B32 U F63 B32 L F30 R F32 B32 R F60 L F32 B32 R F29 L F32 B32 U F63 B32 R F29 L F32';
const rf = run(FULL_RUN);
ok(rf.total === 200 && rf.touches === 0 && rf.bonus && !rf.fell, 'เส้นทางอ้างอิงได้คะแนนเต็ม 200 ไม่แตะเส้นดำ', JSON.stringify(rf.rows));

// ===================== วนซ้ำ ฟังก์ชัน และเงื่อนไข =====================
const mv = (op, v) => ({ kind: 'move', op, v, id: op + (v || '') });
const dist = { dist: true }, n = (x) => ({ num: x });
const C = (tree, funcs) => QB.compile(tree, funcs);
const ran = (tree, funcs) => QB.run(C(tree, funcs).code).result;

ok(C([mv('F', 33), mv('R'), { kind: 'reset', id: 'z' }]).text === 'F33 R Z', 'บล็อกต่อกันธรรมดา ได้ข้อความแบบเดิม (+ Z เริ่มนับระยะใหม่)');

const sq = C([{ kind: 'repeat', n: 4, id: 'rep', body: [mv('F', 10), mv('R')] }]);
ok(sq.text === 'P4 Q5 F10 R J1', 'ทำซ้ำ 4 ครั้ง แปลงเป็น P4 Q5 F10 R J1', sq.text);
const rq = QB.run(sq.code).result;
ok(Math.abs(rq.robot.x - QB.START.x) < 0.01 && Math.abs(rq.robot.y - QB.START.y) < 0.01 && rq.robot.h === 0 && rq.odo === 40,
  'ทำซ้ำ 4 ครั้ง (เดินหน้า 10 เลี้ยวขวา) กลับมาที่เดิม วิ่งรวม 40 ซม.', JSON.stringify(rq.robot) + ' odo ' + rq.odo);
ok(sq.src.join() === 'rep,rep,F10,R,rep', 'ทุกคำสั่งรู้ว่ามาจากบล็อกไหน (ไว้ไฮไลต์)', sq.src.join());
ok(ran([{ kind: 'repeat', n: 0, id: 'r0', body: [mv('F', 50)] }]).odo === 0, 'ทำซ้ำ 0 ครั้ง ไม่ทำข้างในเลย');

const until = C([{ kind: 'loop', until: true, cond: { a: dist, op: '>=', b: n(60) }, id: 'u', body: [mv('F', 7)] }]);
ok(until.text === 'Yd<60@3 F7 J0', 'ทำซ้ำจนกว่า ระยะ ≥ 60 แปลงเป็น "ขณะที่ ระยะ < 60"', until.text);
const ru = QB.run(until.code).result;
ok(ru.odo === 63 && Math.abs(ru.robot.y - (QB.START.y - 63)) < 0.01, 'เดินหน้าทีละ 7 จนระยะ ≥ 60: หยุดที่ 63 ซม. (9 รอบ)', ru.odo);
const rw = ran([{ kind: 'loop', until: false, cond: { a: dist, op: '<', b: n(30) }, id: 'w', body: [mv('F', 10)] }]);
ok(rw.odo === 30, 'ทำซ้ำขณะที่ ระยะ < 30 (เดินหน้าทีละ 10) หยุดที่ 30 ซม.', rw.odo);
ok(ran([{ kind: 'loop', until: true, cond: { a: dist, op: '=', b: n(20) }, id: 'e', body: [mv('F', 5)] }]).odo === 20, 'เครื่องหมาย = ใช้ได้ (ระยะปัดเป็นซม.เต็ม)');
ok(ran([mv('F', 30), { kind: 'reset', id: 'z' }, { kind: 'loop', until: true, cond: { a: dist, op: '>=', b: n(20) }, id: 'u2', body: [mv('F', 10)] }]).odo === 20,
  'เริ่มนับระยะใหม่แล้ว ระยะนับจาก 0 อีกครั้ง');
ok(C([{ kind: 'loop', until: false, cond: { a: n(1), op: '>', b: n(2) }, id: 'c', body: [mv('F', 10)] }]).text === '', 'เงื่อนไขตัวเลขล้วนที่ไม่จริง ไม่ทำข้างในเลย');

const fn = C([{ kind: 'call', name: 'ดัน', id: 'c1' }, mv('U'), { kind: 'call', name: 'ดัน', id: 'c2' }],
  { 'ดัน': { id: 'f', body: [mv('F', 20), mv('B', 20)] } });
ok(fn.text === 'F20 B20 U F20 B20', 'เรียกฟังก์ชัน 2 ครั้ง ได้คำสั่งข้างในฟังก์ชัน 2 ชุด', fn.text);
let e1 = {};
try { C([{ kind: 'call', name: 'วน', id: 'c' }], { 'วน': { id: 'f', body: [mv('F', 5), { kind: 'call', name: 'วน', id: 'inner' }] } }); } catch (e) { e1 = e; }
ok(/เรียกตัวเอง/.test(e1.message) && e1.blockId === 'inner', 'ฟังก์ชันเรียกตัวเอง แจ้งผิดและชี้บล็อกที่เรียก', e1.message);
let e2 = {};
try { C([{ kind: 'repeat', n: 2.5, id: 'bad', body: [] }]); } catch (e) { e2 = e; }
ok(/จำนวนเต็ม/.test(e2.message) && e2.blockId === 'bad', 'จำนวนรอบไม่ใช่จำนวนเต็ม แจ้งผิด', e2.message);
let e3 = {};
try { C(Array.from({ length: 201 }, (_, i) => mv('F', 1 + (i % 9)))); } catch (e) { e3 = e; }
ok(/ยาวเกิน 200/.test(e3.message), 'โปรแกรมเกิน 200 คำสั่ง แจ้งผิด', e3.message);
let deep = [mv('F', 1)];
for (let i = 0; i < 9; i++) deep = [{ kind: 'repeat', n: 1, id: 'd' + i, body: deep }];
let e4 = {};
try { C(deep); } catch (e) { e4 = e; }
ok(/ไม่เกิน 8 ชั้น/.test(e4.message), 'ทำซ้ำซ้อนกันเกิน 8 ชั้น แจ้งผิด', e4.message);

// กันวนไม่จบ
const stuck = QB.run(C([{ kind: 'loop', until: false, cond: { a: dist, op: '<', b: n(10) }, id: 's', body: [] }]).code);
ok(stuck.result.endReason === 'loop' && stuck.events.some((e) => /ไม่ขยับ/.test(e.msg)), 'วนซ้ำแต่ไม่มีการเคลื่อนที่ จำลองหยุดเองพร้อมบอกสาเหตุ');
const spin = QB.run(C([{ kind: 'loop', until: false, cond: { a: n(0), op: '<', b: n(1) }, id: 's', body: [mv('R')] }]).code);
ok(spin.result.endReason === 'time' && spin.result.time <= QB.LIMIT.seconds + 2, 'หมุนวนตลอดไป จำลองหยุดที่ 3 นาที', spin.result.time);

// ข้อความที่ส่งให้หุ่น อ่านกลับได้ตรงกัน
const big = C([mv('S', 60), { kind: 'repeat', n: 3, id: 'r', body: [
  { kind: 'loop', until: true, cond: { a: n(12.5), op: '<=', b: dist }, id: 'l', body: [mv('F', 5)] }, mv('L'), { kind: 'reset', id: 'z' }] }]);
ok(QB.toText(QB.parseCode(big.text)) === big.text, 'แปลงข้อความไป-กลับได้ตรงกัน (รวมคำสั่งวนซ้ำ)', big.text);
ok(big.text.split(' ').every((tk) => tk.length + 1 <= 20), 'ทุกคำสั่งสั้นพอส่งทาง Bluetooth (ไม่เกิน 20 ตัวอักษร)');
let e5 = '';
try { QB.parse('F10 J0'); } catch (e) { e5 = e.message; }
ok(/พิมพ์เองไม่ได้/.test(e5), 'พิมพ์คำสั่งวนซ้ำ (J P Q Y) เองเพื่อสร้างบล็อกไม่ได้ แจ้งเป็นภาษาไทย', e5);

console.log('\n' + pass + ' ผ่าน, ' + fail + ' ไม่ผ่าน');
process.exit(fail ? 1 : 0);

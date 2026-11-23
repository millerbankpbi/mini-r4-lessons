// ทดสอบตัวจำลองและตัวนับคะแนน Quick Box Drop:  node test-engine.js
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

console.log('\n' + pass + ' ผ่าน, ' + fail + ' ไม่ผ่าน');
process.exit(fail ? 1 : 0);

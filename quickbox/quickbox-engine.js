/* quickbox-engine.js — สนาม Dun Dun Box Drop + ตัวจำลองการเคลื่อนที่ + ตัวนับคะแนน
 * ใช้ได้ทั้งในเบราว์เซอร์ (window.QB) และ Node (require) — ไม่ยุ่งกับหน้าเว็บ ไม่สุ่ม ไม่อ่านเวลาจริง
 *
 * หน่วยเป็นเซนติเมตร จุด (0,0) อยู่มุมซ้ายบนของสนาม x ไปทางขวา y ลงล่าง
 * ทิศหุ่น h เป็นองศา: 0 = หันขึ้น (ไปทางช่อง 8), 90 = หันขวา, ค่าบวก = หมุนตามเข็มนาฬิกา
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.QB = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // ===================== กติกา (แก้ตรงนี้ที่เดียว) =====================
  const POINTS = {
    start: 30,  // ออกตัว: จุดกลางหุ่นออกจากพื้นที่เขียวช่อง 1
    zone: 10,   // ไปถึงพื้นที่เขียวช่อง 2–8 ช่องละ (จุดกลางหุ่นอยู่ในพื้นที่เขียว)
    can: 10,    // ดันกระป๋องออกจากพื้นที่เขียวได้ กระป๋องละ (จุดกลางกระป๋องพ้นพื้นที่เขียว)
    bonus: 30,  // ไปครบทุกช่องและดันกระป๋องออกครบทุกใบ
    line: 0,    // แตะเส้นดำ ครั้งละ (ตอนนี้นับไว้ให้ดูเฉยๆ ไม่หักคะแนน)
  };
  const CANS = 7;                 // กระป๋องที่ช่อง 2–8
  const ZONES = 7;                // พื้นที่เขียวที่ต้องไปถึง ช่อง 2–8
  const FULL = POINTS.start + POINTS.zone * ZONES + POINTS.can * CANS + POINTS.bonus;   // 200

  // ===================== สนาม (ตามกติกาข้อ 2.1–2.3 และภาพสนาม) =====================
  const FIELD = {
    size: 120,
    // เส้นดำกว้าง 2 ซม. (สี่เหลี่ยม x, y, w, h)
    lines: [
      { x: 0, y: 0, w: 120, h: 2 }, { x: 0, y: 118, w: 120, h: 2 },     // ขอบบน ขอบล่าง
      { x: 0, y: 0, w: 2, h: 120 }, { x: 118, y: 0, w: 2, h: 120 },     // ขอบซ้าย ขอบขวา
      { x: 29, y: 2, w: 2, h: 28 }, { x: 59, y: 2, w: 2, h: 28 }, { x: 89, y: 2, w: 2, h: 28 },   // คั่นช่องบน
      { x: 29, y: 90, w: 2, h: 28 }, { x: 89, y: 90, w: 2, h: 28 },     // คั่นช่องล่าง 1|2 และ 3|4
      { x: 59, y: 59, w: 2, h: 59 },                                     // เส้นกลางคั่นช่อง 2|3
      { x: 2, y: 59, w: 28, h: 2 },                                      // เส้นนอนซ้าย
      { x: 59, y: 59, w: 31, h: 2 },                                     // เส้นนอนขวา
    ],
    // พื้นที่สีเขียว 8 จุด ประมาณ 15 x 30 ซม.
    zones: [
      { n: 1, x: 2, y: 103, w: 27, h: 15 }, { n: 2, x: 31, y: 103, w: 28, h: 15 },
      { n: 3, x: 61, y: 103, w: 28, h: 15 }, { n: 4, x: 91, y: 103, w: 27, h: 15 },
      { n: 5, x: 91, y: 2, w: 27, h: 15 }, { n: 6, x: 61, y: 2, w: 28, h: 15 },
      { n: 7, x: 31, y: 2, w: 28, h: 15 }, { n: 8, x: 2, y: 2, w: 27, h: 15 },
    ],
    canZones: [2, 3, 4, 5, 6, 7, 8],   // กระป๋องวางกลางพื้นที่เขียวช่อง 2–8
  };

  // ===================== หุ่นและกระป๋อง =====================
  const ROBOT = { w: 16, l: 18 };   // หุ่นกว้าง 16 ซม. ยาว 18 ซม. หมุนรอบจุดกลางตัว
  const CAN_R = 3.3;                // กระป๋องน้ำอัดลม เส้นผ่านศูนย์กลาง 6.6 ซม.
  const START = { x: 15.5, y: 108.5, h: 0 };   // ในช่อง 1 หันขึ้น

  // ===================== เวลา (ประมาณการให้ใกล้หุ่นจริง) =====================
  const SPEED = { def: 40, min: 15, max: 80 };      // ความเร็วเริ่มต้นตรงกับโค้ดในหุ่น
  const TIME = {
    cmPerSecPerSpeed: 0.6,   // ความเร็ว 40 ≈ 24 ซม./วินาที
    straightExtra: 0.35,     // เร่งออกตัว + เบรก (วินาที)
    turn90: 1.0, turn180: 1.6,
  };
  const DIST = { min: 1, max: 150 };
  const STEP_CM = 0.5, STEP_DEG = 3;   // ความละเอียดการจำลอง

  // ===================== โปรแกรม: ข้อความเดียวกับที่ส่งให้หุ่น =====================
  // F30 = เดินหน้า 30 ซม., B20 = ถอยหลัง 20 ซม., L = เลี้ยวซ้าย 90°, R = เลี้ยวขวา 90°, U = กลับหลัง 180°, S50 = ความเร็ว 50
  function toText(steps) {
    return steps.map((s) => s.op + (s.op === 'F' || s.op === 'B' || s.op === 'S' ? String(s.v) : '')).join(' ');
  }
  function parse(text) {
    const out = [];
    for (const tok of String(text).trim().split(/\s+/).filter(Boolean)) {
      const m = /^([FBSLRU])(\d+)?$/.exec(tok.toUpperCase());
      if (!m) throw new Error('ไม่รู้จักคำสั่ง "' + tok + '"');
      const op = m[1], v = m[2] === undefined ? null : Number(m[2]);
      if ('FBS'.includes(op)) {
        if (v === null) throw new Error('คำสั่ง ' + op + ' ต้องมีตัวเลข เช่น ' + op + '30');
        const lim = op === 'S' ? SPEED : DIST;
        if (v < lim.min || v > lim.max) throw new Error(tok + ': ตัวเลขต้องอยู่ระหว่าง ' + lim.min + '–' + lim.max);
        out.push({ op, v });
      } else {
        if (v !== null) throw new Error('คำสั่ง ' + op + ' ไม่ต้องมีตัวเลข');
        out.push({ op });
      }
    }
    return out;
  }

  // ===================== เรขาคณิต =====================
  const rad = (d) => (d * Math.PI) / 180;
  function corners(r) {
    const s = Math.sin(rad(r.h)), c = Math.cos(rad(r.h));
    const fx = s, fy = -c, rx = c, ry = s;   // ทิศหน้า และทิศขวาของหุ่น
    const hl = ROBOT.l / 2, hw = ROBOT.w / 2;
    return [[hl, -hw], [hl, hw], [-hl, hw], [-hl, -hw]].map(([a, b]) => [r.x + fx * a + rx * b, r.y + fy * a + ry * b]);
  }
  // หุ่น (สี่เหลี่ยมหมุนได้) ทับสี่เหลี่ยมแนวแกนไหม — ใช้ separating axis
  function robotHitsRect(r, q) {
    const pts = corners(r);
    const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
    if (Math.max(...xs) <= q.x || Math.min(...xs) >= q.x + q.w || Math.max(...ys) <= q.y || Math.min(...ys) >= q.y + q.h) return false;
    const rc = [[q.x, q.y], [q.x + q.w, q.y], [q.x + q.w, q.y + q.h], [q.x, q.y + q.h]];
    const s = Math.sin(rad(r.h)), c = Math.cos(rad(r.h));
    for (const [ax, ay, half] of [[s, -c, ROBOT.l / 2], [c, s, ROBOT.w / 2]]) {
      const center = r.x * ax + r.y * ay;
      const proj = rc.map((p) => p[0] * ax + p[1] * ay);
      if (Math.max(...proj) <= center - half || Math.min(...proj) >= center + half) return false;
    }
    return true;
  }
  // จุดบนตัวหุ่นที่ใกล้จุด (px,py) ที่สุด (ในพิกัดสนาม) และจุดนั้นอยู่ในตัวหุ่นไหม
  function closestOnRobot(r, px, py) {
    const s = Math.sin(rad(r.h)), c = Math.cos(rad(r.h));
    const dx = px - r.x, dy = py - r.y;
    const a = dx * s - dy * c;   // ตามแนวหน้า
    const b = dx * c + dy * s;   // ตามแนวขวา
    const ca = Math.max(-ROBOT.l / 2, Math.min(ROBOT.l / 2, a));
    const cb = Math.max(-ROBOT.w / 2, Math.min(ROBOT.w / 2, b));
    return { x: r.x + s * ca + c * cb, y: r.y - c * ca + s * cb, inside: ca === a && cb === b };
  }
  const inRect = (q, x, y) => x >= q.x && x <= q.x + q.w && y >= q.y && y <= q.y + q.h;
  const zoneOf = (n) => FIELD.zones.find((z) => z.n === n);

  // ===================== จำลอง =====================
  function newSim() {
    return {
      t: 0, speed: SPEED.def, step: -1,
      robot: { ...START },
      cans: FIELD.canZones.map((n) => { const z = zoneOf(n); return { zone: n, x: z.x + z.w / 2, y: z.y + z.h / 2, out: false }; }),
      touching: FIELD.lines.map(() => false),
      started: false, visited: [],
      touches: 0, ended: false, endReason: '',
      events: [], frames: [],
    };
  }
  function log(S, type, msg, points, n) { S.events.push({ t: +S.t.toFixed(2), s: S.step, type, msg, points: points || 0, n: n || 0 }); }
  function frame(S) {
    S.frames.push({ t: S.t, s: S.step, x: S.robot.x, y: S.robot.y, h: S.robot.h, cans: S.cans.map((k) => [k.x, k.y]) });
  }

  // ดันกระป๋องที่ทับตัวหุ่นออกไป (move = ทิศที่หุ่นกำลังไป ใช้ตอนกระป๋องจมเข้าไปในตัวหุ่น)
  function pushCans(S, mx, my) {
    for (const k of S.cans) {
      const p = closestOnRobot(S.robot, k.x, k.y);
      let nx = k.x - p.x, ny = k.y - p.y, d = Math.hypot(nx, ny);
      if (p.inside || d < 1e-9) {
        const m = Math.hypot(mx, my) || 1;
        nx = mx / m; ny = my / m;
        // ดันออกจากด้านที่หุ่นกำลังเคลื่อนไปหา
        const s = Math.sin(rad(S.robot.h)), c = Math.cos(rad(S.robot.h));
        const a = (k.x - S.robot.x) * s - (k.y - S.robot.y) * c;
        const b = (k.x - S.robot.x) * c + (k.y - S.robot.y) * s;
        const push = Math.min(ROBOT.l / 2 - Math.abs(a), ROBOT.w / 2 - Math.abs(b)) + CAN_R;
        k.x += nx * push; k.y += ny * push;
      } else if (d < CAN_R) {
        k.x += (nx / d) * (CAN_R - d); k.y += (ny / d) * (CAN_R - d);
      }
    }
    // กระป๋องชนกันเอง: แยกออกจากกัน
    for (let i = 0; i < S.cans.length; i++) for (let j = i + 1; j < S.cans.length; j++) {
      const A = S.cans[i], B = S.cans[j], dx = B.x - A.x, dy = B.y - A.y, d = Math.hypot(dx, dy);
      if (d > 0 && d < 2 * CAN_R) { const o = (2 * CAN_R - d) / 2; A.x -= (dx / d) * o; A.y -= (dy / d) * o; B.x += (dx / d) * o; B.y += (dy / d) * o; }
    }
  }

  // ตรวจหลังขยับทุกครั้ง: กระป๋องออกจากพื้นที่เขียว แตะเส้นดำ ตกขอบสนาม
  function judge(S) {
    const r0 = S.robot;
    // ตกขอบก่อน: หุ่นที่ถอยตกสนามต้องไม่ได้คะแนนออกตัว
    if (r0.x < 0 || r0.x > FIELD.size || r0.y < 0 || r0.y > FIELD.size) {
      S.ended = true; S.endReason = 'fell';
      log(S, 'end', 'หุ่นตกขอบสนาม จบรอบ (คะแนนที่ได้ก่อนตกยังนับ)');
      return;
    }
    const inPlay = r0.x > 2 && r0.x < FIELD.size - 2 && r0.y > 2 && r0.y < FIELD.size - 2;   // ไม่นับตอนจุดกลางหุ่นอยู่บนขอบดำนอกสุด
    if (!S.started && inPlay && !inRect(zoneOf(1), r0.x, r0.y)) {
      S.started = true;
      log(S, 'start', 'ออกตัวจากช่อง 1 แล้ว +' + POINTS.start, POINTS.start);
    }
    for (const n of FIELD.canZones) {
      if (!S.visited.includes(n) && inRect(zoneOf(n), r0.x, r0.y)) {
        S.visited.push(n);
        log(S, 'zone', 'ไปถึงพื้นที่เขียวช่อง ' + n + ' +' + POINTS.zone, POINTS.zone, n);
      }
    }
    for (const k of S.cans) {
      if (!k.out && !inRect(zoneOf(k.zone), k.x, k.y)) {
        k.out = true;
        log(S, 'can', 'ดันกระป๋องช่อง ' + k.zone + ' ออกจากพื้นที่เขียวแล้ว +' + POINTS.can, POINTS.can, k.zone);
      }
    }
    FIELD.lines.forEach((q, i) => {
      const hit = robotHitsRect(S.robot, q);
      if (hit && !S.touching[i]) {
        S.touches++;
        log(S, 'line', 'หุ่นแตะเส้นดำ' + (POINTS.line ? ' ' + POINTS.line : '') + ' (ลองปรับระยะให้สั้นลง หรือเลี้ยวก่อนถึงเส้น)', POINTS.line);
      }
      S.touching[i] = hit;
    });
  }

  function straight(S, cm) {
    const dir = cm >= 0 ? 1 : -1, n = Math.ceil(Math.abs(cm) / STEP_CM), step = Math.abs(cm) / n * dir;
    const v = S.speed * TIME.cmPerSecPerSpeed, dt = Math.abs(step) / v;
    for (let i = 0; i < n && !S.ended; i++) {
      const mx = Math.sin(rad(S.robot.h)) * step, my = -Math.cos(rad(S.robot.h)) * step;
      S.robot.x += mx; S.robot.y += my; S.t += dt;
      pushCans(S, mx, my); judge(S); frame(S);
    }
    S.t += TIME.straightExtra;
  }
  function turn(S, deg) {
    const n = Math.ceil(Math.abs(deg) / STEP_DEG), step = deg / n;
    const total = Math.abs(deg) >= 180 ? TIME.turn180 : TIME.turn90 * Math.abs(deg) / 90, dt = total / n;
    for (let i = 0; i < n && !S.ended; i++) {
      S.robot.h += step; S.t += dt;
      // ทิศที่ขอบหุ่นกวาดไป ใช้ดันกระป๋องที่จมเข้ามา
      pushCans(S, 0, 0); judge(S); frame(S);
    }
    S.robot.h = ((Math.round(S.robot.h) % 360) + 360) % 360;
  }

  // รันทั้งโปรแกรม คืนเฟรมสำหรับแอนิเมชัน เหตุการณ์ และคะแนน
  function run(steps) {
    const S = newSim();
    frame(S);
    log(S, 'info', 'เริ่มที่ช่อง 1 หันหน้าไปทางช่อง 8');
    for (const [i, s] of steps.entries()) {
      if (S.ended) break;
      S.step = i;
      if (s.op === 'F') straight(S, s.v);
      else if (s.op === 'B') straight(S, -s.v);
      else if (s.op === 'L') turn(S, -90);
      else if (s.op === 'R') turn(S, 90);
      else if (s.op === 'U') turn(S, 180);
      else if (s.op === 'S') { S.speed = s.v; log(S, 'info', 'ตั้งความเร็วเป็น ' + s.v); }
      frame(S);   // จบคำสั่งนี้ (กันเวลาค้างตอนเบรกให้แอนิเมชันเห็น)
    }
    if (!S.ended) log(S, 'end', 'จบโปรแกรม');
    const R = score(S);
    if (R.bonus) log(S, 'bonus', 'ไปครบทุกช่องและดันกระป๋องครบ โบนัส +' + POINTS.bonus, POINTS.bonus);
    return { frames: S.frames, events: S.events, result: R };
  }

  function score(S) {
    const cansOut = S.cans.filter((k) => k.out).length;
    const zones = S.visited.length;
    const bonus = cansOut === CANS && zones === ZONES;
    const rows = [
      { label: 'ออกตัว', value: S.started ? 'ได้' : 'ยังไม่ออก', points: S.started ? POINTS.start : 0 },
      { label: 'ไปถึงพื้นที่เขียว', value: zones + '/' + ZONES, points: zones * POINTS.zone },
      { label: 'ดันกระป๋องออก', value: cansOut + '/' + CANS, points: cansOut * POINTS.can },
      { label: 'โบนัสครบทุกช่อง', value: bonus ? 'ได้' : 'ยังไม่ได้', points: bonus ? POINTS.bonus : 0 },
      { label: 'แตะเส้นดำ', value: S.touches + ' ครั้ง', points: S.touches * POINTS.line },
    ];
    return {
      started: S.started, zones, visited: S.visited.slice().sort(), cansOut, bonus,
      touches: S.touches, time: +S.t.toFixed(1), fell: S.endReason === 'fell',
      total: rows.reduce((a, r) => a + r.points, 0), full: FULL, rows,
      cans: S.cans.map((k) => ({ zone: k.zone, out: k.out })),
    };
  }

  return { POINTS, CANS, ZONES, FULL, FIELD, ROBOT, CAN_R, START, SPEED, DIST, TIME, parse, toText, run, corners, robotHitsRect };
});

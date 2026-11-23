//@ th=ส่วนกลาง: ส่งข้อความให้หุ่น กดค้าง และหยุด|en=Core: send messages, hold to repeat, and stop|lo=ສ່ວນກາງ: ສົ່ງຂໍ້ຄວາມໃຫ້ຫຸ່ນຍົນ ກົດຄ້າງ ແລະ ຢຸດ
const $ = (css) => document.querySelector(css);
let online = false;

//@ th=รวมกำลังล้อซ้าย-ขวาเป็นเลขเดียว: (ซ้าย+100)×1000 + (ขวา+100)|en=Pack left and right wheel power into one number: (L+100)×1000 + (R+100)|lo=ລວມກຳລັງລໍ້ຊ້າຍ-ຂວາເປັນເລກດຽວ: (ຊ້າຍ+100)×1000 + (ຂວາ+100)
//@ th=เช่น ซ้าย 60 ขวา 40 → "160140" · หุ่นรู้ว่าเลขตั้งแต่ 1000 ขึ้นไปคือคันโยก|en=e.g. left 60, right 40 → "160140" · the robot knows a number of 1000 or more is the stick|lo=ເຊັ່ນ ຊ້າຍ 60 ຂວາ 40 → "160140" · ຫຸ່ນຍົນຮູ້ວ່າເລກຕັ້ງແຕ່ 1000 ຂຶ້ນໄປແມ່ນຄັນໂຍກ
function pack(l, r) {
  const fit = (v) => Math.max(-99, Math.min(99, Math.round(v)));
  return String((fit(l) + 100) * 1000 + (fit(r) + 100));
}

//@ th=คันโยก → กำลังล้อ: y = เดินหน้า/ถอย, x = เลี้ยว (−1 ถึง 1), speed = กำลังสูงสุด|en=Stick → wheel power: y = forward/back, x = turn (−1 to 1), speed = top power|lo=ຄັນໂຍກ → ກຳລັງລໍ້: y = ເດີນໜ້າ/ຖອຍ, x = ລ້ຽວ (−1 ຫາ 1), speed = ກຳລັງສູງສຸດ
function mix(x, y, speed) {
  const fit = (v, max) => Math.max(-max, Math.min(max, v));
  return [fit(Math.round(fit(y + x, 1) * speed), 99), fit(Math.round(fit(y - x, 1) * speed), 99)];
}

//@ th=ส่งข้อความให้หุ่น (ถ้ายังไม่เชื่อมต่อ จะแสดงบนจออย่างเดียว)|en=Send text to the robot (when not connected it is only shown on screen)|lo=ສົ່ງຂໍ້ຄວາມໃຫ້ຫຸ່ນຍົນ (ຖ້າຍັງບໍ່ເຊື່ອມຕໍ່ ຈະສະແດງເທິງຈໍຢ່າງດຽວ)
function send(text) {
  if (!text) return;
  log('out', text);
  if (online) Link.write(text);
}

//@ th=แสดงข้อความ: out = ส่งไป, in = หุ่นตอบมา, info = แจ้งเตือน|en=Show a message: out = sent, in = from the robot, info = notice|lo=ສະແດງຂໍ້ຄວາມ: out = ສົ່ງໄປ, in = ຫຸ່ນຍົນຕອບມາ, info = ແຈ້ງເຕືອນ
function log(dir, text) {
  $({ out: '#out', in: '#in', info: '#note' }[dir]).textContent = text;
  if (typeof termAdd === 'function') termAdd(dir, text);
}

//@ th=กดค้าง: ส่งซ้ำทุก ms มิลลิวินาที จนกว่าจะเรียก stop() · ปล่อยครบทุกอย่างแล้วส่ง S|en=Hold: send again every ms milliseconds until stop() is called · when nothing is held, send S|lo=ກົດຄ້າງ: ສົ່ງຊ້ຳທຸກ ms ມິນລິວິນາທີ ຈົນກວ່າຈະເອີ້ນ stop() · ປ່ອຍໝົດທຸກຢ່າງແລ້ວສົ່ງ S
const repeats = new Set();
function holdRepeat(text, ms) {
  const get = typeof text === 'function' ? text : () => text;
  send(get());
  const timer = setInterval(() => send(get()), ms);
  function stop() {
    if (!repeats.delete(stop)) return;
    clearInterval(timer);
    if (repeats.size === 0) send('S');
  }
  repeats.add(stop);
  return stop;
}

//@ th=จำว่านิ้วไหน (pointerId) กดปุ่มไหน จึงใช้หลายนิ้วพร้อมกันได้|en=Remember which finger (pointerId) holds which control, so several fingers work at once|lo=ຈື່ວ່ານິ້ວໃດ (pointerId) ກົດປຸ່ມໃດ ຈຶ່ງໃຊ້ຫຼາຍນິ້ວພ້ອມກັນໄດ້
const pressed = new Map();
function press(el, down, up, move) {
  let finger = null;
  function end(e) {
    if (finger === null || (e && e.pointerId !== finger)) return;
    finger = null;
    pressed.delete(el);
    el.classList.remove('held');
    if (up) up();
  }
  el.addEventListener('pointerdown', (e) => {
    if (finger !== null) return;
    finger = e.pointerId;
    el.setPointerCapture(finger);
    el.classList.add('held');
    down(e);
    pressed.set(el, end);
  });
  el.addEventListener('pointermove', (e) => {
    if (move && e.pointerId === finger) move(e);
  });
  el.addEventListener('pointerup', end);
  el.addEventListener('pointercancel', end);
}

//@ th=ปล่อยทุกปุ่ม (ปิดจอ สลับแอป หรือหลุดการเชื่อมต่อ) · ได้ true ถ้าส่ง S ไปแล้ว|en=Let go of everything (screen off, app switched or connection lost) · true if S was sent|lo=ປ່ອຍທຸກປຸ່ມ (ປິດຈໍ ສະຫຼັບແອັບ ຫຼື ຫຼຸດການເຊື່ອມຕໍ່) · ໄດ້ true ຖ້າສົ່ງ S ແລ້ວ
function releaseAll() {
  const held = repeats.size > 0;
  pressed.forEach((end) => end());
  repeats.forEach((stop) => stop());
  return held;
}

//@ th=ปุ่มเชื่อมต่อ และสถานะ (จุดเขียว + ชื่อหุ่น = ต่ออยู่กับหุ่นตัวนั้น)|en=Connect button and status (green dot + robot name = connected to that robot)|lo=ປຸ່ມເຊື່ອມຕໍ່ ແລະ ສະຖານະ (ຈຸດຂຽວ + ຊື່ຫຸ່ນຍົນ = ເຊື່ອມຕໍ່ຢູ່ກັບຫຸ່ນຍົນໂຕນັ້ນ)
$('#connect').onclick = () => {
  $('#status').textContent = '{{wait}}';
  Link.connect().catch((e) => {
    if (!online) $('#status').textContent = '{{off}}';
    log('info', '{{fail}}: ' + e.message);
  });
};
Link.onState((state, name) => {
  const was = online;
  online = state === 'on';
  $('#dot').className = state;
  $('#status').textContent = online ? name : '{{off}}';
  if (online) {
    $('#note').textContent = '';
    //@ th=หลายหุ่นในห้องเดียว: เตือนถ้าต่อกับหุ่นคนละชื่อ|en=Many robots in one room: warn when connected to a robot with another name|lo=ຫຼາຍຫຸ່ນຍົນໃນຫ້ອງດຽວ: ເຕືອນຖ້າເຊື່ອມຕໍ່ກັບຫຸ່ນຍົນຄົນລະຊື່
    if (name !== CONFIG.name) log('info', '{{other}}: ' + CONFIG.name);
  } else {
    releaseAll();
    if (was) log('info', '{{lost}}');
  }
});
Link.onText((text) => log('in', text));

//@ th=ปิดจอ สลับแอป หรือออกจากหน้า ตอนกดค้าง → ปล่อยทุกปุ่มและส่ง S|en=Screen off, app switched or page left while holding → let go and send S|lo=ປິດຈໍ ສະຫຼັບແອັບ ຫຼື ອອກຈາກໜ້າ ຕອນກົດຄ້າງ → ປ່ອຍທຸກປຸ່ມ ແລະ ສົ່ງ S
document.addEventListener('visibilitychange', () => {
  if (document.hidden) releaseAll();
});
addEventListener('pagehide', releaseAll);
addEventListener('blur', releaseAll);
//@ th=กดค้างบนปุ่มแล้วไม่ให้ขึ้นเมนู|en=No pop-up menu on a long press|lo=ກົດຄ້າງເທິງປຸ່ມແລ້ວບໍ່ໃຫ້ຂຶ້ນເມນູ
addEventListener('contextmenu', (e) => {
  if (e.target.closest('#pad')) e.preventDefault();
});
//@ th=ปุ่มหยุดสีแดง: ปล่อยทุกอย่างแล้วส่ง S|en=Red stop button: let go of everything and send S|lo=ປຸ່ມຢຸດສີແດງ: ປ່ອຍທຸກຢ່າງແລ້ວສົ່ງ S
document.querySelectorAll('.stop').forEach((b) => press(b, () => releaseAll() || send('S')));

// exportHTML(config, lang) -> one standalone controller HTML file (string).
// build_rc.py wraps this file with PARTS (src/rc/parts/*.js by name), CSS (parts/style.css),
// TEMPLATE (export_template.html) and PRESETS (presets.json) into out/web/rc/rc.js.
// Only the parts a config needs go into the file. Source comments are written
// `//@ th=…|en=…|lo=…` (CSS `/*@ … */`, HTML `<!--@ … -->`) and come out as a plain comment
// in the chosen language; `{{key}}` is a UI text from TEXT; `[[slot]]` is filled here.
// Sections of CSS and TEMPLATE start with a line `/*== name ==*/` or `<!--== name ==-->`.

const BROKER = 'wss://broker.hivemq.com:8884/mqtt';
const MODES = ['none', 'tap4', 'hold4', 'stick1', 'stick2'];
const TEXT = {
  th: {
    title: 'จอยบังคับหุ่น', connect: 'เชื่อมต่อ', wait: 'กำลังเชื่อมต่อ…', off: 'ยังไม่เชื่อมต่อ',
    lost: 'หลุดการเชื่อมต่อ กด “เชื่อมต่อ” อีกครั้ง', fail: 'เชื่อมต่อไม่สำเร็จ', stop: 'หยุด', send: 'ส่ง',
    typeHere: 'พิมพ์ข้อความ', other: 'หุ่นตัวนี้ไม่ใช่ชื่อที่ตั้งไว้ใน CONFIG.name',
    noBle: 'เบราว์เซอร์นี้ใช้ Bluetooth ไม่ได้ · Android ใช้ Chrome · iPhone/iPad ใช้แอป Bluefy',
  },
  en: {
    title: 'Robot controller', connect: 'Connect', wait: 'Connecting…', off: 'Not connected',
    lost: 'Connection lost. Tap Connect again.', fail: 'Could not connect', stop: 'STOP', send: 'Send',
    typeHere: 'Type a message', other: 'This robot is not the name set in CONFIG.name',
    noBle: 'This browser has no Web Bluetooth. Android: use Chrome. iPhone/iPad: use the Bluefy app.',
  },
  lo: {
    title: 'ຈອຍຄວບຄຸມຫຸ່ນຍົນ', connect: 'ເຊື່ອມຕໍ່', wait: 'ກຳລັງເຊື່ອມຕໍ່…', off: 'ຍັງບໍ່ໄດ້ເຊື່ອມຕໍ່',
    lost: 'ການເຊື່ອມຕໍ່ຫຼຸດ ກົດ “ເຊື່ອມຕໍ່” ອີກຄັ້ງ', fail: 'ເຊື່ອມຕໍ່ບໍ່ສຳເລັດ', stop: 'ຢຸດ', send: 'ສົ່ງ',
    typeHere: 'ພິມຂໍ້ຄວາມ', other: 'ຫຸ່ນຍົນໂຕນີ້ບໍ່ແມ່ນຊື່ທີ່ຕັ້ງໄວ້ໃນ CONFIG.name',
    noBle: 'ບຣາວເຊີນີ້ໃຊ້ Bluetooth ບໍ່ໄດ້ · Android ໃຊ້ Chrome · iPhone/iPad ໃຊ້ແອັບ Bluefy',
  },
};

const NOTE = /(\/\/|\/\*|<!--)@ th=([^|\n]*)\|en=([^|\n]*)\|lo=(.*?)( \*\/| -->)?$/gm;
const escHTML = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const escJS = (s) => s.replace(/[\\']/g, '\\$&');

function localize(src, lang, esc) {
  return src
    .replace(NOTE, (m, open, th, en, lo, close) => open + ' ' + { th, en, lo }[lang].trim() + (close || ''))
    .replace(/\{\{(\w+)\}\}/g, (m, key) => {
      if (!(key in TEXT[lang])) throw new Error('rc: no text for {{' + key + '}}');
      return esc(TEXT[lang][key]);
    });
}

function sections(src) {
  const bits = src.split(/^(?:<!--|\/\*)== (\w+) ==(?:-->|\*\/)\n/m), out = {};
  for (let i = 1; i < bits.length; i += 2) out[bits[i]] = bits[i + 1];
  return out;
}

// [[slot]] alone on a line takes the whole line (removed when empty); other [[slot]]s are inline.
// One pass, so text put into a slot (a button label, say) is never read as a slot itself.
function fill(tpl, slots) {
  const get = (k) => {
    if (!(k in slots)) throw new Error('rc: no slot [[' + k + ']]');
    return String(slots[k]);
  };
  return tpl.replace(/^\[\[(\w+)\]\]\n|\[\[(\w+)\]\]/gm, (m, line, inline) =>
    line ? (get(line) ? get(line).replace(/\n*$/, '\n') : '') : get(inline));
}

function normalize(cfg, lang) {
  const num = (v, lo, hi, d) => Math.min(hi, Math.max(lo, Number.isFinite(Number(v)) && v !== null && v !== '' ? Number(v) : d));
  return {
    name: String(cfg.name || 'R4-T01'),
    link: cfg.link === 'mqtt' ? 'mqtt' : 'ble',
    mqtt: { url: String((cfg.mqtt && cfg.mqtt.url) || BROKER) },
    mode: MODES.includes(cfg.mode) ? cfg.mode : 'none',
    speed: Math.round(num(cfg.speed, 10, 100, 60)),
    terminal: Boolean(cfg.terminal),
    buttons: (cfg.buttons || []).map((b) => ({
      label: b.label && typeof b.label === 'object' ? String(b.label[lang] || b.label.en || '') : String(b.label || ''),
      press: String(b.press || ''),
      release: String(b.release || ''),
      angle: Math.round(num(b.angle, 0, 315, 0)),
      x: Math.round(num(b.x, 0, 100, 50) * 10) / 10,
      y: Math.round(num(b.y, 0, 100, 50) * 10) / 10,
    })),
  };
}

// Comments are localized before the values go in, so a name like "R4-{{x}}" stays as typed.
function configJS(c, dirs, sticks, lang) {
  const q = (v) => JSON.stringify(v).replace(/</g, '\\u003c');
  const say = (note) => localize(note, lang, escJS);
  return [
    say('//@ th=ตั้งค่า (แก้ตรงนี้ได้)|en=Settings (change them here)|lo=ຕັ້ງຄ່າ (ແກ້ບ່ອນນີ້ໄດ້)'),
    'const CONFIG = {',
    `  name: ${q(c.name)}, ` + say('//@ th=ชื่อหุ่น ต้องตรงกับในโค้ดหุ่น|en=robot name, must match the robot code|lo=ຊື່ຫຸ່ນຍົນ ຕ້ອງກົງກັບໃນໂຄດຫຸ່ນຍົນ'),
    c.link === 'mqtt' && `  mqtt: { url: ${q(c.mqtt.url)} }, ` + say('//@ th=broker (มือถือใช้ wss)|en=broker (phones use wss)|lo=broker (ມືຖືໃຊ້ wss)'),
    dirs && `  mode: ${q(c.mode)}, ` + say('//@ th=tap4 = กดครั้งเดียว · hold4 = กดค้าง|en=tap4 = tap once · hold4 = hold down|lo=tap4 = ກົດເທື່ອດຽວ · hold4 = ກົດຄ້າງ'),
    sticks && `  speed: ${c.speed}, ` + say('//@ th=กำลังล้อสูงสุดของคันโยก 10–100|en=top wheel power for the sticks, 10–100|lo=ກຳລັງລໍ້ສູງສຸດຂອງຄັນໂຍກ 10–100'),
    '};',
  ].filter(Boolean).join('\n');
}

function exportHTML(config, lang) {
  if (!TEXT[lang]) lang = 'th';
  const c = normalize(config || {}, lang);
  const dirs = c.mode === 'tap4' || c.mode === 'hold4', sticks = c.mode === 'stick1' || c.mode === 'stick2';
  const extra = c.buttons.length > 0;
  const html = sections(localize(TEMPLATE, lang, escHTML));
  const css = sections(localize(CSS, lang, (s) => s));
  const want = { base: true, round: dirs || extra, dirs, stick: sticks, xbtn: extra, term: c.terminal };
  const style = Object.keys(css).filter((k) => want[k]).map((k) => css[k].trim()).join('\n');
  const parts = ['link_' + c.link, 'core', dirs && 'mode_buttons', sticks && 'mode_stick', extra && 'extra_buttons', c.terminal && 'terminal'];
  const code = parts.filter(Boolean).map((p) => localize(PARTS[p], lang, escJS).trim());
  const js = [configJS(c, dirs, sticks, lang), ...code].join('\n\n');
  const list = c.buttons.map((b) => fill(html.xbtn, {
    x: b.x, y: b.y, angle: b.angle, press: escHTML(b.press), release: escHTML(b.release), label: escHTML(b.label),
  })).join('');
  const pad = c.mode === 'none' && !extra ? '' : fill(html.pad, {
    x: extra ? ' class="x"' : '',
    ctl: dirs ? html.dirs : sticks ? html[c.mode] : '',
    xbtns: extra ? fill(html.xbtns, { list }) : '',
  });
  return fill(html.page, { lang, name: escHTML(c.name), css: style, pad, term: c.terminal ? html.term : '', js });
}

function preset(key) {
  return PRESETS[key] ? JSON.parse(JSON.stringify(PRESETS[key])) : null;
}

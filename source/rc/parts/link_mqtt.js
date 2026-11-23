//@ th=เชื่อมต่อแบบ MQTT ผ่าน WebSocket: มือถือ → broker → หุ่น|en=MQTT link over WebSocket: phone → broker → robot|lo=ເຊື່ອມຕໍ່ແບບ MQTT ຜ່ານ WebSocket: ມືຖື → broker → ຫຸ່ນຍົນ
//@ th=คำสั่งไปที่หัวข้อ mr4/<ชื่อหุ่น>/cmd · หุ่นตอบที่ mr4/<ชื่อหุ่น>/msg|en=Commands go to topic mr4/<robot name>/cmd · the robot answers on mr4/<robot name>/msg|lo=ຄຳສັ່ງໄປທີ່ຫົວຂໍ້ mr4/<ຊື່ຫຸ່ນຍົນ>/cmd · ຫຸ່ນຍົນຕອບທີ່ mr4/<ຊື່ຫຸ່ນຍົນ>/msg
const MQTT = {
  //@ th=แพ็กเก็ต = ไบต์ชนิด + ความยาว (ไบต์ละ 7 บิต) + เนื้อหา|en=Packet = type byte + length (7 bits per byte) + body|lo=ແພັກເກັດ = ໄບຕ໌ຊະນິດ + ຄວາມຍາວ (ໄບຕ໌ລະ 7 ບິດ) + ເນື້ອໃນ
  packet(type, body) {
    const head = [type];
    let n = body.length;
    do {
      head.push((n % 128) + (n >= 128 ? 128 : 0));
      n = Math.floor(n / 128);
    } while (n > 0);
    return new Uint8Array([...head, ...body]);
  },
  //@ th=ข้อความ = ความยาว 2 ไบต์ + ตัวอักษร UTF-8|en=String = 2-byte length + UTF-8 bytes|lo=ຂໍ້ຄວາມ = ຄວາມຍາວ 2 ໄບຕ໌ + ຕົວອັກສອນ UTF-8
  str(s) {
    const b = new TextEncoder().encode(s);
    return [b.length >> 8, b.length & 255, ...b];
  },
  //@ th=CONNECT: MQTT 3.1.1 (รุ่น 4), clean session, keepalive เป็นวินาที|en=CONNECT: MQTT 3.1.1 (level 4), clean session, keepalive in seconds|lo=CONNECT: MQTT 3.1.1 (ລຸ້ນ 4), clean session, keepalive ເປັນວິນາທີ
  connect(id, keepalive) {
    return this.packet(0x10, [...this.str('MQTT'), 4, 2, keepalive >> 8, keepalive & 255, ...this.str(id)]);
  },
  publish(topic, text) {
    return this.packet(0x30, [...this.str(topic), ...new TextEncoder().encode(text)]);
  },
  subscribe(topic) {
    return this.packet(0x82, [0, 1, ...this.str(topic), 0]);
  },
  ping() {
    return new Uint8Array([0xc0, 0]);
  },
  //@ th=อ่านแพ็กเก็ตที่ครบแล้ว 1 อัน (ยังไม่ครบ = null)|en=Read one whole packet (not complete yet = null)|lo=ອ່ານແພັກເກັດທີ່ຄົບແລ້ວ 1 ອັນ (ຍັງບໍ່ຄົບ = null)
  decode(b) {
    let len = 0, i = 1;
    for (let mul = 1; ; mul *= 128) {
      if (i >= b.length) return null;
      len += (b[i] & 127) * mul;
      if (b[i++] < 128) break;
    }
    if (b.length < i + len) return null;
    const p = { type: b[0] >> 4, size: i + len, body: b.slice(i, i + len) };
    if (p.type === 3) {
      const n = (p.body[0] << 8) + p.body[1], start = 2 + n + ((b[0] & 6) ? 2 : 0);
      p.topic = new TextDecoder().decode(p.body.slice(2, 2 + n));
      p.text = new TextDecoder().decode(p.body.slice(start));
    }
    return p;
  },
};
const Link = {
  ws: null, textCb() {}, stateCb() {},
  onText(cb) { this.textCb = cb; },
  onState(cb) { this.stateCb = cb; },
  topic(end) { return 'mr4/' + CONFIG.name + '/' + end; },
  connect() {
    //@ th=กดซ้ำ → ปิดการเชื่อมต่อเก่า แล้วต่อใหม่|en=Tapped again → close the old connection and start a new one|lo=ກົດຊ້ຳ → ປິດການເຊື່ອມຕໍ່ເກົ່າ ແລ້ວເຊື່ອມຕໍ່ໃໝ່
    if (this.ws) this.ws.close();
    return new Promise((ok, fail) => {
      const ws = new WebSocket(CONFIG.mqtt.url, 'mqtt');
      let buf = new Uint8Array(0), ping = 0;
      this.ws = ws;
      ws.binaryType = 'arraybuffer';
      ws.onopen = () => ws.send(MQTT.connect('rc-' + Math.random().toString(36).slice(2, 8), 30));
      ws.onerror = () => fail(new Error(CONFIG.mqtt.url));
      ws.onclose = () => {
        clearInterval(ping);
        if (this.ws !== ws) return;
        this.ws = null;
        this.stateCb('off');
      };
      ws.onmessage = (e) => {
        buf = new Uint8Array([...buf, ...new Uint8Array(e.data)]);
        for (let p; (p = MQTT.decode(buf)); buf = buf.slice(p.size)) {
          if (p.type === 2 && p.body[1] !== 0) {
            fail(new Error('CONNACK ' + p.body[1]));
            ws.close();
          } else if (p.type === 2) {
            ws.send(MQTT.subscribe(this.topic('msg')));
            //@ th=ส่ง PINGREQ ทุก 15 วินาที (ครึ่งหนึ่งของ keepalive) ให้ broker รู้ว่ายังอยู่|en=PINGREQ every 15 s (half the keepalive) so the broker knows we are still here|lo=ສົ່ງ PINGREQ ທຸກ 15 ວິນາທີ (ເຄິ່ງໜຶ່ງຂອງ keepalive) ໃຫ້ broker ຮູ້ວ່າຍັງຢູ່
            ping = setInterval(() => ws.send(MQTT.ping()), 15000);
            this.stateCb('on', CONFIG.name);
            ok();
          } else if (p.type === 9 && p.body[2] === 0x80) log('info', '{{fail}}: ' + this.topic('msg'));
          else if (p.type === 3) this.textCb(p.text);
        }
      };
    });
  },
  async write(text) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) this.ws.send(MQTT.publish(this.topic('cmd'), text));
  },
};

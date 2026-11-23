//@ th=เชื่อมต่อ Bluetooth แบบ UART (บริการเดียวกับที่ MATRIXblock สร้างในหุ่น)|en=Bluetooth UART link (the same service MATRIXblock puts in the robot)|lo=ເຊື່ອມຕໍ່ Bluetooth ແບບ UART (ບໍລິການດຽວກັບທີ່ MATRIXblock ສ້າງໃນຫຸ່ນຍົນ)
const UART = '6e400001-b5a3-f393-e0a9-e50e24dcca9e';
const TO_ROBOT = '6e400002-b5a3-f393-e0a9-e50e24dcca9e';
const FROM_ROBOT = '6e400003-b5a3-f393-e0a9-e50e24dcca9e';
const Link = {
  dev: null, rx: null, tx: null, queue: [], busy: false,
  textCb() {}, stateCb() {},
  onText(cb) { this.textCb = cb; },
  onState(cb) { this.stateCb = cb; },
  async connect() {
    if (!navigator.bluetooth) throw new Error('{{noBle}}');
    //@ th=ครั้งแรก หรือกดตอนต่ออยู่ → เลือกหุ่นจากรายการ · หลุดแล้วกดใหม่ → ต่อหุ่นตัวเดิม|en=First time, or tapped while connected → pick a robot from the list · after a drop → the same robot again|lo=ເທື່ອທຳອິດ ຫຼື ກົດຕອນເຊື່ອມຕໍ່ຢູ່ → ເລືອກຫຸ່ນຍົນຈາກລາຍການ · ຫຼຸດແລ້ວກົດໃໝ່ → ເຊື່ອມຕໍ່ຫຸ່ນຍົນໂຕເດີມ
    if (!this.dev || this.dev.gatt.connected) {
      if (this.dev) this.dev.gatt.disconnect();
      const dev = await navigator.bluetooth.requestDevice({ filters: [{ services: [UART] }] }).catch((e) => {
        throw e.name === 'SecurityError' ? new Error('{{noBle}}') : e;
      });
      dev.addEventListener('gattserverdisconnected', () => {
        if (dev === this.dev) this.lost();
      });
      this.dev = dev;
    }
    const uart = await (await this.dev.gatt.connect()).getPrimaryService(UART);
    this.rx = await uart.getCharacteristic(TO_ROBOT);
    const tx = await uart.getCharacteristic(FROM_ROBOT);
    if (tx !== this.tx) tx.addEventListener('characteristicvaluechanged', () => this.textCb(new TextDecoder().decode(tx.value)));
    this.tx = tx;
    await tx.startNotifications();
    this.stateCb('on', this.dev.name);
  },
  lost() {
    this.rx = null;
    this.queue = [];
    this.stateCb('off');
  },
  //@ th=ส่งทีละข้อความ (Bluetooth ส่งซ้อนกันไม่ได้) · ค่าคันโยกที่รอคิวอยู่ ใช้ค่าล่าสุดแทน|en=One write at a time (Bluetooth cannot overlap writes) · a stick value still waiting is replaced by the newest|lo=ສົ່ງເທື່ອລະຂໍ້ຄວາມ (Bluetooth ສົ່ງຊ້ອນກັນບໍ່ໄດ້) · ຄ່າຄັນໂຍກທີ່ລໍຖ້າຢູ່ ໃຊ້ຄ່າລ່າສຸດແທນ
  write(text) {
    const q = this.queue, last = q[q.length - 1], isStick = (t) => Number(t) >= 1000;
    if (last === text || (isStick(last) && isStick(text))) q[q.length - 1] = text;
    else q.push(text);
    if (q.length > 10) q.shift();
    return this.pump();
  },
  async pump() {
    if (this.busy) return;
    this.busy = true;
    while (this.queue.length && this.rx) {
      const data = new TextEncoder().encode(this.queue.shift());
      try {
        if (this.rx.properties.writeWithoutResponse) await this.rx.writeValueWithoutResponse(data);
        else await this.rx.writeValue(data);
      } catch (e) {
        if (this.rx) log('info', e.message);
      }
    }
    this.busy = false;
  },
};
//@ th=เบราว์เซอร์นี้ไม่มี Bluetooth → บอกให้ใช้ Chrome หรือ Bluefy (รอให้สคริปต์ทั้งหน้าทำงานก่อน)|en=No Bluetooth in this browser → say to use Chrome or Bluefy (once the whole script has run)|lo=ບຣາວເຊີນີ້ບໍ່ມີ Bluetooth → ບອກໃຫ້ໃຊ້ Chrome ຫຼື Bluefy (ລໍໃຫ້ສະຄຣິບທັງໜ້າເຮັດວຽກກ່ອນ)
if (!navigator.bluetooth) setTimeout(() => log('info', '{{noBle}}'));

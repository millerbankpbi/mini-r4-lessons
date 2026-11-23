//@ th=คันโยก: ลากปุ่มกลมสีขาว · ส่งกำลังล้อเป็นเลขเดียวทุก 0.1 วินาที · ปล่อยครบแล้วส่ง S|en=Sticks: drag the white knob · wheel power is sent as one number every 0.1 s · letting go sends S|lo=ຄັນໂຍກ: ລາກປຸ່ມກົມສີຂາວ · ສົ່ງກຳລັງລໍ້ເປັນເລກດຽວທຸກ 0.1 ວິນາທີ · ປ່ອຍໝົດແລ້ວສົ່ງ S
//@ th=data-axis: xy = คันโยกเดียว, y = เดินหน้า/ถอย, x = เลี้ยว|en=data-axis: xy = one stick, y = forward/back, x = turn|lo=data-axis: xy = ຄັນໂຍກດຽວ, y = ເດີນໜ້າ/ຖອຍ, x = ລ້ຽວ
const joy = { x: 0, y: 0, held: 0, stop: null };
document.querySelectorAll('.stick').forEach((track) => {
  const knob = track.querySelector('b'), axis = track.dataset.axis;
  function drag(e) {
    const r = track.getBoundingClientRect();
    const rx = (r.width - knob.offsetWidth) / 2, ry = (r.height - knob.offsetHeight) / 2;
    let x = axis === 'y' ? 0 : (e.clientX - r.left - r.width / 2) / rx;
    let y = axis === 'x' ? 0 : (e.clientY - r.top - r.height / 2) / ry;
    const len = Math.hypot(x, y);
    if (len > 1) { x /= len; y /= len; }
    knob.style.transform = `translate(${x * rx}px, ${y * ry}px)`;
    //@ th=บนจอ y เพิ่มเมื่อลงล่าง แต่ดันขึ้น = เดินหน้า จึงกลับเครื่องหมาย|en=On screen y grows downward, but pushing up = forward, so flip the sign|lo=ເທິງຈໍ y ເພີ່ມເມື່ອລົງລຸ່ມ ແຕ່ດັນຂຶ້ນ = ເດີນໜ້າ ຈຶ່ງປີ້ນເຄື່ອງໝາຍ
    if (axis !== 'y') joy.x = x;
    if (axis !== 'x') joy.y = -y;
  }
  press(track, (e) => {
    drag(e);
    if (joy.held++ === 0) joy.stop = holdRepeat(() => pack(...mix(joy.x, joy.y, CONFIG.speed)), 100);
  }, () => {
    knob.style.transform = '';
    if (axis !== 'y') joy.x = 0;
    if (axis !== 'x') joy.y = 0;
    if (--joy.held === 0) joy.stop();
  }, drag);
});

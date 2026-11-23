//@ th=ปุ่ม 4 ทิศ: data-cmd คือข้อความที่ส่ง (F เดินหน้า, B ถอย, L เลี้ยวซ้าย, R เลี้ยวขวา)|en=4 direction buttons: data-cmd is the text sent (F forward, B back, L left, R right)|lo=ປຸ່ມ 4 ທິດ: data-cmd ແມ່ນຂໍ້ຄວາມທີ່ສົ່ງ (F ເດີນໜ້າ, B ຖອຍ, L ລ້ຽວຊ້າຍ, R ລ້ຽວຂວາ)
//@ th=tap4 = กด 1 ครั้ง ส่ง 1 ครั้ง · hold4 = กดค้างส่งซ้ำทุก 0.15 วินาที ปล่อยแล้วส่ง S|en=tap4 = one tap sends once · hold4 = holding sends again every 0.15 s, letting go sends S|lo=tap4 = ກົດ 1 ເທື່ອ ສົ່ງ 1 ເທື່ອ · hold4 = ກົດຄ້າງສົ່ງຊ້ຳທຸກ 0.15 ວິນາທີ ປ່ອຍແລ້ວສົ່ງ S
document.querySelectorAll('[data-cmd]').forEach((b) => {
  const cmd = b.dataset.cmd;
  if (CONFIG.mode === 'tap4') press(b, () => send(cmd));
  else {
    let stop = null;
    press(b, () => { stop = holdRepeat(cmd, 150); }, () => stop());
  }
});

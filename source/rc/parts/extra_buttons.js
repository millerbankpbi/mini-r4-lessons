//@ th=ปุ่มพิเศษ: กดแล้วส่ง data-press · ปล่อยแล้วส่ง data-release (ว่าง = ไม่ส่ง)|en=Extra buttons: pressing sends data-press · letting go sends data-release (empty = nothing)|lo=ປຸ່ມພິເສດ: ກົດແລ້ວສົ່ງ data-press · ປ່ອຍແລ້ວສົ່ງ data-release (ວ່າງ = ບໍ່ສົ່ງ)
document.querySelectorAll('.xbtn').forEach((b) => {
  press(b, () => send(b.dataset.press), () => send(b.dataset.release));
});

//@ th=หน้าต่างข้อความ: พิมพ์แล้วกดส่ง · ข้อความที่หุ่นตอบจะขึ้นตรงนี้|en=Terminal: type and send · the robot's answers show here|lo=ໜ້າຕ່າງຂໍ້ຄວາມ: ພິມແລ້ວກົດສົ່ງ · ຂໍ້ຄວາມທີ່ຫຸ່ນຍົນຕອບຈະຂຶ້ນຢູ່ນີ້
function termAdd(dir, text) {
  const box = $('#log'), last = box.lastElementChild;
  if (!text) return;
  //@ th=ข้อความเดิมซ้ำ → นับจำนวน ไม่ขึ้นบรรทัดใหม่|en=The same message again → count it instead of adding a line|lo=ຂໍ້ຄວາມເດີມຊ້ຳ → ນັບຈຳນວນ ບໍ່ຂຶ້ນແຖວໃໝ່
  if (last && last.className === dir && last.dataset.text === text) {
    last.dataset.n = Number(last.dataset.n) + 1;
    last.textContent = text + '  ×' + last.dataset.n;
    return;
  }
  const line = document.createElement('div');
  line.className = dir;
  line.dataset.text = text;
  line.dataset.n = 1;
  line.textContent = text;
  box.append(line);
  if (box.children.length > 100) box.firstElementChild.remove();
  box.scrollTop = box.scrollHeight;
}
$('#sendForm').addEventListener('submit', (e) => {
  e.preventDefault();
  send($('#msg').value);
  $('#msg').value = '';
});

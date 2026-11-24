# ข้อความหน้า "ติดตั้งโปรแกรม" 3 ภาษา  ({IMG} = โฟลเดอร์รูป, <div id="testCode"> = กล่องโค้ดทดสอบ)
def fig(name, w, h, alt):
    return '<figure class="shot"><img src="{IMG}' + name + '" width="' + str(w) + '" height="' + str(h) + '" loading="lazy" alt="' + alt + '"></figure>'

TH = dict(
  install='ติดตั้งโปรแกรม', installTitle='ติดตั้งโปรแกรม',
  installMore='ดูขั้นตอนละเอียดพร้อมรูป → ติดตั้งโปรแกรม',
  installHtml=(
    '<h1>ติดตั้งโปรแกรม: Arduino IDE · บอร์ด R4 · ไลบรารี MatrixMiniR4</h1>'
    '<p class="lead">ทำครั้งเดียวต่อคอมพิวเตอร์หนึ่งเครื่อง ใช้เวลาราว 10–20 นาที (ขึ้นกับความเร็วอินเทอร์เน็ต) เสร็จแล้วเครื่องนี้อัปโหลดโค้ดทุกบทในเว็บนี้ลงหุ่น Mini R4 ได้</p>'
    '<h2>ต้องมีอะไรบ้าง</h2><ul class="need">'
    '<li>คอมพิวเตอร์ Windows 10/11 หรือ macOS ที่ต่ออินเทอร์เน็ต</li>'
    '<li>หุ่น MATRIX Mini R4 กับสาย USB-C ที่ส่งข้อมูลได้ (สายสำหรับชาร์จอย่างเดียว คอมจะมองไม่เห็นหุ่น)</li>'
    '<li>ภาพในหน้านี้มาจาก Arduino IDE 2.3.6 รุ่นอื่นในเวอร์ชัน 2 หน้าตาใกล้เคียงกัน</li></ul>'
    '<h2>ขั้นตอน</h2><ol class="steps">'
    '<li><b>ดาวน์โหลดและติดตั้ง Arduino IDE 2</b> จาก <a href="https://www.arduino.cc/en/software" target="_blank" rel="noopener">arduino.cc/en/software</a> เลือกไฟล์ให้ตรงกับเครื่อง (Windows เลือกตัวติดตั้งสำหรับ Windows 10 ขึ้นไป) แล้วติดตั้งตามปกติ ถ้า Windows ถามว่าจะติดตั้งซอฟต์แวร์อุปกรณ์ (USB driver) ไหม ให้กด <b>Install</b> · เปิดโปรแกรมครั้งแรกอาจช้าสักพัก รอให้แถบด้านล่างโหลดเสร็จก่อน</li>'
    '<li><b>เปิดตัวจัดการบอร์ด (Boards Manager)</b> กดไอคอนรูปบอร์ด ① ที่แถบซ้าย (ไอคอนที่ 2 จากบน) จะมีช่องค้นหา ② ขึ้นมา หรือใช้เมนู Tools → Board → Boards Manager…'
    + fig('install-boards-manager.webp', 1060, 620, 'Arduino IDE: ไอคอนตัวจัดการบอร์ดที่แถบซ้าย (1) และช่องค้นหา (2)') + '</li>'
    '<li><b>ติดตั้งบอร์ด Arduino UNO R4</b> พิมพ์ <code>arduino r4</code> ในช่องค้นหา ① จะเจอ <b>Arduino UNO R4 Boards</b> by Arduino กด <b>INSTALL</b> ② แล้วรอจนมีป้ายสีเขียว “1.6.0 installed” (อาจใช้เวลาหลายนาที) ถ้า Windows ถามเรื่องไดรเวอร์ระหว่างนี้ ให้กด Install'
    + fig('install-uno-r4-boards.webp', 1060, 560, 'ค้นหา arduino r4 (1) แล้วกด INSTALL ที่ Arduino UNO R4 Boards (2)')
    + '<p class="warn">เว็บนี้ทดสอบกับรุ่น 1.6.0 ถ้ารุ่นที่ใหม่กว่าคอมไพล์โค้ดในบทเรียนไม่ผ่าน ให้เลือก 1.6.0 ในช่องเลือกรุ่นข้างปุ่ม INSTALL แล้วติดตั้งใหม่</p></li>'
    '<li><b>ติดตั้งไลบรารี MatrixMiniR4</b> กดไอคอนรูปหนังสือ ① (ไอคอนที่ 3 จากบน หรือเมนู Sketch → Include Library → Manage Libraries…) พิมพ์ <code>MatrixMiniR4</code> ในช่องค้นหา ② เลือก <b>MatrixMiniR4</b> by KKITC แล้วกด <b>INSTALL</b> ③ จะมีหน้าต่างถามว่าจะติดตั้งไลบรารีที่ต้องใช้ด้วยไหม (<b>ArduinoBLE</b> และ <b>PubSubClient</b>) ให้กด <b>INSTALL ALL</b> แล้วรอจนขึ้น “1.2.6 installed”'
    + fig('install-matrixminir4.webp', 1060, 580, 'ไอคอนตัวจัดการไลบรารี (1) ค้นหา MatrixMiniR4 (2) แล้วกด INSTALL (3)')
    + '<p class="warn">ถ้าเผลอกด INSTALL WITHOUT DEPENDENCIES ให้ค้น <code>ArduinoBLE</code> และ <code>PubSubClient</code> แล้วกด INSTALL ทีละตัว บทเรียนหน่วยที่ 6 (Bluetooth และ WiFi) ต้องใช้สองตัวนี้</p></li>'
    '<li><b>ต่อหุ่น แล้วเลือกบอร์ดกับพอร์ต</b> เสียบสาย USB-C จากหุ่นเข้าคอมพิวเตอร์ กดช่องเลือกบอร์ดด้านบน ① → <b>Select other board and port…</b> ฝั่ง BOARDS พิมพ์ <code>uno r4 wifi</code> เลือก <b>Arduino UNO R4 WiFi</b> ฝั่ง PORTS เลือกพอร์ตของหุ่น (Windows เป็น COM เช่น COM5 · macOS เป็น /dev/cu.usbmodem…) แล้วกด OK · หรือใช้เมนู Tools → Board → Arduino UNO R4 Boards → Arduino UNO R4 WiFi และ Tools → Port'
    + fig('install-toolbar.webp', 820, 182, 'ช่องเลือกบอร์ด (1) ปุ่มตรวจโค้ด (2) และปุ่มอัปโหลด (3) ที่แถบด้านบนของ Arduino IDE')
    + '<p class="warn">ต้องเลือก <b>UNO R4 WiFi</b> (ไม่ใช่ Minima) · ไม่รู้ว่าพอร์ตไหนคือหุ่น: ถอดสายแล้วดูว่าพอร์ตไหนหายไป เสียบกลับ พอร์ตที่โผล่มาคือหุ่น</p></li>'
    '<li><b>ทดสอบอัปโหลด: ตัวอย่าง “สวัสดี MATRIX”</b> โค้ดเบื้องต้นสำหรับโชว์ข้อความบนจอ ตั้งขนาดตัวอักษรครั้งเดียวใน <code>setup()</code> แล้วพิมพ์ 2 บรรทัด · กด File → New Sketch ลบโค้ดเดิมทั้งหมด วางโค้ดด้านล่าง (กดปุ่ม คัดลอก) กด ✓ Verify ② รอข้อความ “Done compiling” แล้วกด → Upload ③ รอ “Done uploading” · ถ้าจอ OLED ขึ้น <b>Hello</b> และ <b>MATRIX R4</b> สองบรรทัด แปลว่าติดตั้งครบ พร้อมเรียนแล้ว (ถ้าจอไม่ขึ้น ใส่แบตเตอรี่และเปิดสวิตช์หุ่นแล้วลองอีกครั้ง)<div id="testCode"></div><p>อยากรู้ว่าแต่ละบรรทัดทำอะไร ดูบท <a href="#u1-oled">จอ OLED: แสดงข้อความและตัวเลข</a></p></li>'
    '</ol>'
    '<h2>แก้ปัญหาที่พบบ่อย</h2><dl class="faq">'
    '<dt><code>MatrixMiniR4.h: No such file or directory</code></dt><dd>ยังไม่ได้ติดตั้งไลบรารี MatrixMiniR4 (ขั้นที่ 4) หรือเลือกบอร์ดผิด ต้องเป็น Arduino UNO R4 WiFi (ขั้นที่ 5)</dd>'
    '<dt><code>ArduinoBLE.h</code> หรือ <code>PubSubClient.h: No such file or directory</code></dt><dd>ติดตั้งไลบรารี ArduinoBLE และ PubSubClient เพิ่ม (ดูข้อควรรู้ในขั้นที่ 4)</dd>'
    '<dt>ไม่มีพอร์ตให้เลือก หรือขึ้น “No device found”</dt><dd>เปลี่ยนเป็นสายที่ส่งข้อมูลได้ ลองช่อง USB อื่น ถอดเสียบใหม่แล้วเลือกพอร์ตอีกครั้ง และปิดโปรแกรมอื่นที่อาจใช้พอร์ตอยู่ เช่น MATRIXblock หรือ Serial Monitor ในอีกหน้าต่าง</dd>'
    '<dt>ค้างที่ “Uploading…” นาน หรืออัปโหลดไม่สำเร็จ</dt><dd>ถอดสายเสียบใหม่ เลือกพอร์ตอีกครั้ง แล้วกดอัปโหลดใหม่</dd>'
    '<dt>ติดตั้งบอร์ดหรือไลบรารีไม่สำเร็จ (ดาวน์โหลดล้มเหลว)</dt><dd>อินเทอร์เน็ตของโรงเรียนอาจบล็อกเว็บดาวน์โหลด ลองต่อฮอตสปอตมือถือ แล้วกด INSTALL อีกครั้ง</dd>'
    '<dt>ไม่แน่ใจว่าติดตั้งแล้วหรือยัง</dt><dd>ค้นชื่อในตัวจัดการบอร์ดหรือตัวจัดการไลบรารี ถ้าติดตั้งแล้วจะมีป้ายสีเขียว “… installed”</dd>'
    '</dl>'
    '<p class="next">ติดตั้งเสร็จแล้ว ต่อไปดู <a href="#start">เริ่มต้น: ย้ายโค้ดจากบล็อกไป Arduino IDE</a></p>'
  ),
)

EN = dict(
  install='Install the software', installTitle='Install the software',
  installMore='Step-by-step with pictures → Install the software',
  installHtml=(
    '<h1>Install the software: Arduino IDE · R4 board · MatrixMiniR4 library</h1>'
    '<p class="lead">Do this once per computer. It takes about 10–20 minutes, depending on your internet speed. After that, this computer can upload every lesson on this site to the Mini R4 robot.</p>'
    '<h2>What you need</h2><ul class="need">'
    '<li>A Windows 10/11 or macOS computer with internet</li>'
    '<li>A MATRIX Mini R4 robot and a USB-C cable that carries data (a charge-only cable will not show the robot)</li>'
    '<li>The pictures on this page come from Arduino IDE 2.3.6; other version 2 releases look about the same</li></ul>'
    '<h2>Steps</h2><ol class="steps">'
    '<li><b>Download and install Arduino IDE 2</b> from <a href="https://www.arduino.cc/en/software" target="_blank" rel="noopener">arduino.cc/en/software</a>. Pick the file for your computer (on Windows, the installer for Windows 10 and newer) and install it as usual. If Windows asks whether to install device software (USB driver), press <b>Install</b>. The first start can be slow; wait until the bar at the bottom finishes loading.</li>'
    '<li><b>Open the Boards Manager</b>: press the board icon ① in the left bar (second icon from the top). A search box ② appears. You can also use Tools → Board → Boards Manager…'
    + fig('install-boards-manager.webp', 1060, 620, 'Arduino IDE: the Boards Manager icon in the left bar (1) and the search box (2)') + '</li>'
    '<li><b>Install the Arduino UNO R4 board</b>: type <code>arduino r4</code> in the search box ①. You will find <b>Arduino UNO R4 Boards</b> by Arduino. Press <b>INSTALL</b> ② and wait for the green “1.6.0 installed” label (this can take several minutes). If Windows asks about a driver meanwhile, press Install.'
    + fig('install-uno-r4-boards.webp', 1060, 560, 'Search for arduino r4 (1), then press INSTALL on Arduino UNO R4 Boards (2)')
    + '<p class="warn">This site was tested with version 1.6.0. If a newer version fails to compile the lesson code, pick 1.6.0 in the version box next to INSTALL and install again.</p></li>'
    '<li><b>Install the MatrixMiniR4 library</b>: press the book icon ① (third icon from the top, or Sketch → Include Library → Manage Libraries…). Type <code>MatrixMiniR4</code> in the search box ②, pick <b>MatrixMiniR4</b> by KKITC and press <b>INSTALL</b> ③. A window asks whether to install the libraries it needs as well (<b>ArduinoBLE</b> and <b>PubSubClient</b>): press <b>INSTALL ALL</b> and wait for “1.2.6 installed”.'
    + fig('install-matrixminir4.webp', 1060, 580, 'The Library Manager icon (1), search for MatrixMiniR4 (2), then press INSTALL (3)')
    + '<p class="warn">If you pressed INSTALL WITHOUT DEPENDENCIES by mistake, search for <code>ArduinoBLE</code> and <code>PubSubClient</code> and install each one. Unit 6 (Bluetooth and WiFi) needs both.</p></li>'
    '<li><b>Connect the robot, then choose the board and port</b>: plug the robot’s USB-C cable into the computer. Press the board box at the top ① → <b>Select other board and port…</b>. Under BOARDS type <code>uno r4 wifi</code> and pick <b>Arduino UNO R4 WiFi</b>; under PORTS pick the robot’s port (COM on Windows, such as COM5 · /dev/cu.usbmodem… on macOS), then press OK. You can also use Tools → Board → Arduino UNO R4 Boards → Arduino UNO R4 WiFi and Tools → Port.'
    + fig('install-toolbar.webp', 820, 182, 'The board box (1), the Verify button (2) and the Upload button (3) at the top of Arduino IDE')
    + '<p class="warn">Choose <b>UNO R4 WiFi</b> (not Minima). Not sure which port is the robot? Unplug the cable and see which port disappears; plug it back in and the port that appears is the robot.</p></li>'
    '<li><b>Test an upload: the “Hello MATRIX” example</b>, a first sketch that shows text on the screen. It sets the text size once in <code>setup()</code>, then prints 2 lines. Press File → New Sketch, delete all the code, paste the code below (press Copy), press ✓ Verify ② and wait for “Done compiling”, then press → Upload ③ and wait for “Done uploading”. If the OLED screen shows <b>Hello</b> and <b>MATRIX R4</b> on two lines, everything is installed and you are ready to learn. (If the screen stays blank, put in the battery, switch the robot on and try again.)<div id="testCode"></div><p>To learn what each line does, see the lesson <a href="#u1-oled">OLED screen: showing text and numbers</a>.</p></li>'
    '</ol>'
    '<h2>Common problems</h2><dl class="faq">'
    '<dt><code>MatrixMiniR4.h: No such file or directory</code></dt><dd>The MatrixMiniR4 library is not installed (step 4), or the wrong board is chosen; it must be Arduino UNO R4 WiFi (step 5).</dd>'
    '<dt><code>ArduinoBLE.h</code> or <code>PubSubClient.h: No such file or directory</code></dt><dd>Install the ArduinoBLE and PubSubClient libraries (see the note in step 4).</dd>'
    '<dt>No port to choose, or “No device found”</dt><dd>Use a cable that carries data, try another USB socket, unplug and plug in again and choose the port again, and close other programs that may hold the port, such as MATRIXblock or a Serial Monitor in another window.</dd>'
    '<dt>Stuck at “Uploading…” or the upload fails</dt><dd>Unplug and plug in the cable, choose the port again, then upload again.</dd>'
    '<dt>Installing the board or library fails (download failed)</dt><dd>The school internet may block the download site. Try a phone hotspot, then press INSTALL again.</dd>'
    '<dt>Not sure whether it is installed</dt><dd>Search for the name in the Boards Manager or Library Manager. Installed items show a green “… installed” label.</dd>'
    '</dl>'
    '<p class="next">All installed? Next, see <a href="#start">Getting started: from blocks to Arduino IDE</a></p>'
  ),
)

LO = dict(
  install='ຕິດຕັ້ງໂປຣແກຣມ', installTitle='ຕິດຕັ້ງໂປຣແກຣມ',
  installMore='ເບິ່ງຂັ້ນຕອນລະອຽດພ້ອມຮູບ → ຕິດຕັ້ງໂປຣແກຣມ',
  installHtml=(
    '<h1>ຕິດຕັ້ງໂປຣແກຣມ: Arduino IDE · ບອດ R4 · ຫ້ອງສະໝຸດ MatrixMiniR4</h1>'
    '<p class="lead">ເຮັດເທື່ອດຽວຕໍ່ຄອມພິວເຕີໜຶ່ງເຄື່ອງ ໃຊ້ເວລາປະມານ 10–20 ນາທີ (ຂຶ້ນກັບຄວາມໄວອິນເຕີເນັດ) ເມື່ອເຮັດແລ້ວ ເຄື່ອງນີ້ອັບໂຫຼດໂຄ້ດທຸກບົດໃນເວັບນີ້ລົງຫຸ່ນຍົນ Mini R4 ໄດ້</p>'
    '<h2>ຕ້ອງມີຫຍັງແດ່</h2><ul class="need">'
    '<li>ຄອມພິວເຕີ Windows 10/11 ຫຼື macOS ທີ່ຕໍ່ອິນເຕີເນັດ</li>'
    '<li>ຫຸ່ນຍົນ MATRIX Mini R4 ກັບສາຍ USB-C ທີ່ສົ່ງຂໍ້ມູນໄດ້ (ສາຍສຳລັບສາກໄຟຢ່າງດຽວ ຄອມຈະເບິ່ງບໍ່ເຫັນຫຸ່ນຍົນ)</li>'
    '<li>ຮູບໃນໜ້ານີ້ມາຈາກ Arduino IDE 2.3.6 ລຸ້ນອື່ນໃນເວີຊັນ 2 ໜ້າຕາໃກ້ຄຽງກັນ</li></ul>'
    '<h2>ຂັ້ນຕອນ</h2><ol class="steps">'
    '<li><b>ດາວໂຫຼດ ແລະ ຕິດຕັ້ງ Arduino IDE 2</b> ຈາກ <a href="https://www.arduino.cc/en/software" target="_blank" rel="noopener">arduino.cc/en/software</a> ເລືອກໄຟລ໌ໃຫ້ກົງກັບເຄື່ອງ (Windows ເລືອກຕົວຕິດຕັ້ງສຳລັບ Windows 10 ຂຶ້ນໄປ) ແລ້ວຕິດຕັ້ງຕາມປົກກະຕິ ຖ້າ Windows ຖາມວ່າຈະຕິດຕັ້ງຊອບແວອຸປະກອນ (USB driver) ບໍ່ ໃຫ້ກົດ <b>Install</b> · ເປີດໂປຣແກຣມເທື່ອທຳອິດອາດຊ້າໄລຍະໜຶ່ງ ລໍໃຫ້ແຖບທາງລຸ່ມໂຫຼດແລ້ວກ່ອນ</li>'
    '<li><b>ເປີດຕົວຈັດການບອດ (Boards Manager)</b> ກົດໄອຄອນຮູບບອດ ① ທີ່ແຖບຊ້າຍ (ໄອຄອນທີ 2 ຈາກເທິງ) ຈະມີຊ່ອງຄົ້ນຫາ ② ຂຶ້ນມາ ຫຼື ໃຊ້ເມນູ Tools → Board → Boards Manager…'
    + fig('install-boards-manager.webp', 1060, 620, 'Arduino IDE: ໄອຄອນຕົວຈັດການບອດທີ່ແຖບຊ້າຍ (1) ແລະ ຊ່ອງຄົ້ນຫາ (2)') + '</li>'
    '<li><b>ຕິດຕັ້ງບອດ Arduino UNO R4</b> ພິມ <code>arduino r4</code> ໃນຊ່ອງຄົ້ນຫາ ① ຈະພົບ <b>Arduino UNO R4 Boards</b> by Arduino ກົດ <b>INSTALL</b> ② ແລ້ວລໍຈົນມີປ້າຍສີຂຽວ “1.6.0 installed” (ອາດໃຊ້ເວລາຫຼາຍນາທີ) ຖ້າ Windows ຖາມເລື່ອງໄດຣເວີລະຫວ່າງນີ້ ໃຫ້ກົດ Install'
    + fig('install-uno-r4-boards.webp', 1060, 560, 'ຄົ້ນຫາ arduino r4 (1) ແລ້ວກົດ INSTALL ທີ່ Arduino UNO R4 Boards (2)')
    + '<p class="warn">ເວັບນີ້ທົດສອບກັບລຸ້ນ 1.6.0 ຖ້າລຸ້ນໃໝ່ກວ່າຄອມໄພລ໌ໂຄ້ດໃນບົດຮຽນບໍ່ຜ່ານ ໃຫ້ເລືອກ 1.6.0 ໃນຊ່ອງເລືອກລຸ້ນຂ້າງປຸ່ມ INSTALL ແລ້ວຕິດຕັ້ງໃໝ່</p></li>'
    '<li><b>ຕິດຕັ້ງຫ້ອງສະໝຸດ MatrixMiniR4</b> ກົດໄອຄອນຮູບປຶ້ມ ① (ໄອຄອນທີ 3 ຈາກເທິງ ຫຼື ເມນູ Sketch → Include Library → Manage Libraries…) ພິມ <code>MatrixMiniR4</code> ໃນຊ່ອງຄົ້ນຫາ ② ເລືອກ <b>MatrixMiniR4</b> by KKITC ແລ້ວກົດ <b>INSTALL</b> ③ ຈະມີໜ້າຕ່າງຖາມວ່າຈະຕິດຕັ້ງຫ້ອງສະໝຸດທີ່ຕ້ອງໃຊ້ນຳບໍ່ (<b>ArduinoBLE</b> ແລະ <b>PubSubClient</b>) ໃຫ້ກົດ <b>INSTALL ALL</b> ແລ້ວລໍຈົນຂຶ້ນ “1.2.6 installed”'
    + fig('install-matrixminir4.webp', 1060, 580, 'ໄອຄອນຕົວຈັດການຫ້ອງສະໝຸດ (1) ຄົ້ນຫາ MatrixMiniR4 (2) ແລ້ວກົດ INSTALL (3)')
    + '<p class="warn">ຖ້າເຜີກົດ INSTALL WITHOUT DEPENDENCIES ໃຫ້ຄົ້ນຫາ <code>ArduinoBLE</code> ແລະ <code>PubSubClient</code> ແລ້ວກົດ INSTALL ເທື່ອລະໂຕ ບົດຮຽນໜ່ວຍທີ 6 (Bluetooth ແລະ WiFi) ຕ້ອງໃຊ້ທັງສອງໂຕນີ້</p></li>'
    '<li><b>ຕໍ່ຫຸ່ນຍົນ ແລ້ວເລືອກບອດກັບພອດ</b> ສຽບສາຍ USB-C ຈາກຫຸ່ນຍົນເຂົ້າຄອມພິວເຕີ ກົດຊ່ອງເລືອກບອດທາງເທິງ ① → <b>Select other board and port…</b> ຝັ່ງ BOARDS ພິມ <code>uno r4 wifi</code> ເລືອກ <b>Arduino UNO R4 WiFi</b> ຝັ່ງ PORTS ເລືອກພອດຂອງຫຸ່ນຍົນ (Windows ເປັນ COM ເຊັ່ນ COM5 · macOS ເປັນ /dev/cu.usbmodem…) ແລ້ວກົດ OK · ຫຼື ໃຊ້ເມນູ Tools → Board → Arduino UNO R4 Boards → Arduino UNO R4 WiFi ແລະ Tools → Port'
    + fig('install-toolbar.webp', 820, 182, 'ຊ່ອງເລືອກບອດ (1) ປຸ່ມກວດໂຄ້ດ (2) ແລະ ປຸ່ມອັບໂຫຼດ (3) ທີ່ແຖບທາງເທິງຂອງ Arduino IDE')
    + '<p class="warn">ຕ້ອງເລືອກ <b>UNO R4 WiFi</b> (ບໍ່ແມ່ນ Minima) · ບໍ່ຮູ້ວ່າພອດໃດແມ່ນຫຸ່ນຍົນ: ຖອດສາຍແລ້ວເບິ່ງວ່າພອດໃດຫາຍໄປ ສຽບຄືນ ພອດທີ່ໂຜ່ຂຶ້ນມາແມ່ນຫຸ່ນຍົນ</p></li>'
    '<li><b>ທົດສອບອັບໂຫຼດ: ຕົວຢ່າງ “ສະບາຍດີ MATRIX”</b> ໂຄ້ດເບື້ອງຕົ້ນສຳລັບສະແດງຂໍ້ຄວາມເທິງຈໍ ຕັ້ງຂະໜາດຕົວອັກສອນເທື່ອດຽວໃນ <code>setup()</code> ແລ້ວພິມ 2 ແຖວ · ກົດ File → New Sketch ລຶບໂຄ້ດເດີມອອກທັງໝົດ ວາງໂຄ້ດທາງລຸ່ມ (ກົດປຸ່ມ ສຳເນົາ) ກົດ ✓ Verify ② ລໍຂໍ້ຄວາມ “Done compiling” ແລ້ວກົດ → Upload ③ ລໍ “Done uploading” · ຖ້າຈໍ OLED ຂຶ້ນ <b>Hello</b> ແລະ <b>MATRIX R4</b> ສອງແຖວ ແປວ່າຕິດຕັ້ງຄົບແລ້ວ ພ້ອມຮຽນ (ຖ້າຈໍບໍ່ຂຶ້ນ ໃສ່ແບັດເຕີຣີ ແລະ ເປີດສະວິດຫຸ່ນຍົນ ແລ້ວລອງອີກເທື່ອ)<div id="testCode"></div><p>ຢາກຮູ້ວ່າແຕ່ລະແຖວເຮັດຫຍັງ ເບິ່ງບົດ <a href="#u1-oled">ໜ້າຈໍ OLED: ສະແດງຂໍ້ຄວາມ ແລະ ຕົວເລກ</a></p></li>'
    '</ol>'
    '<h2>ແກ້ບັນຫາທີ່ພົບເລື້ອຍ</h2><dl class="faq">'
    '<dt><code>MatrixMiniR4.h: No such file or directory</code></dt><dd>ຍັງບໍ່ໄດ້ຕິດຕັ້ງຫ້ອງສະໝຸດ MatrixMiniR4 (ຂັ້ນທີ 4) ຫຼື ເລືອກບອດຜິດ ຕ້ອງເປັນ Arduino UNO R4 WiFi (ຂັ້ນທີ 5)</dd>'
    '<dt><code>ArduinoBLE.h</code> ຫຼື <code>PubSubClient.h: No such file or directory</code></dt><dd>ຕິດຕັ້ງຫ້ອງສະໝຸດ ArduinoBLE ແລະ PubSubClient ເພີ່ມ (ເບິ່ງຂໍ້ຄວນຮູ້ໃນຂັ້ນທີ 4)</dd>'
    '<dt>ບໍ່ມີພອດໃຫ້ເລືອກ ຫຼື ຂຶ້ນ “No device found”</dt><dd>ປ່ຽນເປັນສາຍທີ່ສົ່ງຂໍ້ມູນໄດ້ ລອງຊ່ອງ USB ອື່ນ ຖອດສຽບໃໝ່ແລ້ວເລືອກພອດອີກເທື່ອ ແລະ ປິດໂປຣແກຣມອື່ນທີ່ອາດໃຊ້ພອດຢູ່ ເຊັ່ນ MATRIXblock ຫຼື Serial Monitor ໃນອີກໜ້າຕ່າງ</dd>'
    '<dt>ຄ້າງຢູ່ “Uploading…” ດົນ ຫຼື ອັບໂຫຼດບໍ່ສຳເລັດ</dt><dd>ຖອດສາຍສຽບໃໝ່ ເລືອກພອດອີກເທື່ອ ແລ້ວກົດອັບໂຫຼດໃໝ່</dd>'
    '<dt>ຕິດຕັ້ງບອດ ຫຼື ຫ້ອງສະໝຸດບໍ່ສຳເລັດ (ດາວໂຫຼດລົ້ມເຫຼວ)</dt><dd>ອິນເຕີເນັດຂອງໂຮງຮຽນອາດບລັອກເວັບດາວໂຫຼດ ລອງຕໍ່ຮັອດສະປອດມືຖື ແລ້ວກົດ INSTALL ອີກເທື່ອ</dd>'
    '<dt>ບໍ່ແນ່ໃຈວ່າຕິດຕັ້ງແລ້ວຫຼືຍັງ</dt><dd>ຄົ້ນຫາຊື່ໃນຕົວຈັດການບອດ ຫຼື ຕົວຈັດການຫ້ອງສະໝຸດ ຖ້າຕິດຕັ້ງແລ້ວຈະມີປ້າຍສີຂຽວ “… installed”</dd>'
    '</dl>'
    '<p class="next">ຕິດຕັ້ງແລ້ວ ຕໍ່ໄປເບິ່ງ <a href="#start">ເລີ່ມຕົ້ນ: ຍ້າຍໂຄ້ດຈາກບລັອກໄປ Arduino IDE</a></p>'
  ),
)

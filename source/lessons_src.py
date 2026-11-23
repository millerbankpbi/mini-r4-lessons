# เนื้อหาบทเรียน: บล็อกใน MATRIXblock Mini R4 คู่กับโค้ด Arduino (MatrixMiniR4.h)
# ทุกตัวอย่างเขียนเป็นโปรแกรมบล็อก แล้วให้ตัวสร้างโค้ดของโปรแกรม MATRIXblock เองแปลงเป็น C++ ตอน build
import os
from xmlkit import *

UNITS = [
  dict(id=1, title='R4 Core · Movement · Looks', sub='บอร์ด มอเตอร์ การเคลื่อนที่ ไฟ เสียง จอ', color='#00878F'),
  dict(id=2, title='Sensing', sub='IMU · Grayscale · Potentiometer · Color V3 · Laser V2', color='#5cb1d6', soon=True),
  dict(id=3, title='Control', sub='รอ · ถ้า · ทำซ้ำ · จับเวลา', color='#FFAB19'),
  dict(id=4, title='Operators · Variables', sub='คำนวณ · เปรียบเทียบ · ตัวแปร · ข้อความ', color='#40BF4A'),
  dict(id=5, title='My Blocks', sub='สร้างบล็อกของตัวเอง = ฟังก์ชัน', color='#FF6680', soon=True),
  dict(id=6, title='บังคับหุ่นผ่านมือถือ', sub='Bluetooth · WiFi · MQTT', color='#7A5CD6'),
]

L = []

# =====================================================================
# หน่วยที่ 1
# =====================================================================
L.append(dict(id='u1-begin', unit=1, cat='core', title='โครงโปรแกรม: R4 Begin = setup + loop',
  goals=['รู้ว่าบล็อก R4 Begin กลายเป็นโค้ดส่วนไหน', 'แยกได้ว่าคำสั่งไหนควรอยู่ Setup คำสั่งไหนควรอยู่ Loop'],
  intro='ทุกโปรแกรมใน MATRIXblock เริ่มที่บล็อก <b>R4 Begin</b> เสมอ ลองดูโค้ดด้านขวาของโปรแกรม จะเห็นว่าบล็อกเดียวนี้สร้างโครงโปรแกรม Arduino ให้ครบทั้งไฟล์',
  blocks=['mini_setup'],
  examples=[
    dict(title='โปรแกรมว่าง', desc='ยังไม่มีบล็อกอื่นเลย แต่ได้โค้ดครบโครงแล้ว ชี้ที่บล็อกหรือบรรทัดโค้ดเพื่อดูว่าคู่กันตรงไหน',
         xml=P(),
         notes=[('#include "MatrixMiniR4.h"', 'ดึงไลบรารีของบอร์ดเข้ามา ทำให้ใช้คำว่า <code>MiniR4</code> ได้ ถ้าเขียนใน Arduino IDE เองต้องมีบรรทัดนี้เสมอ'),
                ('void setup()', 'ทำครั้งเดียวตอนเปิดเครื่องหรือกดรีเซ็ต'),
                ('MiniR4.begin();', 'เตรียมบอร์ดทั้งหมด (มอเตอร์ จอ ไฟ ปุ่ม) ต้องมาก่อนคำสั่งอื่น'),
                ('MiniR4.PWR.setBattCell(2);', 'บอกว่าใช้ถ่าน 18650 สองก้อน'),
                ('Serial.begin(9600);', 'เปิดช่องส่งข้อความเข้าคอม (UART: On)'),
                ('void loop()', 'ทำซ้ำไปเรื่อย ๆ ตลอดเวลาที่บอร์ดเปิดอยู่')]),
    dict(title='Setup กับ Loop ต่างกันอย่างไร', desc='ไฟเขียวติดครั้งเดียวตอนเริ่ม ส่วนเสียงบี๊บดังซ้ำทุก 1 วินาที',
         xml=P(setup=[led(0, 80, 0)], loop=[B('mini_Buzzer_Tone', v={'FREQ': 880, 'VOL': 100}), wait(1000)]),
         notes=[('MiniR4.LED.setColor(1, 0, 80, 0);', 'บล็อกใน Setup ไปต่อท้ายใน <code>setup()</code> หลังคำสั่งเตรียมบอร์ด'),
                ('delay(1000);', 'บล็อกใน Loop อยู่ใน <code>loop()</code> วนไปเรื่อย ๆ')]),
  ],
  arduino=['ทุกคำสั่งใน C++ จบด้วยเครื่องหมาย <code>;</code>', 'ปีกกา <code>{ }</code> บอกว่าคำสั่งไหนอยู่ในส่วนไหน คล้ายช่องของบล็อก',
           '<code>MiniR4.LED.setColor(…)</code> อ่านว่า “บอร์ด MiniR4 → ส่วน LED → คำสั่ง setColor” จุดคือการเข้าไปในส่วนย่อย'],
  tries=[dict(task='ตั้ง UART เป็น <b>Off</b> แล้วดูว่าบรรทัดไหนในโค้ดหายไป',
              solution=P(uart='0'), answer='บรรทัด <code>Serial.begin(9600);</code> หายไป เพราะไม่ได้เปิด Serial'),
         dict(task='เปลี่ยนเป็นถ่าน 18650 สามก้อน (18650x3) โค้ดเปลี่ยนตรงไหน',
              solution=P(aa='3'), answer='<code>MiniR4.PWR.setBattCell(3);</code>')],
  quiz=[dict(q='ถ้าอยากให้ไฟติดครั้งเดียวตอนเปิดเครื่อง ควรวางบล็อกไว้ที่ไหน', choices=['ช่อง Setup', 'ช่อง Loop', 'วางนอก R4 Begin'], answer=0,
             why='Setup ทำครั้งเดียว ส่วนบล็อกที่วางนอก R4 Begin จะไม่ถูกแปลงเป็นโค้ดเลย'),
        dict(q='บรรทัดใดต้องมีเสมอเมื่อเขียนโค้ดเองใน Arduino IDE เพื่อใช้คำสั่ง MiniR4', choices=['#include "MatrixMiniR4.h"', 'Serial.begin(9600);', 'delay(1000);'], answer=0,
             why='ถ้าไม่ include ไลบรารี คอมไพเลอร์จะไม่รู้จัก MiniR4'),
        dict(q='ในหนึ่งโปรแกรมมีบล็อก R4 Begin ได้กี่อัน', choices=['1 อัน', '2 อัน (Setup กับ Loop)', 'กี่อันก็ได้'], answer=0,
             why='โปรแกรมเตือนว่าใส่ได้อันเดียว มีสองอันจะทำงานผิดปกติ')]))

L.append(dict(id='u1-led', unit=1, cat='looks', title='ไฟ RGB LED และการกระพริบ',
  goals=['ผสมสีด้วยค่า R G B', 'ทำไฟกระพริบด้วย wait และอ่านเป็น delay() ในโค้ด'],
  intro='บอร์ด Mini R4 มีไฟ RGB สองดวง (LED1, LED2) แต่ละดวงผสมแสง <b style="color:#d33">แดง</b> <b style="color:#2a2">เขียว</b> <b style="color:#36c">น้ำเงิน</b> ได้ 0–255 บทนี้ใช้บล็อก <b>wait</b> จากหมวด Control ด้วย (เรียนละเอียดในหน่วยที่ 3)',
  blocks=['mini_setRGB', 'control_wait'],
  examples=[
    dict(title='ไฟกระพริบสีแดง', desc='ติด 0.5 วินาที ดับ 0.5 วินาที วนไปเรื่อย ๆ',
         xml=P(loop=[led(255, 0, 0), wait(500), led(0, 0, 0), wait(500)]),
         notes=[('MiniR4.LED.setColor(1, 255, 0, 0);', 'ตัวเลขเรียงตามบล็อก: ดวงที่ 1, R=255, G=0, B=0'),
                ('MiniR4.LED.setColor(1, 0, 0, 0);', 'ทุกสีเป็น 0 = ดับ'),
                ('delay(500);', 'รอ 500 ms = ครึ่งวินาที')]),
    dict(title='ไฟจราจรสองดวง', desc='LED1 เขียว LED2 แดง แล้วสลับกันทุก 2 วินาที',
         xml=P(loop=[led(0, 255, 0, 1), led(255, 0, 0, 2), wait(2000), led(255, 0, 0, 1), led(0, 255, 0, 2), wait(2000)])),
  ],
  arduino=['เลขตัวแรกใน <code>setColor</code> คือดวงไฟ (1 หรือ 2) ไม่ใช่ความสว่าง', 'ลองเปลี่ยนตัวเลขในโค้ดแทนการลากบล็อกใหม่ เร็วกว่าเมื่อชินแล้ว'],
  tries=[dict(task='ทำไฟสีม่วง (แดงผสมน้ำเงิน) กระพริบเร็วขึ้นเป็นทุก 0.2 วินาที',
              solution=P(loop=[led(255, 0, 255), wait(200), led(0, 0, 0), wait(200)]), answer='สีม่วงคือ R=255 G=0 B=255 และ delay(200)'),
         dict(task='ไฟเปลี่ยนสี แดง → เขียว → น้ำเงิน สีละ 1 วินาที',
              solution=P(loop=[led(255, 0, 0), wait(1000), led(0, 255, 0), wait(1000), led(0, 0, 255), wait(1000)]))],
  quiz=[dict(q='MiniR4.LED.setColor(2, 0, 0, 255); ทำให้เกิดอะไร', choices=['LED2 เป็นสีน้ำเงิน', 'LED1 สว่าง 2 เท่า', 'LED2 เป็นสีแดง'], answer=0, why='เลข 2 คือดวงที่ 2 แล้ว R=0 G=0 B=255'),
        dict(q='ถ้าเอา wait ออกทั้งหมดจากตัวอย่างไฟกระพริบ จะเห็นอะไร', choices=['ไฟเหมือนติดค้างหรี่ ๆ เพราะสลับเร็วมาก', 'ไฟกระพริบช้าลง', 'คอมไพล์ไม่ผ่าน'], answer=0, why='บอร์ดสลับติด-ดับเร็วจนตามองไม่ทัน')]))

L.append(dict(id='u1-buzzer', unit=1, cat='looks', title='เสียง: Buzzer ความถี่และโน้ต',
  goals=['สั่งเสียงด้วยความถี่และด้วยชื่อโน้ต', 'เข้าใจว่าคำสั่งเสียงไม่รอ จึงต้องใส่ wait'],
  intro='Buzzer บนบอร์ดเล่นเสียงได้ทั้งแบบระบุความถี่ (Hz) และเลือกโน้ตดนตรี คำสั่งเสียงเป็นแบบ<b>ไม่รอ</b> สั่งแล้วโปรแกรมไปต่อทันที',
  blocks=['mini_Buzzer_Tone', 'mini_Buzzer_ToneNote', 'mini_Buzzer_NoTone'],
  examples=[
    dict(title='โด เร มี', desc='เล่นโน้ตละ 300 ms แล้วรอให้จบก่อนเล่นตัวถัดไป',
         xml=P(setup=[B('mini_Buzzer_ToneNote', f={'FREQ': 'NOTE_C4'}, v={'VOL': 300}), wait(350),
                      B('mini_Buzzer_ToneNote', f={'FREQ': 'NOTE_D4'}, v={'VOL': 300}), wait(350),
                      B('mini_Buzzer_ToneNote', f={'FREQ': 'NOTE_E4'}, v={'VOL': 300}), wait(350)]),
         notes=[('MiniR4.Buzzer.Tone(NOTE_C4, 300);', '<code>NOTE_C4</code> คือชื่อแทนตัวเลข 262 Hz ช่องที่สองคือเวลาเป็น ms'),
                ('delay(350);', 'รอให้เสียงจบ (300) และเว้นช่วงอีกนิด ถ้าไม่รอ โน้ตจะทับกันจนได้ยินแค่ตัวสุดท้าย')]),
    dict(title='ไซเรน', desc='เสียงสูง-ต่ำสลับกัน',
         xml=P(loop=[B('mini_Buzzer_Tone', v={'FREQ': 988, 'VOL': 250}), wait(250), B('mini_Buzzer_Tone', v={'FREQ': 659, 'VOL': 250}), wait(250)])),
  ],
  arduino=['<code>MiniR4.Buzzer.Tone(ความถี่, เวลา)</code> ใช้คำสั่ง <code>tone()</code> ของ Arduino อยู่ข้างใน', 'ความถี่สองเท่า = โน้ตเดียวกันแต่สูงขึ้น 1 ช่วงเสียง (C4 262 Hz, C5 523 Hz)'],
  tries=[dict(task='เล่นโน้ต C4 D4 E4 F4 G4 ไล่ขึ้น โน้ตละ 200 ms ครั้งเดียวตอนเปิดเครื่อง',
              solution=P(setup=[x for n in ['C4', 'D4', 'E4', 'F4', 'G4'] for x in (B('mini_Buzzer_ToneNote', f={'FREQ': 'NOTE_' + n}, v={'VOL': 200}), wait(250))])),
         dict(task='ทำเสียงเตือนติ๊ด ๆ สองครั้งแล้วเงียบ 1 วินาที วนไปเรื่อย ๆ',
              solution=P(loop=[B('mini_Buzzer_Tone', v={'FREQ': 2000, 'VOL': 80}), wait(150), B('mini_Buzzer_Tone', v={'FREQ': 2000, 'VOL': 80}), wait(150), wait(1000)]))],
  quiz=[dict(q='สั่ง Tone สามบรรทัดติดกันโดยไม่มี delay จะได้ยินอะไร', choices=['ได้ยินเกือบแค่โน้ตสุดท้าย', 'ได้ยินครบสามโน้ต', 'ไม่มีเสียง'], answer=0, why='คำสั่งไม่รอ โน้ตใหม่มาทับโน้ตเก่าทันที'),
        dict(q='NOTE_C4 ในโค้ดคืออะไร', choices=['ชื่อแทนตัวเลขความถี่ของโน้ตโด', 'ชื่อไฟล์เสียง', 'ช่องเสียบ C4'], answer=0, why='เป็นค่าคงที่ที่กำหนดไว้แล้วในไลบรารี')]))

L.append(dict(id='u1-oled', unit=1, cat='looks', title='จอ OLED: แสดงข้อความและตัวเลข',
  goals=['พิมพ์ข้อความลงจอที่ตำแหน่ง x, y', 'เข้าใจว่าบล็อกเดียวเป็นโค้ด 3 บรรทัด และใช้ Update ให้จอไม่กระพริบ'],
  intro='จอ OLED บนบอร์ดขนาด 128 × 32 จุด จุด (0, 0) อยู่มุมซ้ายบน x เพิ่มไปทางขวา y เพิ่มลงล่าง',
  blocks=['mini_OLED_clear', 'mini_OLED_printEASY', 'mini_OLED_setTextSize', 'mini_OLED_setTextColor'],
  examples=[
    dict(title='สวัสดี MATRIX', desc='ตั้งขนาดตัวอักษรครั้งเดียวใน Setup แล้วพิมพ์ 2 บรรทัด',
         xml=P(setup=[oled_size(1), oled_clear(), oled_print('Hello', 0, 0, 'No'), oled_print('MATRIX R4', 0, 16, 'Yes')]),
         notes=[('MiniR4.OLED.setCursor(0, 0);', 'ย้ายตำแหน่งเขียนไปที่ x=0, y=0'),
                ('MiniR4.OLED.print("Hello");', 'วาดข้อความลงหน่วยความจำของจอ ยังไม่ขึ้นจริง'),
                ('MiniR4.OLED.display();', 'ส่งภาพทั้งหมดขึ้นจอ บรรทัดนี้มีเมื่อเลือก Update: Yes เท่านั้น')]),
    dict(title='นับเลขบนจอ', desc='ใช้ตัวแปร <code>count</code> (เรียนในหน่วยที่ 4) ล้างจอก่อนพิมพ์ทุกครั้ง ตัวเลขจะไม่ซ้อนกัน',
         xml=P(setup=[oled_size(3), setvar('count', '0')],
               loop=[oled_clear(), oled_print(VAR('count'), 0, 0), changevar('count', 1), wait(1000)]),
         vars=['count'],
         notes=[('MiniR4.OLED.clearDisplay();', 'ล้างภาพเก่า ถ้าไม่ล้าง เลข 10 จะทับเลข 9 จนอ่านไม่ออก'),
                ('float count;', 'ตัวแปรจากบล็อกเป็นชนิด float จึงแสดงเป็น 0.00, 1.00 …')]),
  ],
  arduino=['<code>print</code> แสดงทศนิยม 2 ตำแหน่งเมื่อเป็น float ถ้าอยากได้เลขเต็มใช้ <code>MiniR4.OLED.print((int)count);</code> ใน Arduino IDE',
           'ตัวอักษรขนาด 1 สูง 8 จุด ขนาด 2 สูง 16 จุด ขนาด 3 สูง 24 จุด'],
  tries=[dict(task='แสดงชื่อเล่นตัวเองขนาด 2 ที่มุมซ้ายบน และเลขที่ด้านล่าง ขนาด 1',
              solution=P(setup=[oled_clear(), oled_size(2), oled_print('BANK', 0, 0, 'No'), oled_size(1), oled_print('No. 7', 0, 24, 'Yes')])),
         dict(task='ทำข้อความ “GO!” กระพริบบนจอ (ขึ้น 0.5 วิ หาย 0.5 วิ)',
              solution=P(setup=[oled_size(3)], loop=[oled_clear(), oled_print('GO!', 20, 4), wait(500), oled_clear(), oled_print('', 0, 0), wait(500)]),
              answer='การล้างจอต้องสั่ง display() ด้วยจึงเห็นผล ในบล็อกทำได้โดยพิมพ์ข้อความว่างด้วย Update: Yes')],
  quiz=[dict(q='พิมพ์ 3 บรรทัดติดกัน ควรตั้ง Update อย่างไรให้จอไม่กระพริบ', choices=['No สองบรรทัดแรก Yes บรรทัดสุดท้าย', 'Yes ทุกบรรทัด', 'No ทุกบรรทัด'], answer=0, why='display() ครั้งเดียวตอนท้าย ภาพขึ้นพร้อมกัน'),
        dict(q='จอสูง 32 จุด ใช้ตัวอักษรขนาด 1 ได้กี่บรรทัด', choices=['4 บรรทัด', '2 บรรทัด', '8 บรรทัด'], answer=0, why='ขนาด 1 สูง 8 จุด 32 ÷ 8 = 4')]))

L.append(dict(id='u1-button', unit=1, cat='core', title='ปุ่มบนบอร์ดและแรงดันแบตเตอรี่',
  goals=['อ่านปุ่ม Up/Down เป็นค่า true/false', 'อ่านแรงดันแบตแล้วแสดงบนจอ'],
  intro='บล็อกทรงหกเหลี่ยมให้ค่า <b>จริง/เท็จ</b> บล็อกทรงมนให้ค่า <b>ตัวเลข</b> ทั้งสองแบบใช้เดี่ยว ๆ ไม่ได้ ต้องเสียบลงช่องของบล็อกอื่น',
  blocks=['mini_BTNget', 'mini_PWR_getVolt'],
  examples=[
    dict(title='กดปุ่มแล้วไฟติด', desc='ใช้ if/else จากหมวด Control กดปุ่ม Up ค้างไว้ไฟเขียว ปล่อยไฟดับ',
         xml=P(loop=[B('control_if_else', v={'CONDITION': button('BTN_UP')}, s={'SUBSTACK': [led(0, 255, 0)], 'SUBSTACK2': [led(0, 0, 0)]})]),
         notes=[('if(MiniR4.BTN_UP.getState())', '<code>getState()</code> ได้ true เมื่อกดอยู่'),
                ('else', 'ไม่ได้กด')]),
    dict(title='แสดงแรงดันแบต', desc='อ่านทุก 1 วินาทีแล้วพิมพ์บนจอ',
         xml=P(setup=[oled_size(2)], loop=[oled_clear(), oled_print(B('mini_PWR_getVolt'), 0, 8), wait(1000)]),
         notes=[('MiniR4.OLED.print(MiniR4.PWR.getBattVoltage());', 'เสียบบล็อกค่าลงช่องข้อความ โค้ดจึงเอาคำสั่งอ่านไปไว้ในวงเล็บของ print')]),
  ],
  arduino=['บล็อกค่า (ทรงมน/หกเหลี่ยม) กลายเป็น<b>นิพจน์</b>ที่ไม่มี <code>;</code> และอยู่ในวงเล็บของคำสั่งอื่นเสมอ'],
  tries=[dict(task='กด Up ให้ไฟแดง กด Down ให้ไฟน้ำเงิน ไม่กดให้ดับ',
              solution=P(loop=[B('control_if_else', v={'CONDITION': button('BTN_UP')}, s={'SUBSTACK': [led(255, 0, 0)], 'SUBSTACK2': [
                  B('control_if_else', v={'CONDITION': button('BTN_DOWN')}, s={'SUBSTACK': [led(0, 0, 255)], 'SUBSTACK2': [led(0, 0, 0)]})]})])),
         dict(task='ถ้าแรงดันต่ำกว่า 7.0V ให้ไฟแดงเตือน (ใช้บล็อก &lt; จากหมวด Operators)',
              solution=P(loop=[B('control_if_else', v={'CONDITION': cmp('operator_lt', B('mini_PWR_getVolt'), N(7.0))}, s={'SUBSTACK': [led(255, 0, 0)], 'SUBSTACK2': [led(0, 60, 0)]}), wait(1000)]))],
  quiz=[dict(q='MiniR4.BTN_DOWN.getState() ให้ค่าแบบไหน', choices=['true หรือ false', 'ตัวเลข 0–1023', 'ข้อความ'], answer=0, why='บล็อกหกเหลี่ยม = ค่าความจริง'),
        dict(q='ทำไมโค้ด getBattVoltage() ไม่มี ; ต่อท้ายในตัวอย่าง', choices=['เพราะอยู่ในวงเล็บของ print เป็นค่าที่ส่งให้คำสั่งอื่น', 'ลืมใส่', 'คำสั่งอ่านไม่ต้องมี ; เสมอ'], answer=0, why='นิพจน์ที่อยู่ในวงเล็บไม่ใช่คำสั่งเดี่ยว')]))

L.append(dict(id='u1-gpio', unit=1, cat='core', title='Mini GPIO: พอร์ตดิจิทัล D และแอนะล็อก A',
  goals=['อ่าน/สั่งขาดิจิทัล Left/Right ของพอร์ต D1–D4', 'อ่านค่าแอนะล็อก 0–1023 จากพอร์ต A1–A3'],
  intro='พอร์ต D และ A แต่ละช่องมี 4 ขา: <b>Left</b>, <b>Right</b>, VCC, GND ขาสัญญาณมี 2 ขา จึงต้องเลือก Left หรือ Right ในบล็อก',
  blocks=['mini_DIget', 'mini_DOset', 'mini_AIget'],
  examples=[
    dict(title='สวิตช์ภายนอกที่ D1 คุมไฟ', desc='อ่านขา Left ของ D1 ถ้าเป็น HIGH ไฟเขียว',
         xml=P(loop=[B('control_if_else', v={'CONDITION': B('mini_DIget', f={'PIN': 'D1', 'PIN2': 'L'})}, s={'SUBSTACK': [led(0, 255, 0)], 'SUBSTACK2': [led(0, 0, 0)]})]),
         notes=[('MiniR4.D1.getL()', 'L = ขา Left ถ้าเลือก Right จะเป็น <code>getR()</code>')]),
    dict(title='ดูค่าแอนะล็อก A1 บนจอ', desc='หมุนเซนเซอร์หรือตัวต้านทานที่เสียบ A1 แล้วดูตัวเลขเปลี่ยน',
         xml=P(setup=[oled_size(3)], loop=[oled_clear(), oled_print(B('mini_AIget', f={'PIN': 'A1', 'PIN2': 'L'}), 0, 4), wait(200)]),
         notes=[('MiniR4.A1.getAIL()', 'AIL = Analog Input ขา Left ได้ 0–1023')]),
  ],
  arduino=['ชื่อพอร์ตเป็นชื่อสมาชิกของ MiniR4 โดยตรง เช่น <code>MiniR4.D3.setR(LOW);</code>', 'HIGH มีค่าเป็น 1 และ LOW เป็น 0'],
  tries=[dict(task='ต่อ LED ภายนอกที่ D2 ขา Right ให้กระพริบทุก 0.5 วินาที',
              solution=P(loop=[B('mini_DOset', f={'PIN': 'D2', 'PIN2': 'R'}, v={'HIGHLOW': B('mini_pins_high_low', f={'NUM': 'HIGH'})}), wait(500),
                               B('mini_DOset', f={'PIN': 'D2', 'PIN2': 'R'}, v={'HIGHLOW': B('mini_pins_high_low', f={'NUM': 'LOW'})}), wait(500)]))],
  quiz=[dict(q='MiniR4.A2.getAIR() อ่านค่าจากที่ไหน', choices=['พอร์ต A2 ขา Right', 'พอร์ต A2 ขา Left', 'ปุ่ม Right'], answer=0, why='AIR = Analog Input Right'),
        dict(q='ค่าแอนะล็อกอยู่ในช่วงใด', choices=['0–1023', '0–255', '0–1'], answer=0, why='ตัวแปลงสัญญาณ 10 บิต')]))

L.append(dict(id='u1-motor', unit=1, cat='core', title='มอเตอร์ DC ทีละตัว: Power, Speed, เบรก, เอนโคเดอร์',
  goals=['แยก Power (กำลังตรง) กับ Speed (คุมความเร็วด้วยเอนโคเดอร์)', 'นับองศาที่ล้อหมุนด้วยเอนโคเดอร์'],
  intro='หมวด R4 Core สั่งมอเตอร์ทีละตัว (M1–M4) เหมาะกับแขนกล สายพาน หรือทดลองมอเตอร์ ส่วนการขับหุ่นสองล้อใช้หมวด Movement ในบทถัดไป',
  blocks=['mini_MsetDIR', 'mini_ddc_set_ppr_rpm', 'mini_Mset', 'mini_MsetSpeed', 'mini_Mbrake', 'mini_ENC_reset', 'mini_ENC_get'],
  examples=[
    dict(title='หมุน 2 วิ แล้วเบรก', desc='จ่ายกำลัง 60% ให้ M1',
         xml=P(setup=[B('mini_Mset', f={'PIN': 'M1'}, v={'Speed': 60}), wait(2000), B('mini_Mbrake', f={'PIN': 'M1', 'BrakeType': 'true'})]),
         notes=[('MiniR4.M1.setPower(60);', 'สั่งแล้วมอเตอร์หมุนค้าง โปรแกรมไปต่อทันที'),
                ('delay(2000);', 'ปล่อยให้หมุน 2 วินาที'), ('MiniR4.M1.setBrake(true);', 'true = Brake, false = Coast')]),
    dict(title='หมุนครบ 1 รอบพอดี', desc='รีเซ็ตตัวนับ แล้วหมุนจนกว่าองศา ≥ 360 จึงเบรก',
         xml=P(setup=[B('mini_ENC_reset', f={'PIN': 'M1'}), B('mini_MsetSpeed', f={'PIN': 'M1'}, v={'Speed': 40}),
                      B('control_wait_until', v={'CONDITION': cmp('operator_gte', B('mini_ENC_get', f={'PIN': 'M1'}), N(360))}),
                      B('mini_Mbrake', f={'PIN': 'M1', 'BrakeType': 'true'})]),
         notes=[('MiniR4.M1.resetCounter();', 'เริ่มนับ 0'), ('while(!(MiniR4.M1.getDegrees() >= 360));', 'wait until กลายเป็น “วนรอตราบใดที่ยังไม่ถึง 360”'),
                ('MiniR4.M1.setSpeed(40);', 'Speed ใช้เอนโคเดอร์คุมความเร็วให้คงที่')]),
  ],
  arduino=['<code>setPower</code> = กำลังไฟตรง ๆ ถ่านอ่อนหมุนช้าลง / <code>setSpeed</code> = บอร์ดวัดความเร็วจริงแล้วปรับให้คงที่',
           'มอเตอร์ TT ของ MATRIX ใช้ PPR 545 และ RPM 200 ซึ่งเป็นค่าเริ่มต้นอยู่แล้ว'],
  tries=[dict(task='ให้ M2 หมุนไปข้างหน้า 1 วินาที หยุด 0.5 วินาที แล้วหมุนกลับ 1 วินาที',
              solution=P(setup=[B('mini_Mset', f={'PIN': 'M2'}, v={'Speed': 50}), wait(1000), B('mini_Mbrake', f={'PIN': 'M2', 'BrakeType': 'true'}), wait(500),
                                B('mini_Mset', f={'PIN': 'M2'}, v={'Speed': -50}), wait(1000), B('mini_Mbrake', f={'PIN': 'M2', 'BrakeType': 'true'})])),
         dict(task='แสดงองศาของ M1 บนจอตลอดเวลา แล้วลองหมุนล้อด้วยมือ',
              solution=P(setup=[B('mini_ENC_reset', f={'PIN': 'M1'}), oled_size(3)], loop=[oled_clear(), oled_print(B('mini_ENC_get', f={'PIN': 'M1'}), 0, 4), wait(100)]))],
  quiz=[dict(q='ถ่านอ่อนลง คำสั่งใดยังรักษาความเร็วได้ใกล้เดิม', choices=['setSpeed()', 'setPower()', 'ทั้งสองแบบเท่ากัน'], answer=0, why='setSpeed อ่านเอนโคเดอร์แล้วชดเชย'),
        dict(q='getDegrees() ได้ 720 หมายความว่า', choices=['ล้อหมุนไป 2 รอบ', 'ล้อหมุน 720 รอบ', 'ความเร็ว 720 รอบ/นาที'], answer=0, why='360 องศา = 1 รอบ')]))

L.append(dict(id='u1-servo', unit=1, cat='core', title='เซอร์โว RC: สั่งมุม 0–180°',
  goals=['สั่งเซอร์โวไปที่มุมที่ต้องการ', 'รู้ว่าต้องรอให้เซอร์โวหมุนเสร็จ'],
  intro='เซอร์โวใช้ทำแขนคีบ ประตู หรือหัวหมุน เสียบที่ช่อง RC1–RC4 สั่งเป็นมุม 0–180 องศา',
  blocks=['mini_RCsetDIR', 'mini_RCset'],
  examples=[
    dict(title='ปัดซ้าย-ขวา', desc='หมุนไป 30° และ 150° สลับกัน',
         xml=P(loop=[B('mini_RCset', f={'PIN': 'RC1'}, v={'Angle': 30}), wait(800), B('mini_RCset', f={'PIN': 'RC1'}, v={'Angle': 150}), wait(800)]),
         notes=[('MiniR4.RC1.setAngle(30);', 'สั่งแล้วไปต่อทันที เซอร์โวยังหมุนไม่เสร็จ'), ('delay(800);', 'รอให้หมุนถึงก่อนสั่งมุมถัดไป')]),
    dict(title='ค่อย ๆ หมุนทีละ 10°', desc='ใช้ repeat และตัวแปร <code>angle</code> ทำให้หมุนนุ่มนวล',
         xml=P(setup=[setvar('angle', '0'), B('control_repeat', v={'TIMES': 18}, s={'SUBSTACK': [B('mini_RCset', f={'PIN': 'RC1'}, v={'Angle': VAR('angle')}), changevar('angle', 10), wait(60)]})]),
         vars=['angle']),
  ],
  arduino=['ถ้าแขนกลับด้าน ใช้บล็อก Enable Reverse On → <code>setHWDir(false)</code> ใส่ใน Setup'],
  tries=[dict(task='ทำแขนคีบ: กาง 150° รอ 1 วิ หนีบ 60° รอ 1 วิ',
              solution=P(loop=[B('mini_RCset', f={'PIN': 'RC3'}, v={'Angle': 150}), wait(1000), B('mini_RCset', f={'PIN': 'RC3'}, v={'Angle': 60}), wait(1000)]))],
  quiz=[dict(q='สั่ง setAngle(0) แล้ว setAngle(180) ติดกันทันที จะเกิดอะไร', choices=['เซอร์โวแทบไม่ขยับไป 0 เพราะคำสั่ง 180 มาทับทันที', 'ไป 0 แล้วไป 180 ครบ', 'คอมไพล์ไม่ผ่าน'], answer=0, why='setAngle ไม่รอ ต้องใส่ delay คั่น')]))

L.append(dict(id='u1-move', unit=1, cat='move', title='Movement 1: ตั้งค่าล้อ และวิ่งตามระยะ',
  goals=['ตั้ง Set Movement ให้ถูกก่อนใช้บล็อก Movement', 'วิ่งตามองศาล้อหรือตามเวลา และเลือก Brake/Coast'],
  intro='หมวด Movement คุมหุ่นสองล้อพร้อมกัน (โค้ดขึ้นต้นด้วย <code>MiniR4.DriveDC</code>) ขั้นแรกต้องบอกว่าล้อซ้าย-ขวาอยู่ที่มอเตอร์ไหน',
  blocks=['mini_ddc_setting', 'mini_ddc_runFor'],
  examples=[
    dict(title='เดินหน้า 2 รอบล้อ แล้วถอยกลับ', desc='วางบล็อก Set Movement ไว้ใน Setup เสมอ',
         xml=P(setup=[drive_setup(), B('mini_ddc_runFor', f={'UNIT': 'degrees', 'BrakeType': 'true'}, v={'NUM': 720, 'SPEEDL': 50, 'SPEEDR': 50}), wait(500),
                      B('mini_ddc_runFor', f={'UNIT': 'degrees', 'BrakeType': 'true'}, v={'NUM': 720, 'SPEEDL': -50, 'SPEEDR': -50})]),
         notes=[('#define ENABLE_DRIVEDC_BRAKE_DELAY', 'มาจาก Brake Settle: Yes ต้องอยู่<b>ก่อน</b> #include จึงมีผล'),
                ('MiniR4.DriveDC.begin(1, 2, false, true);', 'ล้อซ้าย M1 ล้อขวา M2 กลับทิศเฉพาะล้อขวา (มอเตอร์ติดหันคนละด้าน)'),
                ('MiniR4.DriveDC.MoveDegs(50, 50, 720, true);', 'กำลังซ้าย, กำลังขวา, องศาล้อ, เบรก — โปรแกรมรอจนวิ่งครบจึงไปต่อ'),
                ('MiniR4.DriveDC.MoveDegs((-50), (-50), 720, true);', 'กำลังติดลบ = ถอยหลัง (โปรแกรมใส่วงเล็บรอบเลขลบให้)')]),
    dict(title='วิ่งตามเวลา', desc='เปลี่ยนหน่วยเป็น seconds คำสั่งกลายเป็น MoveTime',
         xml=P(setup=[drive_setup(), B('mini_ddc_runFor', f={'UNIT': 'seconds', 'BrakeType': 'false'}, v={'NUM': 1.5, 'SPEEDL': 60, 'SPEEDR': 60})]),
         notes=[('MiniR4.DriveDC.MoveTime(60, 60, 1.5, false);', 'วิ่ง 1.5 วินาที แล้วปล่อยไหล (Coast)')]),
  ],
  arduino=['คำสั่ง Move…Degs / Move…Time <b>รอจนเสร็จ</b> ต่างจาก setPower ที่สั่งแล้วไปต่อทันที',
           'ล้อเส้นผ่านศูนย์กลาง d ซม. หมุน 360° วิ่งได้ π × d ซม. ใช้คำนวณองศาจากระยะทาง'],
  tries=[dict(task='เดินหน้า 1 รอบล้อ หยุด 1 วิ ทำซ้ำ 3 ครั้ง (ใช้ repeat)',
              solution=P(setup=[drive_setup(), B('control_repeat', v={'TIMES': 3}, s={'SUBSTACK': [B('mini_ddc_runFor', f={'UNIT': 'degrees', 'BrakeType': 'true'}, v={'NUM': 360, 'SPEEDL': 50, 'SPEEDR': 50}), wait(1000)]})])),
         dict(task='ให้ล้อซ้าย 60 ล้อขวา 20 วิ่ง 2 วินาที หุ่นจะเลี้ยวไปทางไหน',
              solution=P(setup=[drive_setup(), B('mini_ddc_runFor', f={'UNIT': 'seconds', 'BrakeType': 'true'}, v={'NUM': 2, 'SPEEDL': 60, 'SPEEDR': 20})]),
              answer='ล้อซ้ายเร็วกว่า หุ่นโค้งไปทางขวา')],
  quiz=[dict(q='ถ้าลืมบล็อก Set Movement จะเกิดอะไร', choices=['บล็อก Movement ไม่รู้ว่าล้ออยู่มอเตอร์ไหน หุ่นไม่วิ่ง', 'หุ่นวิ่งปกติ', 'ไฟกระพริบ'], answer=0, why='ต้อง begin() ก่อนเสมอ'),
        dict(q='MoveDegs(50, 50, 360, true) — เลข 360 คืออะไร', choices=['องศาที่ล้อหมุน', 'ระยะ 360 ซม.', 'เวลา 360 ms'], answer=0, why='หน่วย degrees ของล้อ')]))

L.append(dict(id='u1-sync', unit=1, cat='move', title='Movement 2: วิ่งตรงด้วย Sync และ Gyro',
  goals=['เปรียบเทียบ power / Sync / Gyro', 'รู้จักบล็อก Set PID'],
  intro='มอเตอร์สองตัวไม่เคยเหมือนกันเป๊ะ วิ่งด้วย power เฉย ๆ หุ่นจึงมักเฉ หมวด Movement มีตัวช่วยสองแบบ: <b>Sync</b> ใช้เอนโคเดอร์ให้สองล้อหมุนเท่ากัน และ <b>Gyro</b> ใช้ไจโรบนบอร์ดคุมทิศ',
  blocks=['mini_ddc_runFor_sync', 'mini_ddc_runFor_gyro', 'mini_ddc_set_pid'],
  examples=[
    dict(title='ทดสอบสามแบบ', desc='กดปุ่ม Up แล้ววิ่งแบบละ 3 รอบล้อ สังเกตว่าแบบไหนตรงที่สุด',
         xml=P(setup=[drive_setup()], loop=[B('control_wait_until', v={'CONDITION': button()}),
               B('mini_ddc_runFor', f={'UNIT': 'degrees', 'BrakeType': 'true'}, v={'NUM': 1080, 'SPEEDL': 60, 'SPEEDR': 60}), wait(1000),
               B('mini_ddc_runFor_sync', f={'UNIT': 'degrees', 'BrakeType': 'true'}, v={'NUM': 1080, 'SPEEDL': 60, 'SPEEDR': 60}), wait(1000),
               B('mini_ddc_runFor_gyro', f={'UNIT': 'degrees', 'BrakeType': 'true'}, v={'NUM': 1080, 'SPEED': 60})]),
         notes=[('MiniR4.DriveDC.MoveSyncDegs(60, 60, 1080, true);', 'Sync: บอร์ดดูเอนโคเดอร์สองล้อแล้วปรับให้เท่ากัน'),
                ('MiniR4.DriveDC.MoveGyroDegs(60, 0, 1080, true);', 'Gyro: ความเร็ว, ทิศเป้าหมาย (บล็อกใส่ 0), องศาล้อ, เบรก')]),
    dict(title='ปรับ PID ของการวิ่ง Gyro', desc='ค่าแนะนำจากคู่มือ MATRIX สำหรับมอเตอร์ TT (ใส่ใน Setup ก่อนวิ่ง)',
         xml=P(setup=[drive_setup(), B('mini_ddc_set_pid', f={'PID_TYPE': 'MoveGyroPID'}, v={'KP': 6.01, 'KI': 0.0, 'KD': 2.15}),
                      B('mini_ddc_runFor_gyro', f={'UNIT': 'degrees', 'BrakeType': 'true'}, v={'NUM': 1440, 'SPEED': 70})]),
         notes=[('MiniR4.DriveDC.setMoveGyroPID(6.01, 0.0, 2.15);', 'Kp แก้ทันทีเมื่อเฉ, Ki แก้ที่สะสม, Kd ลดการส่าย')]),
  ],
  arduino=['ค่า PID เริ่มต้นสำหรับมอเตอร์ TT ตามคู่มือ: MoveSync (0.02, 0, 0.04) · MoveGyro (6.01, 0, 2.15) · TurnGyro (22.75, 0.08, 0.25)',
           'Kp มากไปหุ่นส่ายไปมา Kp น้อยไปหุ่นแก้ทิศช้า'],
  tries=[dict(task='วิ่ง Gyro 2 วินาทีด้วยความเร็ว 50 แล้วปล่อยไหล',
              solution=P(setup=[drive_setup(), B('mini_ddc_runFor_gyro', f={'UNIT': 'seconds', 'BrakeType': 'false'}, v={'NUM': 2, 'SPEED': 50})]))],
  quiz=[dict(q='แบบใดใช้ไจโรบนบอร์ดคุมทิศ', choices=['Move(Gyro)', 'Move(Sync)', 'Move for … power'], answer=0, why='Sync ใช้เอนโคเดอร์ Gyro ใช้ IMU'),
        dict(q='หุ่นส่ายซ้าย-ขวาถี่ ๆ ระหว่างวิ่ง Gyro ควรลองทำอะไรก่อน', choices=['ลด Kp หรือเพิ่ม Kd', 'เพิ่ม Kp อีก', 'ตั้ง Ki เป็น 100'], answer=0, why='Kp มากเกินทำให้แกว่ง Kd ช่วยหน่วง')]))

L.append(dict(id='u1-moving', unit=1, cat='move', title='Movement 3: วิ่งต่อเนื่อง หยุดเอง และวัดระยะ',
  goals=['ใช้ Moving at … คู่กับ Stop moving', 'วัดระยะด้วย degrees counted'],
  intro='บล็อก <b>Moving</b> สั่งแล้วหุ่นวิ่งค้างไว้ โปรแกรมไปต่อทันที เราจึงเช็กเงื่อนไขอื่นระหว่างวิ่งได้ เช่น ระยะ เวลา หรือเซนเซอร์ แล้วสั่ง Stop moving เอง',
  blocks=['mini_ddc_on', 'mini_ddc_on_sync', 'mini_ddc_on_gyro', 'mini_ddc_get_degs', 'mini_ddc_reset_degs', 'mini_ddc_off'],
  examples=[
    dict(title='วิ่งจนครบระยะที่วัดเอง', desc='รีเซ็ตระยะ วิ่ง Sync แล้วรอจนระยะ ≥ 1000 องศาจึงหยุด',
         xml=P(setup=[drive_setup(), B('mini_ddc_reset_degs'), B('mini_ddc_on_sync', v={'SPEEDL': 50, 'SPEEDR': 50}),
                      B('control_wait_until', v={'CONDITION': cmp('operator_gte', B('mini_ddc_get_degs'), N(1000))}),
                      B('mini_ddc_off', f={'BrakeType': 'true'})]),
         notes=[('MiniR4.DriveDC.MoveSync(50, 50);', 'เริ่มวิ่งแล้วไปบรรทัดถัดไปทันที'),
                ('while(!(MiniR4.DriveDC.getDegrees() >= 1000));', 'วนรอจนระยะถึง'), ('MiniR4.DriveDC.brake(true);', 'Stop moving แบบ Brake')]),
    dict(title='วิ่งไปจนกดปุ่ม', desc='กด Down เมื่อไหร่หยุดทันที แล้วโชว์ระยะบนจอ',
         xml=P(setup=[drive_setup(), oled_size(2), B('mini_ddc_reset_degs'), B('mini_ddc_on_gyro', v={'SPEEDL': 40}),
                      B('control_wait_until', v={'CONDITION': button('BTN_DOWN')}), B('mini_ddc_off', f={'BrakeType': 'true'}),
                      oled_clear(), oled_print(B('mini_ddc_get_degs'), 0, 8)])),
  ],
  arduino=['Moving = <code>Move</code> / <code>MoveSync</code> / <code>MoveGyro</code> ไม่มีคำว่า Degs/Time จึงไม่หยุดเอง',
           'บล็อก Moving at … % power (<code>Move</code>) ไม่มี PID เหมาะใช้กับอัลกอริทึมเดินตามเส้นที่คำนวณกำลังล้อเอง'],
  tries=[dict(task='วิ่ง 3 วินาทีด้วย Moving(Sync) แล้วหยุด (ใช้ wait แทนการวัดระยะ)',
              solution=P(setup=[drive_setup(), B('mini_ddc_on_sync', v={'SPEEDL': 50, 'SPEEDR': 50}), wait(3000), B('mini_ddc_off', f={'BrakeType': 'true'})]))],
  quiz=[dict(q='สั่ง Moving at … แล้วไม่สั่ง Stop moving เลย จะเป็นอย่างไร', choices=['หุ่นวิ่งต่อไปเรื่อย ๆ', 'หุ่นหยุดเองหลัง 1 วินาที', 'หุ่นไม่ขยับ'], answer=0, why='ไม่มีระยะหรือเวลาหยุดในคำสั่ง'),
        dict(q='getDegrees() ของ DriveDC คิดจากอะไร', choices=['ค่าเฉลี่ยองศาล้อซ้ายและขวา', 'มุมไจโร', 'เวลาที่วิ่ง'], answer=0, why='(|ซ้าย| + |ขวา|) ÷ 2')]))

L.append(dict(id='u1-turn', unit=1, cat='move', title='Movement 4: เลี้ยวด้วยไจโร ล้อเดียว / สองล้อ',
  goals=['เลือกใช้ Turn Single-Wheel หรือ Turn Two-Wheel', 'ทดลองดูว่ามุมเลี้ยวต่อกันหลายครั้งเป็นอย่างไร'],
  intro='บล็อกเลี้ยวทั้งสองแบบใช้ <b>ไจโร (IMU)</b> วัดมุม มุมบวก = ตามเข็มนาฬิกา (ขวา) มุมลบ = ทวนเข็ม (ซ้าย) ในโค้ดเป็นคำสั่งเดียวกันคือ <code>TurnGyro</code> ต่างกันที่เลขโหมด',
  blocks=['mini_ddc_turn', 'mini_ddc_turntwo'],
  examples=[
    dict(title='เดินเป็นสี่เหลี่ยม', desc='เดิน-เลี้ยว 4 ครั้ง (ใช้ repeat)',
         xml=P(setup=[drive_setup(), B('mini_motion_reset'), B('control_repeat', v={'TIMES': 4}, s={'SUBSTACK': [
               B('mini_ddc_runFor_gyro', f={'UNIT': 'degrees', 'BrakeType': 'true'}, v={'NUM': 720, 'SPEED': 50}),
               B('mini_ddc_turntwo', f={'BrakeType': 'true'}, v={'ANGLE': 90, 'SPEED': 40})]})]),
         notes=[('MiniR4.Motion.resetIMUValues();', 'รีเซ็ตไจโรก่อนเริ่ม (บล็อกจากหมวด Sensing)'),
                ('MiniR4.DriveDC.TurnGyro(40, 90, 1, true);', 'ความเร็ว 40, มุม 90, โหมด 1 = สองล้อ, เบรก')]),
  ],
  arduino=['Turn Single-Wheel → โหมด <code>0</code> ล้อเดียวหมุน วงเลี้ยวกว้าง · Turn Two-Wheel → โหมด <code>1</code> หมุนอยู่กับที่',
           'คู่มือเรียกมุมนี้ว่า <i>heading</i> ของไจโร ลองทดลองข้างล่างเพื่อดูว่าหุ่นของเรานับมุมแบบไหน'],
  tries=[dict(task='<b>ทดลอง:</b> สั่ง Turn Two-Wheel 90° สองครั้งติดกัน หุ่นหมุนรวม 180° หรือหมุนแค่ 90° แล้วค้าง? จดผลไว้ แล้วลองเปลี่ยนครั้งที่สองเป็น 180°',
              solution=P(setup=[drive_setup(), B('mini_motion_reset'), B('mini_ddc_turntwo', f={'BrakeType': 'true'}, v={'ANGLE': 90, 'SPEED': 40}), wait(1000),
                                B('mini_ddc_turntwo', f={'BrakeType': 'true'}, v={'ANGLE': 90, 'SPEED': 40})]),
              answer='ถ้าหมุนแค่ 90° แสดงว่ามุมเป็นทิศเป้าหมายนับจากตอนรีเซ็ตไจโร ต้องสั่ง 90, 180, 270 … ถ้าหมุน 180° แสดงว่านับเพิ่มจากทิศปัจจุบัน'),
         dict(task='เลี้ยวซ้าย 90° แบบล้อเดียว',
              solution=P(setup=[drive_setup(), B('mini_motion_reset'), B('mini_ddc_turn', f={'BrakeType': 'true'}, v={'ANGLE': -90, 'SPEED': 40})]),
              answer='ใช้มุมลบ −90')],
  quiz=[dict(q='TurnGyro(40, 90, 0, true) เลี้ยวแบบไหน', choices=['ล้อเดียว', 'สองล้อหมุนสวนกัน', 'ถอยหลัง'], answer=0, why='โหมด 0 = Single-Wheel'),
        dict(q='อยากหมุนตัวในที่แคบ ควรใช้บล็อกใด', choices=['Turn Two-Wheel', 'Turn Single-Wheel', 'Move for'], answer=0, why='หมุนรอบจุดกลางหุ่น')]))

# =====================================================================
# หน่วยที่ 3 Control
# =====================================================================
L.append(dict(id='u3-wait', unit=3, cat='control', title='เวลา: wait และ millis',
  goals=['ใช้ wait (delay) หยุดรอ', 'ใช้ millis จับเวลาโดยไม่ต้องหยุดโปรแกรม'],
  intro='<b>wait</b> สั่งให้บอร์ดหยุดรอ ระหว่างนั้นทำอย่างอื่นไม่ได้ ส่วน <b>millis</b> เป็นนาฬิกาที่เดินตลอด เราอ่านเวลาแล้วตัดสินใจเองได้ บอร์ดจึงทำงานอื่นไปพร้อมกัน',
  blocks=['control_wait', 'mini_millis'],
  examples=[
    dict(title='นาฬิกาจับเวลา', desc='โชว์จำนวนวินาทีตั้งแต่เปิดเครื่อง',
         xml=P(setup=[oled_size(3)], loop=[oled_clear(), oled_print(op('operator_divide', B('mini_millis'), N(1000)), 0, 4), wait(100)]),
         notes=[('millis() / 1000', 'millis นับเป็นมิลลิวินาที หาร 1000 ได้วินาที')]),
    dict(title='กระพริบไปด้วย อ่านปุ่มไปด้วย', desc='ไม่มี wait ยาว ปุ่มจึงตอบสนองทันที ใช้ตัวแปร <code>last</code> จำเวลาที่สลับไฟครั้งล่าสุด',
         xml=P(setup=[setvar('last', '0'), setvar('on', '0')], loop=[
             B('control_if', v={'CONDITION': cmp('operator_gt', op('operator_subtract', B('mini_millis'), VAR('last')), N(500))}, s={'SUBSTACK': [
                 setvar('last', B('mini_millis')), setvar('on', op('operator_subtract', N(1), VAR('on')))]}),
             B('control_if_else', v={'CONDITION': cmp('operator_equals', VAR('on'), N(1))}, s={'SUBSTACK': [led(0, 0, 255)], 'SUBSTACK2': [led(0, 0, 0)]}),
             B('control_if_else', v={'CONDITION': button()}, s={'SUBSTACK': [led(255, 0, 0, 2)], 'SUBSTACK2': [led(0, 0, 0, 2)]})]),
         vars=['last', 'on'],
         notes=[('if((millis() - last) > 500)', 'ผ่านไปเกิน 500 ms จากครั้งก่อนหรือยัง'), ('on = 1 - on;', 'สลับ 0 ↔ 1')]),
  ],
  arduino=['ระหว่าง <code>delay()</code> บอร์ดไม่อ่านปุ่ม ไม่อ่านเซนเซอร์ ถ้ากดปุ่มตอนนั้นจะพลาด', 'รูปแบบ <code>millis() - last &gt; ช่วงเวลา</code> คือเทคนิคมาตรฐานของ Arduino'],
  tries=[dict(task='ตั้งเวลา 5 วินาที: เมื่อ millis เกิน 5000 ให้ไฟแดงติด',
              solution=P(loop=[B('control_if', v={'CONDITION': cmp('operator_gt', B('mini_millis'), N(5000))}, s={'SUBSTACK': [led(255, 0, 0)]})]))],
  quiz=[dict(q='wait 2000 คือกี่วินาที', choices=['2 วินาที', '20 วินาที', '0.2 วินาที'], answer=0, why='1000 ms = 1 s'),
        dict(q='ทำไมตัวอย่างที่สองไม่ใช้ wait 500', choices=['เพื่อให้อ่านปุ่มได้ตลอดเวลา', 'wait ใช้กับไฟไม่ได้', 'millis แม่นกว่าเสมอ'], answer=0, why='wait ทำให้บอร์ดหยุดทุกอย่าง')]))

L.append(dict(id='u3-if', unit=3, cat='control', title='ตัดสินใจ: if และ if … else',
  goals=['เขียนเงื่อนไขด้วย if', 'อ่าน if(…) { } else { } ในโค้ด'],
  intro='if รับเงื่อนไขเป็นบล็อกหกเหลี่ยม (จริง/เท็จ) เช่น ปุ่มถูกกด หรือการเปรียบเทียบตัวเลข',
  blocks=['control_if', 'control_if_else'],
  examples=[
    dict(title='ไฟเตือนแบตตามระดับ', desc='if ซ้อน if: มากกว่า 7.6V เขียว, มากกว่า 7.0V เหลือง, นอกนั้นแดง',
         xml=P(loop=[B('control_if_else', v={'CONDITION': cmp('operator_gt', B('mini_PWR_getVolt'), N(7.6))}, s={
             'SUBSTACK': [led(0, 200, 0)],
             'SUBSTACK2': [B('control_if_else', v={'CONDITION': cmp('operator_gt', B('mini_PWR_getVolt'), N(7.0))}, s={'SUBSTACK': [led(200, 150, 0)], 'SUBSTACK2': [led(255, 0, 0)]})]}),
             wait(1000)]),
         notes=[('if(MiniR4.PWR.getBattVoltage() > 7.6)', 'เงื่อนไขอยู่ในวงเล็บหลัง if'),
                ('else', 'ส่วนที่ทำเมื่อเงื่อนไขเป็นเท็จ')]),
  ],
  arduino=['ในโค้ด if ที่ไม่มี else คือ <code>if(เงื่อนไข) { … }</code> เฉย ๆ', 'ปีกกาเปิด-ปิดต้องครบคู่ ถ้าเขียนเองแล้วขาด จะคอมไพล์ไม่ผ่าน'],
  tries=[dict(task='กด Up ให้บี๊บเสียงสูง ไม่กดให้ไฟฟ้าอ่อน',
              solution=P(loop=[B('control_if_else', v={'CONDITION': button()}, s={'SUBSTACK': [B('mini_Buzzer_Tone', v={'FREQ': 1500, 'VOL': 100}), wait(150)], 'SUBSTACK2': [led(0, 0, 60)]})]))],
  quiz=[dict(q='if ที่ไม่มี else ถ้าเงื่อนไขเป็นเท็จจะทำอะไร', choices=['ข้ามไปทำบล็อกถัดไป', 'หยุดโปรแกรม', 'ทำข้างในอยู่ดี'], answer=0, why='ไม่มีทางเลือกอื่นให้ทำ')]))

L.append(dict(id='u3-loop', unit=3, cat='control', title='ทำซ้ำ: repeat และ forever',
  goals=['ใช้ repeat ทำซ้ำตามจำนวนครั้ง', 'อ่านลูป for และ while(true) ในโค้ด'],
  intro='repeat กลายเป็นลูป <code>for</code> ที่มีตัวนับ ส่วน forever กลายเป็น <code>while(true)</code> ที่ไม่มีวันจบ',
  blocks=['control_repeat', 'control_forever'],
  examples=[
    dict(title='บี๊บ 3 ครั้งตอนเปิดเครื่อง', desc='แล้วไฟเขียวติด',
         xml=P(setup=[B('control_repeat', v={'TIMES': 3}, s={'SUBSTACK': [B('mini_Buzzer_Tone', v={'FREQ': 1200, 'VOL': 100}), wait(250)]}), led(0, 200, 0)]),
         notes=[('for(int i_0 = 0; i_0 < 3; i_0++)', 'เริ่ม i_0 = 0 ทำตราบที่ i_0 &lt; 3 แต่ละรอบบวก 1 → ทำ 3 รอบ (0, 1, 2)')]),
    dict(title='forever ใน Setup', desc='ทำงานเหมือน Loop แต่บล็อกที่ต่อท้าย forever จะไม่มีวันได้ทำ',
         xml=P(setup=[B('control_forever', s={'SUBSTACK': [led(255, 0, 0), wait(300), led(0, 0, 0), wait(300)]})]),
         notes=[('while(true)', 'เงื่อนไขเป็นจริงเสมอ วนไม่รู้จบ')]),
  ],
  arduino=['ชื่อตัวนับ <code>i_0</code> โปรแกรมตั้งให้อัตโนมัติ ถ้ามี repeat หลายอันจะเป็น i_1, i_2 …', 'เขียนเองใน Arduino นิยมใช้ <code>for (int i = 0; i &lt; 3; i++)</code>'],
  tries=[dict(task='ไฟกระพริบ 5 ครั้งแล้วดับไปเลย',
              solution=P(setup=[B('control_repeat', v={'TIMES': 5}, s={'SUBSTACK': [led(255, 255, 255), wait(200), led(0, 0, 0), wait(200)]})])),
         dict(task='repeat ซ้อน repeat: บี๊บ 2 ครั้ง เว้น 1 วินาที ทำทั้งหมด 3 ชุด',
              solution=P(setup=[B('control_repeat', v={'TIMES': 3}, s={'SUBSTACK': [B('control_repeat', v={'TIMES': 2}, s={'SUBSTACK': [B('mini_Buzzer_Tone', v={'FREQ': 1500, 'VOL': 80}), wait(200)]}), wait(1000)]})]),
              answer='ลูปในใช้ตัวนับ i_1 ลูปนอกใช้ i_0')],
  quiz=[dict(q='for(int i_0 = 0; i_0 &lt; 10; i_0++) ทำกี่รอบ', choices=['10 รอบ', '11 รอบ', '9 รอบ'], answer=0, why='0 ถึง 9'),
        dict(q='บล็อกที่ต่อใต้ forever จะเป็นอย่างไร', choices=['ไม่ได้ทำ', 'ทำหลัง forever ครบรอบ', 'ทำพร้อมกัน'], answer=0, why='while(true) ไม่มีวันออก')]))

L.append(dict(id='u3-until', unit=3, cat='control', title='รอและวนจนกว่า: wait until · repeat until',
  goals=['รอจนเงื่อนไขจริงด้วย wait until', 'ทำซ้ำจนเงื่อนไขจริงด้วย repeat until'],
  intro='สองบล็อกนี้กลายเป็นลูป <code>while(!เงื่อนไข)</code> อ่านว่า “ตราบใดที่<b>ยังไม่</b>จริง” เครื่องหมาย <code>!</code> คือ not',
  blocks=['control_wait_until', 'control_repeat_until'],
  examples=[
    dict(title='กดปุ่มเพื่อเริ่ม', desc='แบบที่ใช้ในการแข่งขัน: รอกดปุ่มแล้วจึงวิ่ง',
         xml=P(setup=[drive_setup(), oled_size(2), oled_print('PRESS UP', 0, 8), B('control_wait_until', v={'CONDITION': button()}), oled_clear(), oled_print('GO', 0, 8),
                      B('mini_ddc_runFor_sync', f={'UNIT': 'degrees', 'BrakeType': 'true'}, v={'NUM': 720, 'SPEEDL': 50, 'SPEEDR': 50})]),
         notes=[('while(!MiniR4.BTN_UP.getState());', 'วนรอเปล่า ๆ (มี ; ต่อท้ายทันที) จนปุ่มถูกกด')]),
    dict(title='กระพริบจนกว่าจะกด Down', desc='repeat until มีคำสั่งข้างในให้ทำระหว่างรอ',
         xml=P(setup=[B('control_repeat_until', v={'CONDITION': button('BTN_DOWN')}, s={'SUBSTACK': [led(255, 120, 0), wait(150), led(0, 0, 0), wait(150)]}), led(0, 255, 0)])),
  ],
  arduino=['<code>while(!x);</code> ถ้าเงื่อนไขไม่มีวันจริง โปรแกรมจะค้างตรงนี้ตลอดไป ตรวจเงื่อนไขให้ดี'],
  tries=[dict(task='เดิน Moving(Gyro) จนกว่าจะกด Down แล้วหยุด',
              solution=P(setup=[drive_setup(), B('mini_ddc_on_gyro', v={'SPEEDL': 40}), B('control_wait_until', v={'CONDITION': button('BTN_DOWN')}), B('mini_ddc_off', f={'BrakeType': 'true'})]))],
  quiz=[dict(q='repeat until (ปุ่มถูกกด) จะหยุดวนเมื่อไร', choices=['เมื่อปุ่มถูกกด', 'เมื่อปล่อยปุ่ม', 'ครบ 10 รอบ'], answer=0, why='until = จนกว่า')]))

# =====================================================================
# หน่วยที่ 4 Operators & Variables
# =====================================================================
L.append(dict(id='u4-vars', unit=4, cat='vars', title='ตัวแปร: สร้าง กำหนดค่า เพิ่มค่า',
  goals=['สร้างตัวแปรและใช้ set / change', 'รู้ว่าตัวแปรจากบล็อกเป็นชนิด float'],
  intro='ตัวแปรคือกล่องเก็บค่าที่มีชื่อ สร้างได้ที่หมวด Variables ปุ่ม Make a Variable ตั้งชื่อเป็นภาษาอังกฤษ ไม่มีเว้นวรรค ห้ามขึ้นต้นด้วยตัวเลข',
  blocks=['data_setvariableto', 'data_changevariableby', 'data_variable'],
  examples=[
    dict(title='นับจำนวนครั้งที่กดปุ่ม', desc='กดหนึ่งครั้งนับเพิ่ม 1 (รอให้ปล่อยก่อน กันนับซ้ำ)',
         xml=P(setup=[setvar('presses', '0'), oled_size(3)], loop=[
             B('control_wait_until', v={'CONDITION': button()}), changevar('presses', 1),
             oled_clear(), oled_print(VAR('presses'), 0, 4),
             B('control_wait_until', v={'CONDITION': B('operator_not', v={'OPERAND': button()})})]),
         vars=['presses'],
         notes=[('float presses;', 'ตัวแปรถูกประกาศไว้บนสุด นอก setup/loop ทุกส่วนจึงใช้ได้'),
                ('presses = 0;', 'set → กำหนดค่า'), ('presses = presses + 1;', 'change by 1 → เอาค่าเดิมบวก 1 แล้วเก็บกลับ')]),
  ],
  arduino=['ตัวแปรทุกตัวจากบล็อกเป็น <code>float</code> (ทศนิยม) จอจึงแสดง 3.00 ถ้าเขียนเองควรใช้ <code>int</code> กับการนับ',
           'ชื่อตัวแปรตัวเล็ก-ใหญ่ต่างกัน <code>Score</code> กับ <code>score</code> คือคนละตัว'],
  tries=[dict(task='ตัวแปร speed เริ่มที่ 30 ทุกครั้งที่กด Up เพิ่ม 10 แล้วโชว์บนจอ',
              solution=P(setup=[setvar('speed', '30'), oled_size(3)], loop=[B('control_wait_until', v={'CONDITION': button()}), changevar('speed', 10), oled_clear(), oled_print(VAR('speed'), 0, 4), wait(300)]),
              vars=['speed'])],
  quiz=[dict(q='change score by -2 ได้โค้ดใด', choices=['score = score + -2;', 'score = -2;', 'score - 2;'], answer=0, why='change = บวกเพิ่มจากค่าเดิม'),
        dict(q='ตัวแปรที่สร้างในบล็อกเป็นชนิดใด', choices=['float', 'int', 'String'], answer=0, why='ตัวสร้างโค้ดประกาศ float ทุกตัว')]))

L.append(dict(id='u4-math', unit=4, cat='ops', title='คำนวณ: + − × ÷ mod round และฟังก์ชันคณิต',
  goals=['ใช้บล็อกคำนวณซ้อนกัน', 'ระวังการหารจำนวนเต็มและตัวเลือกที่คอมไพล์ไม่ผ่าน'],
  intro='บล็อกคำนวณเป็นทรงมน เอาไปเสียบในช่องตัวเลขได้ทุกที่ บล็อกซ้อนกันกลายเป็นวงเล็บในโค้ด',
  blocks=['operator_add', 'operator_subtract', 'operator_multiply', 'operator_divide', 'operator_mod', 'operator_round', 'operator_mathop'],
  examples=[
    dict(title='คำนวณระยะทางจากองศาล้อ', desc='ล้อเส้นผ่านศูนย์กลาง 6.5 ซม. ระยะ (ซม.) = องศา × 3.14 × 6.5 ÷ 360 เข็นหุ่นด้วยมือแล้วดูตัวเลข',
         xml=P(setup=[drive_setup(), B('mini_ddc_reset_degs'), oled_size(2)], loop=[oled_clear(), oled_print(op('operator_divide', op('operator_multiply', B('mini_ddc_get_degs'), op('operator_multiply', N(3.14), N(6.5))), N(360)), 0, 8), wait(200)]),
         notes=[('((MiniR4.DriveDC.getDegrees() * (3.14 * 6.5)) / 360)', 'บล็อกที่ซ้อนอยู่ข้างในคำนวณก่อน เหมือนวงเล็บในคณิตศาสตร์'),
                ('MiniR4.DriveDC.getDegrees()', 'ค่านี้เป็นจำนวนเต็ม จึงต้อง<b>คูณก่อนหาร</b> ถ้าหาร 360 ก่อน 500 ÷ 360 จะได้ 1 แทน 1.39')]),
    dict(title='ระวัง! หารจำนวนเต็ม', desc='7 ÷ 2 ในโค้ดได้ 3 ไม่ใช่ 3.5 แต่ถ้าเก็บใส่ตัวแปรก่อนได้ 3.5',
         xml=P(setup=[setvar('a', '7'), oled_print(op('operator_divide', N(7), N(2)), 0, 0, 'No'), oled_print(op('operator_divide', VAR('a'), N(2)), 0, 16)]),
         vars=['a'],
         notes=[('(7 / 2)', 'int ÷ int = int ได้ 3'), ('(a / 2)', 'a เป็น float จึงได้ 3.50')]),
  ],
  arduino=['mod ในบล็อกใช้ <code>fmod(a, b)</code> ใช้ได้กับทศนิยม เขียนเองกับ int ใช้ <code>a % b</code>',
           'ตัวเลือก <b>ceiling</b> ในบล็อก abs/floor… สร้าง <code>ceiling()</code> ซึ่งคอมไพล์ไม่ผ่าน แก้ใน Arduino เป็น <code>ceil()</code>',
           'sin/cos ธรรมดาใช้หน่วยเรเดียน ถ้าคิดเป็นองศาเลือก “sin (degrees)”'],
  tries=[dict(task='โชว์เลขคู่หรือคี่ของจำนวนครั้งที่กดปุ่ม (ใช้ mod 2 แล้วเทียบกับ 0)',
              solution=P(setup=[setvar('n', '0'), oled_size(3)], loop=[B('control_wait_until', v={'CONDITION': button()}), changevar('n', 1), oled_clear(),
                  B('control_if_else', v={'CONDITION': cmp('operator_equals', op('operator_mod', VAR('n'), N(2)), N(0))}, s={'SUBSTACK': [oled_print('EVEN', 0, 4)], 'SUBSTACK2': [oled_print('ODD', 0, 4)]}),
                  B('control_wait_until', v={'CONDITION': B('operator_not', v={'OPERAND': button()})})]), vars=['n'])],
  quiz=[dict(q='Serial.println((7 / 2)); แสดงค่าใด', choices=['3', '3.5', '4'], answer=0, why='หารจำนวนเต็มตัดเศษทิ้ง'),
        dict(q='10 mod 4 ได้เท่าไร', choices=['2', '2.5', '0'], answer=0, why='10 = 4×2 + 2')]))

L.append(dict(id='u4-logic', unit=4, cat='ops', title='เปรียบเทียบและตรรกะ: &lt; = &gt; and or not',
  goals=['สร้างเงื่อนไขจากการเปรียบเทียบ', 'รวมเงื่อนไขด้วย and / or / not'],
  intro='บล็อกหกเหลี่ยมให้ค่า true/false ใช้ใส่ใน if, wait until, repeat until',
  blocks=['operator_lt', 'operator_equals', 'operator_gt', 'operator_gte', 'operator_lte', 'operator_and', 'operator_or', 'operator_not', 'operator_const_bool'],
  examples=[
    dict(title='ต้องกดสองปุ่มพร้อมกัน', desc='ไฟเขียวเมื่อกด Up <b>และ</b> Down พร้อมกันเท่านั้น',
         xml=P(loop=[B('control_if_else', v={'CONDITION': B('operator_and', v={'OPERAND1': button('BTN_UP'), 'OPERAND2': button('BTN_DOWN')})}, s={'SUBSTACK': [led(0, 255, 0)], 'SUBSTACK2': [led(0, 0, 0)]})]),
         notes=[('&&', 'and = จริงเมื่อทั้งสองข้างจริง')]),
    dict(title='ค่าอยู่ในช่วงที่กำหนดไหม', desc='ค่าแอนะล็อก A1 อยู่ระหว่าง 300 ถึง 700 ไฟเขียว นอกช่วงไฟแดง',
         xml=P(loop=[B('control_if_else', v={'CONDITION': B('operator_and', v={'OPERAND1': cmp('operator_gte', B('mini_AIget', f={'PIN': 'A1', 'PIN2': 'L'}), N(300)), 'OPERAND2': cmp('operator_lte', B('mini_AIget', f={'PIN': 'A1', 'PIN2': 'L'}), N(700))})},
                         s={'SUBSTACK': [led(0, 255, 0)], 'SUBSTACK2': [led(255, 0, 0)]})])),
  ],
  arduino=['<code>=</code> ในบล็อก กลายเป็น <code>==</code> ในโค้ด ถ้าเขียนเองแล้วใช้ = ตัวเดียวใน if จะกลายเป็นการกำหนดค่า (บั๊กที่พบบ่อย)',
           'or → <code>||</code> · not → <code>!</code>'],
  tries=[dict(task='ไฟแดงเมื่อแบตต่ำกว่า 7V <b>หรือ</b> กดปุ่ม Down',
              solution=P(loop=[B('control_if_else', v={'CONDITION': B('operator_or', v={'OPERAND1': cmp('operator_lt', B('mini_PWR_getVolt'), N(7)), 'OPERAND2': button('BTN_DOWN')})}, s={'SUBSTACK': [led(255, 0, 0)], 'SUBSTACK2': [led(0, 0, 0)]})]))],
  quiz=[dict(q='!(5 &gt; 3) ได้ค่าใด', choices=['false', 'true', '2'], answer=0, why='5 > 3 จริง แล้ว not กลับเป็นเท็จ'),
        dict(q='if (x = 5) ในโค้ดที่เขียนเองมีปัญหาอะไร', choices=['เป็นการกำหนดค่า ไม่ใช่เปรียบเทียบ', 'ไม่มีปัญหา', 'ต้องใช้ === แบบ JavaScript'], answer=0, why='เปรียบเทียบต้องใช้ ==')]))

L.append(dict(id='u4-range', unit=4, cat='ops', title='สุ่ม และปรับช่วงค่า: random · map · constrain',
  goals=['สุ่มตัวเลข', 'แปลงช่วงค่าเซนเซอร์เป็นช่วงที่ใช้งาน และกันค่าเกิน'],
  intro='map กับ constrain ใช้บ่อยมากกับเซนเซอร์และมอเตอร์ เช่น เปลี่ยนค่า 0–1023 ให้เป็นความเร็ว 0–100',
  blocks=['operator_random', 'mini_randomSeed', 'mini_map', 'operator_constrain'],
  examples=[
    dict(title='ลูกเต๋า', desc='กดปุ่มแล้วสุ่ม 1–6 (Arduino ไม่รวมเลขท้าย จึงใส่ 7)',
         xml=P(setup=[B('mini_randomSeed', v={'SEED': B('mini_AIget', f={'PIN': 'A3', 'PIN2': 'L'})}), oled_size(3)],
               loop=[B('control_wait_until', v={'CONDITION': button()}), oled_clear(), oled_print(B('operator_random', v={'FROM': 1, 'TO': 7}), 50, 4), wait(400)]),
         notes=[('randomSeed(MiniR4.A3.getAIL());', 'ใช้ค่าจากขาที่ไม่ได้เสียบอะไร (ค่าแกว่งไปมา) เป็นเมล็ดสุ่ม ทำให้ไม่ซ้ำทุกครั้งที่เปิดเครื่อง'),
                ('random(1, 7)', 'ได้ 1–6')]),
    dict(title='ปุ่มหมุนคุมความเร็วมอเตอร์', desc='ค่าแอนะล็อก 0–1023 → ความเร็ว 0–100 แล้วบีบไม่ให้เกิน 80',
         xml=P(loop=[B('mini_Mset', f={'PIN': 'M1'}, v={'Speed': B('operator_constrain', v={'NUM': B('mini_map', v={'VAL': B('mini_AIget', f={'PIN': 'A1', 'PIN2': 'L'}), 'frmL': 0, 'frmH': 1023, 'toL': 0, 'toH': 100}), 'MIN': 0, 'MAX': 80})}), wait(50)]),
         notes=[('map(MiniR4.A1.getAIL(), 0, 1023, 0, 100)', 'ค่า, ช่วงเดิม (ต่ำ สูง), ช่วงใหม่ (ต่ำ สูง)'),
                ('constrain(', 'ผลลัพธ์อยู่ในช่วง 0–80 เสมอ')]),
  ],
  arduino=['<code>map()</code> ของ Arduino คิดเป็นจำนวนเต็ม (ปัดเศษทิ้ง)', '<code>random(a, b)</code> ได้ a ถึง b−1'],
  tries=[dict(task='สุ่มสีไฟ R G B แต่ละสี 0–255 ทุก 0.5 วินาที',
              solution=P(loop=[led(B('operator_random', v={'FROM': 0, 'TO': 256}), B('operator_random', v={'FROM': 0, 'TO': 256}), B('operator_random', v={'FROM': 0, 'TO': 256})), wait(500)]))],
  quiz=[dict(q='map(512, 0, 1023, 0, 100) ได้ประมาณเท่าไร', choices=['50', '512', '100'], answer=0, why='512 อยู่กลางช่วงเดิม จึงได้กลางช่วงใหม่'),
        dict(q='constrain(130, 0, 100) ได้เท่าไร', choices=['100', '130', '0'], answer=0, why='เกินสูงสุดจึงได้ค่าสูงสุด')]))

L.append(dict(id='u4-text', unit=4, cat='ops', title='ข้อความ: join · letter of · length · แปลงชนิด',
  goals=['ต่อข้อความกับตัวเลขเพื่อแสดงผล', 'รู้ข้อแตกต่างการนับตำแหน่งตัวอักษร'],
  intro='บล็อกข้อความใช้คลาส <code>String</code> ของ Arduino เหมาะกับการแสดงผลบนจอหรือ Serial',
  blocks=['operator_join', 'operator_join_three', 'operator_letter_of', 'operator_length', 'operator_toString', 'operator_toFloat'],
  examples=[
    dict(title='แสดงแบตพร้อมหน่วย', desc='ต่อคำว่า BAT กับค่าแรงดันและตัว V',
         xml=P(setup=[oled_size(2)], loop=[oled_clear(), oled_print(B('operator_join_three', v={'STRING1': 'BAT ', 'STRING2': B('mini_PWR_getVolt'), 'STRING3': ' V'}), 0, 8), wait(1000)]),
         notes=[('String("BAT ") + String(MiniR4.PWR.getBattVoltage()) + String(" V")', 'แปลงทุกชิ้นเป็น String แล้วต่อด้วย +')]),
    dict(title='ตำแหน่งตัวอักษร', desc='letter 1 of “world” ในบล็อก แต่ในโค้ด <code>charAt(1)</code> นับจาก 0 จึงได้ <b>o</b>',
         xml=P(setup=[oled_print(B('operator_letter_of', v={'LETTER': 1, 'STRING': 'world'}), 0, 0, 'No'), oled_print(B('operator_length', v={'STRING': 'world'}), 0, 16)])),
  ],
  arduino=['<code>String("world").charAt(0)</code> คือ w — ภาษา C++ นับตำแหน่งเริ่มที่ 0',
           'บล็อก to Number ที่พิมพ์ตัวเลขลงช่องตรง ๆ จะคอมไพล์ไม่ผ่าน ใน Arduino เขียน <code>String("100.1").toFloat()</code>'],
  tries=[dict(task='แสดง “SPEED: ” ตามด้วยค่าตัวแปร speed',
              solution=P(setup=[setvar('speed', '75'), oled_size(2), oled_print(B('operator_join', v={'STRING1': 'SPEED: ', 'STRING2': VAR('speed')}), 0, 8)]), vars=['speed'])],
  quiz=[dict(q='String("robot").length() ได้เท่าไร', choices=['5', '4', '6'], answer=0, why='r-o-b-o-t'),
        dict(q='String("robot").charAt(0) ได้ตัวอะไร', choices=['r', 'o', 'b'], answer=0, why='ตำแหน่ง 0 คือตัวแรก')]))

# =====================================================================
# หน่วยที่ 6 บังคับหุ่นผ่านมือถือ — Bluetooth (6.1–6.5)
# มือถือเปิดหน้าจอย rc/?p=<rc> ส่งข้อความ: F B L R (ทิศ) · S (หยุด) · เลขคันโยก (ซ้าย+100)×1000 + (ขวา+100) · U D (ปุ่มแขน)
# =====================================================================
NAME = 'R4-T01'

# ทางเชื่อมต่อ: บล็อกที่ต่างกันระหว่าง Bluetooth กับ MQTT (ตรรกะขับเหมือนกัน) · quiet = เงียบกี่ ms ถึงถือว่าสัญญาณหาย
VIA_BLE = dict(data=ble_data, connected=ble_connected, poll=ble_poll, hat=ble_on_received, quiet=500)
VIA_MQTT = dict(data=mqtt_msg, connected=mqtt_connected, poll=mqtt_loop, hat=mqtt_on_message, quiet=1000)


def got(text, via=VIA_BLE):
    """received data = "text" (เทียบข้อความที่มือถือส่งมาตรง ๆ เพราะตัวแปรของบล็อกเป็น float เก็บข้อความไม่ได้)"""
    return cmp('operator_equals', via['data'](), text)


def when(cond, stmts):
    return B('control_if', v={'CONDITION': cond}, s={'SUBSTACK': list(stmts)})


def either(cond, yes, no):
    return B('control_if_else', v={'CONDITION': cond}, s={'SUBSTACK': list(yes), 'SUBSTACK2': list(no)})


def show_name(name=NAME):
    """ชื่อหุ่นขึ้นจอ OLED ตอนเปิดเครื่อง หุ่นหลายตัวในห้องจะได้เลือกถูกตัว"""
    return [oled_size(2), oled_clear(), oled_print(name, 0, 8)]


def wheels(l, r):
    return [setvar('l', str(l)), setvar('r', str(r))]


def since_last(ms):
    return cmp('operator_gt', op('operator_subtract', millis(), VAR('last')), N(ms))


def lost(ms=None, via=VIA_BLE):
    """หลุดการเชื่อมต่อ หรือเงียบเกิน ms (ไม่ใส่ = ค่าของทางเชื่อมต่อนั้น)"""
    return B('operator_or', v={'OPERAND1': B('operator_not', v={'OPERAND': via['connected']()}), 'OPERAND2': since_last(ms or via['quiet'])})


def drive_loop(on_stop=(), on_move=(), via=VIA_BLE):
    """loop ของบท 6.3–6.5 และ 6.8: ระบบกันหลุด แล้วสั่งล้อตาม l, r (on_stop / on_move = บล็อกเพิ่มต่อท้ายแต่ละกรณี)"""
    stopped = B('operator_and', v={'OPERAND1': cmp('operator_equals', VAR('l'), N(0)), 'OPERAND2': cmp('operator_equals', VAR('r'), N(0))})
    return [via['poll'](), when(lost(via=via), wheels(0, 0)),
            either(stopped, [stop_moving()] + list(on_stop), [moving(VAR('l'), VAR('r'))] + list(on_move))]


HOLD = [('F', 50, 50), ('B', -50, -50), ('L', -40, 40), ('R', 40, -40), ('S', 0, 0)]


def stick_hat(letters=(), via=VIA_BLE):
    """เลขคันโยก ≥ 1000 → แยกเป็น l, r · ตัวอักษร (toFloat ได้ 0) → S หยุด และคำสั่งอื่นใน letters"""
    return via['hat']([
        setvar('last', millis()),
        setvar('v', to_float(via['data']())),
        either(cmp('operator_gte', VAR('v'), N(1000)),
               [setvar('l', op('operator_subtract', mathop('floor', op('operator_divide', VAR('v'), N(1000))), N(100))),
                setvar('r', op('operator_subtract', op('operator_mod', VAR('v'), N(1000)), N(100)))],
               [when(got('S', via), wheels(0, 0))] + list(letters))])


def arm(via=VIA_BLE):
    """ปุ่มพิเศษ U / D → เซอร์โว RC1 แขนขึ้น 150° / ลง 60°"""
    return [when(got('U', via), [servo('RC1', 150)]), when(got('D', via), [servo('RC1', 60)])]


ARM = arm()

# ตัวอย่าง C++ ล้วน (ไม่มีบล็อก): ข้อความแบบ J,60,40 ตัดด้วย indexOf / substring
STICK_TEXT_CPP = r'''#include <ArduinoBLE.h>
#define ENABLE_DRIVEDC_BRAKE_DELAY
#include "MatrixMiniR4.h"

BLEService uartService("6E400001-B5A3-F393-E0A9-E50E24DCCA9E");
BLEStringCharacteristic rxChar("6E400002-B5A3-F393-E0A9-E50E24DCCA9E", BLEWrite, 128);
BLEStringCharacteristic txChar("6E400003-B5A3-F393-E0A9-E50E24DCCA9E", BLERead | BLENotify, 128);
int l = 0;
int r = 0;
unsigned long last = 0;

void onBLEWritten(BLEDevice central, BLECharacteristic characteristic) {
  String data = rxChar.value();
  last = millis();
  if (data.startsWith("J,")) {
    int comma = data.indexOf(',', 2);
    l = data.substring(2, comma).toInt();
    r = data.substring(comma + 1).toInt();
  }
  else if (data == "S") {
    l = 0;
    r = 0;
  }
}

void setup()
{
  MiniR4.begin();
  MiniR4.PWR.setBattCell(2);
  BLE.begin();
  BLE.setLocalName("R4-T01");
  BLE.setAdvertisedService(uartService);
  uartService.addCharacteristic(rxChar);
  uartService.addCharacteristic(txChar);
  BLE.addService(uartService);
  rxChar.setEventHandler(BLEWritten, onBLEWritten);
  BLE.advertise();
  MiniR4.DriveDC.begin(1, 2, false, true);
  MiniR4.OLED.setTextSize(2);
  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(0, 8);
  MiniR4.OLED.print("R4-T01");
  MiniR4.OLED.display();
}

void loop()
{
  BLE.poll();
  if (!BLE.connected() || millis() - last > 500) {
    l = 0;
    r = 0;
  }
  if (l == 0 && r == 0) {
    MiniR4.DriveDC.brake(true);
  }
  else {
    MiniR4.DriveDC.Move(l, r);
  }
}
'''

L.append(dict(id='u6-ble-hello', unit=6, cat='iot', rc='hello', title='Bluetooth ครั้งแรก: ตั้งชื่อหุ่น ส่งข้อความ หุ่นตอบกลับ',
  goals=['เปิด Bluetooth ตั้งชื่อหุ่นไม่ให้ซ้ำกับเพื่อน แล้วต่อจากมือถือ', 'รับข้อความจากมือถือด้วยบล็อกหมวก และส่งข้อความกลับไปที่มือถือ'],
  intro='บอร์ด UNO R4 WiFi มี Bluetooth LE ในตัว ใช้บล็อกหมวด <b>IoT</b> ต่อกับมือถือได้โดยไม่ต้องมีเน็ต ฝั่งมือถือเปิด<b>หน้าจอย</b>ของเว็บนี้ (ปุ่มสีม่วง “เปิดจอยของบทนี้” ด้านล่าง) กด “เชื่อมต่อ” แล้วเลือกชื่อหุ่นของเรา โปรแกรมมีสองส่วน: ใน <b>R4 Begin</b> เปิด Bluetooth แล้ววน <b>BLE Polling</b> ตลอด ส่วนบล็อกหมวก <b>When BLE UART Data Received</b> วางแยกไว้<b>ใต้</b> R4 Begin ทำงานทุกครั้งที่มือถือส่งข้อความมา',
  blocks=['mini_ble_begin', 'mini_ble_set_name', 'mini_ble_uart_enable', 'mini_ble_poll', 'mini_ble_connected', 'mini_ble_on_received', 'mini_ble_received_data', 'mini_ble_uart_send'],
  examples=[
    dict(title='สวัสดี Bluetooth', desc='จอขึ้นชื่อหุ่น ไฟแดงรอ มือถือต่อติดแล้วไฟเป็นสีเขียว พิมพ์ข้อความในหน้าจอยแล้วกดส่ง ข้อความขึ้นจอ OLED และหุ่นตอบ OK กลับมา',
         xml=P(setup=ble_setup(NAME) + show_name(),
               loop=[ble_poll(), either(ble_connected(), [led(0, 255, 0)], [led(255, 0, 0)])],
               extra=[ble_on_received([oled_clear(), oled_print(ble_data(), 0, 8), ble_send('OK')])]),
         notes=[('#include &lt;ArduinoBLE.h&gt;', 'ไลบรารี Bluetooth ของ Arduino บล็อก BLE ใส่บรรทัดนี้ให้เอง'),
                ('BLE.setLocalName("R4-T01");', 'ชื่อที่มือถือเห็นตอนค้นหา หุ่นทุกตัวในห้องต้องใช้ชื่อไม่ซ้ำกัน'),
                ('void onBLEWritten(', 'บล็อกหมวกกลายเป็นฟังก์ชันนี้ อยู่นอก <code>setup()</code> และ <code>loop()</code> ถูกเรียกทุกครั้งที่มือถือส่งข้อความมา'),
                ('ble_rcvData = rxChar.value();', 'เก็บข้อความที่ได้รับไว้ใน <code>ble_rcvData</code> (ชนิด String) บล็อก Received Data ก็คือตัวแปรนี้'),
                ('txChar.writeValue(String("OK"));', 'ส่งข้อความกลับไปที่มือถือ ขึ้นในหน้าต่างข้อความของหน้าจอย'),
                ('BLE.poll();', 'ให้บอร์ดตรวจ Bluetooth ทุกรอบ <code>onBLEWritten</code> ถูกเรียกจากในคำสั่งนี้ ถ้า loop มี wait นาน ข้อความจะเข้าช้า'),
                ('if(BLE.connected())', 'มือถือต่ออยู่ไหม ใช้ทำไฟบอกสถานะ')]),
    dict(title='ส่งค่าแบตไปมือถือทุก 1 วินาที', desc='แรงดันแบตขึ้นในหน้าต่างข้อความของหน้าจอยทุก 1 วินาที ใช้ millis จับเวลา (บทเวลาในหน่วยที่ 3) loop จึงยังวนเร็วและรับข้อความได้ตลอด',
         xml=P(setup=ble_setup(NAME) + show_name() + [setvar('last', '0')],
               loop=[ble_poll(), when(since_last(1000), [setvar('last', millis()), ble_send(B('mini_PWR_getVolt'))])],
               extra=[ble_on_received([oled_clear(), oled_print(ble_data(), 0, 8)])]),
         vars=['last'],
         notes=[('if((millis() - last) > 1000)', 'ผ่านไปเกิน 1 วินาทีจากครั้งที่ส่งล่าสุดหรือยัง'),
                ('txChar.writeValue(String(MiniR4.PWR.getBattVoltage()));', 'เปลี่ยนตัวเลขเป็นข้อความแล้วส่ง มือถือได้ข้อความเช่น 7.85'),
                ('MiniR4.OLED.print(ble_rcvData);', 'บล็อกหมวกต้องมีเสมอ ถึงไม่ได้ใช้มากก็ให้ทำอะไรง่าย ๆ เช่นโชว์ข้อความที่ได้รับ')]),
  ],
  arduino=['มือถือ <b>Android</b> เปิดหน้าจอยด้วย <b>Chrome</b> · <b>iPhone/iPad</b> ใช้แอป <b>Bluefy</b> (Safari ต่อ Bluetooth จากเว็บไม่ได้) ไม่ต้องจับคู่ในหน้าตั้งค่า Bluetooth ของมือถือ กด “เชื่อมต่อ” ในหน้าจอยแล้วเลือกชื่อหุ่นได้เลย',
           'หุ่นทุกตัวในห้องต้องมีชื่อไม่ซ้ำ เปลี่ยน <code>R4-T01</code> เป็นเลขทีมของตัวเอง (ใช้ตัวอังกฤษ ตัวเลข และ - เท่านั้น) ตอนกดเชื่อมต่อ ให้เลือกชื่อหุ่นของทีมตัวเองจากรายการ',
           '<b>ข้อควรระวัง 1:</b> มีบล็อก BLE Enable Nordic UART Service แต่ไม่มีบล็อกหมวก When BLE UART Data Received → คอมไพล์ไม่ผ่าน <code>\'onBLEWritten\' was not declared</code> ต้องมีบล็อกหมวกเสมอ แม้ข้างในจะยังว่าง',
           '<b>ข้อควรระวัง 2:</b> วางบล็อกหมวกไว้<b>ใต้</b> R4 Begin ถ้าวางสูงกว่า → คอมไพล์ไม่ผ่าน <code>\'rxChar\' was not declared</code> เพราะตัวสร้างโค้ดเรียงบล็อกจากบนลงล่าง',
           'เขียนเองใน Arduino IDE ต้องติดตั้งไลบรารี <b>ArduinoBLE</b> ก่อน (Sketch → Include Library → Manage Libraries) ถ้ามือถือค้นไม่เจอหุ่น ลองอัปเดตเฟิร์มแวร์ไร้สายของบอร์ด: Tools → <b>Firmware Updater</b>'],
  tries=[dict(task='พิมพ์ <code>hi</code> แล้วให้หุ่นตอบ <code>hello</code> ข้อความอื่นตอบ <code>OK</code> เหมือนเดิม (ใช้ if … else กับบล็อก = )',
              solution=P(setup=ble_setup(NAME) + show_name(), loop=[ble_poll()],
                         extra=[ble_on_received([oled_clear(), oled_print(ble_data(), 0, 8), either(got('hi'), [ble_send('hello')], [ble_send('OK')])])]),
              answer='เทียบด้วย <code>ble_rcvData == "hi"</code> ตัวพิมพ์เล็ก-ใหญ่ต้องตรงกัน <code>hi</code> กับ <code>Hi</code> คือคนละคำ'),
         dict(task='ส่งค่าแบตเฉพาะตอนมือถือต่ออยู่ และส่งทุก 2 วินาที (ใช้บล็อก and)',
              solution=P(setup=ble_setup(NAME) + show_name() + [setvar('last', '0')],
                         loop=[ble_poll(), when(B('operator_and', v={'OPERAND1': ble_connected(), 'OPERAND2': since_last(2000)}), [setvar('last', millis()), ble_send(B('mini_PWR_getVolt'))])],
                         extra=[ble_on_received([oled_clear(), oled_print(ble_data(), 0, 8)])]),
              vars=['last'])],
  quiz=[dict(q='มีบล็อก BLE Enable Nordic UART Service แต่ลืมบล็อกหมวก When BLE UART Data Received จะเกิดอะไร', choices=['คอมไพล์ไม่ผ่าน เพราะไม่มีฟังก์ชัน onBLEWritten', 'อัปโหลดได้ แต่รับข้อความไม่ได้', 'มือถือหาชื่อหุ่นไม่เจอ'], answer=0,
             why='โค้ดของ UART enable เรียกใช้ <code>onBLEWritten</code> ซึ่งสร้างจากบล็อกหมวก'),
        dict(q='ในห้องมีหุ่น 10 ตัว ทำไมต้องตั้งชื่อ Bluetooth ไม่ซ้ำกัน', choices=['มือถือจะเห็นชื่อซ้ำในรายการ เลือกผิดแล้วไปบังคับหุ่นของเพื่อน', 'ในห้องหนึ่งต่อ Bluetooth ได้ทีละตัว', 'ชื่อซ้ำทำให้คอมไพล์ไม่ผ่าน'], answer=0,
             why='ทุกตัวประกาศชื่อพร้อมกัน ถ้าชื่อเหมือนกันจะแยกไม่ออก'),
        dict(q='ทำไมตัวอย่างที่ 2 ไม่ใช้ wait 1000 ใน loop', choices=['ระหว่าง wait บอร์ดไม่ได้เรียก BLE.poll() ข้อความจากมือถือจะเข้าช้า', 'wait ใช้คู่กับ Bluetooth ไม่ได้ คอมไพล์ไม่ผ่าน', 'millis ส่งข้อความได้เร็วกว่า'], answer=0,
             why='<code>BLE.poll()</code> ต้องถูกเรียกบ่อย ๆ บล็อกหมวกจึงทำงานทันทีที่ข้อความมาถึง')]))

L.append(dict(id='u6-ble-tap', unit=6, cat='iot', rc='tap4', title='ปุ่ม 4 ทิศ: กด 1 ครั้ง เดิน 0.5 วินาที',
  goals=['เทียบข้อความที่ได้รับกับตัวอักษร F B L R', 'สั่งเดินหรือเลี้ยวช่วงสั้น ๆ ด้วย Move(Sync) for … seconds'],
  intro='หน้าจอยแบบ<b>ปุ่ม 4 ทิศ (กดครั้งเดียว)</b> ส่งตัวอักษรหนึ่งตัวต่อการกดหนึ่งครั้ง: <code>F</code> เดินหน้า <code>B</code> ถอยหลัง <code>L</code> เลี้ยวซ้าย <code>R</code> เลี้ยวขวา ในบล็อกหมวกเราเอา <b>BLE UART Received Data</b> ไปเทียบกับตัวอักษรด้วยบล็อก <b>=</b> ถ้าตรงก็สั่งเดิน 0.5 วินาที',
  blocks=['operator_equals', 'mini_ddc_runFor_sync'],
  examples=[
    dict(title='เดินหน้า-ถอยหลัง', desc='เริ่มจากสองปุ่มก่อน กด ▲ หรือ ▼ ในหน้าจอย หุ่นขยับทีละนิด',
         xml=P(setup=ble_setup(NAME) + [drive_setup()] + show_name(), loop=[ble_poll()],
               extra=[ble_on_received([when(got('F'), [move_sync_time(50, 50, 0.5)]), when(got('B'), [move_sync_time(-50, -50, 0.5)])])]),
         notes=[('if(ble_rcvData == "F")', 'เทียบข้อความทั้งคำ ต้องตรงทุกตัวอักษร ตัวเล็ก <code>f</code> ไม่นับ'),
                ('MiniR4.DriveDC.MoveSyncTime(50, 50, 0.5, true);', 'เดินแบบ Sync กำลัง 50 นาน 0.5 วินาทีแล้วเบรก คำสั่งนี้รอจนเดินเสร็จ'),
                ('MiniR4.DriveDC.begin(1, 2, false, true);', 'อย่าลืม Set Movement ใน Setup ไม่อย่างนั้นล้อไม่หมุน')]),
    dict(title='ครบ 4 ทิศ และดูคำสั่งบนจอ', desc='เลี้ยวด้วยล้อหมุนสวนกัน และโชว์ตัวอักษรที่ได้รับไว้ท้ายชื่อหุ่น ถ้าหุ่นไม่ขยับ ดูจอก่อนว่าได้รับอะไรมา',
         xml=P(setup=ble_setup(NAME) + [drive_setup()] + show_name(), loop=[ble_poll()],
               extra=[ble_on_received([oled_clear(), oled_print(NAME, 0, 8, 'No'), oled_print(ble_data(), 100, 8),
                                       when(got('F'), [move_sync_time(50, 50, 0.5)]), when(got('B'), [move_sync_time(-50, -50, 0.5)]),
                                       when(got('L'), [move_sync_time(-50, 50, 0.5)]), when(got('R'), [move_sync_time(50, -50, 0.5)])])]),
         notes=[('MiniR4.OLED.setCursor(100, 8);', 'ตัวอักษรที่ได้รับขึ้นทางขวาของชื่อหุ่น ชื่อจึงยังอยู่บนจอ'),
                ('MiniR4.DriveDC.MoveSyncTime((-50), 50, 0.5, true);', 'ล้อซ้ายถอย ล้อขวาเดิน → หมุนซ้ายอยู่กับที่'),
                ('MiniR4.DriveDC.MoveSyncTime(50, (-50), 0.5, true);', 'สลับกัน → หมุนขวา')]),
  ],
  arduino=['ข้อความที่ได้รับเป็น <code>String</code> ชื่อ <code>ble_rcvData</code> แต่ตัวแปรที่สร้างในบล็อกเป็น float ทั้งหมด เก็บตัวอักษรไม่ได้ จึงเอาบล็อก Received Data ไปเทียบด้วย = ในบล็อกหมวกเลย',
           'Move(Sync) for … seconds → <code>MoveSyncTime(ซ้าย, ขวา, วินาที, เบรก)</code> <b>รอจนเดินเสร็จ</b> ระหว่างนั้นบอร์ดไม่อ่านข้อความใหม่ กดรัวเกินไปหุ่นจะตามไม่ทัน',
           'ใน C++ เขียน if … else if ต่อกันได้ เช่น <code>if (ble_rcvData == "F") { … } else if (ble_rcvData == "B") { … }</code>'],
  tries=[dict(task='เพิ่มแตร: ในหน้าสร้างจอย กด “+ เพิ่มปุ่ม” ตั้งข้อความตอนกดเป็น <code>H</code> แล้วให้หุ่นบี๊บ 0.2 วินาทีเมื่อได้รับ <code>H</code>',
              solution=P(setup=ble_setup(NAME) + [drive_setup()] + show_name(), loop=[ble_poll()],
                         extra=[ble_on_received([when(got('F'), [move_sync_time(50, 50, 0.5)]), when(got('B'), [move_sync_time(-50, -50, 0.5)]),
                                                 when(got('L'), [move_sync_time(-50, 50, 0.5)]), when(got('R'), [move_sync_time(50, -50, 0.5)]),
                                                 when(got('H'), [B('mini_Buzzer_Tone', v={'FREQ': 880, 'VOL': 200})])])]),
              answer='ปุ่มพิเศษส่งข้อความอะไรก็ได้ที่ตั้งไว้ หุ่นแค่ต้องมี if ที่เทียบข้อความนั้น')],
  quiz=[dict(q='มือถือส่ง <code>f</code> (ตัวเล็ก) หุ่นในตัวอย่างจะทำอะไร', choices=['ไม่ขยับ เพราะ "f" ไม่เท่ากับ "F"', 'เดินหน้าตามปกติ', 'คอมไพล์ไม่ผ่าน'], answer=0,
             why='การเทียบข้อความแยกตัวพิมพ์เล็ก-ใหญ่'),
        dict(q='ทำไมเอาบล็อก = ไปเทียบกับ Received Data ตรง ๆ ไม่เก็บใส่ตัวแปรก่อน', choices=['ตัวแปรของบล็อกเป็น float เก็บตัวอักษรไม่ได้', 'ตัวแปรทำให้หุ่นช้าลง', 'บล็อกหมวกใช้ตัวแปรไม่ได้'], answer=0,
             why='MATRIXblock ประกาศตัวแปรทุกตัวเป็น float ส่วนข้อความอยู่ใน <code>ble_rcvData</code> ที่เป็น String'),
        dict(q='ระหว่างที่หุ่นกำลังเดิน 0.5 วินาที กดปุ่มอื่นซ้ำ ๆ จะเป็นอย่างไร', choices=['บอร์ดยังไม่อ่านข้อความใหม่จนกว่าจะเดินเสร็จ', 'หุ่นหยุดทันทีแล้วทำคำสั่งใหม่', 'หุ่นเดินเร็วขึ้น'], answer=0,
             why='<code>MoveSyncTime</code> รอจนเดินครบ ระหว่างนั้นไม่ได้เรียก <code>BLE.poll()</code> บทถัดไปจึงใช้ Moving ที่ไม่ต้องรอ')]))

L.append(dict(id='u6-ble-hold', unit=6, cat='iot', rc='hold4', title='กดค้างเดิน ปล่อยหยุด และหยุดเองเมื่อสัญญาณหาย',
  goals=['ให้บล็อกหมวกแค่จำคำสั่ง แล้วให้ loop สั่งล้อด้วย Moving at …', 'ทำระบบกันหลุด: มือถือหลุด หรือเงียบเกิน 0.5 วินาที หุ่นต้องหยุดเอง'],
  intro='หน้าจอยแบบ<b>ปุ่ม 4 ทิศ (กดค้าง)</b> ส่งตัวอักษรซ้ำทุก 0.15 วินาทีตลอดที่นิ้วยังกดอยู่ และส่ง <code>S</code> ตอนปล่อย บล็อก <b>Moving at …</b> ทำให้หุ่นวิ่งค้างจนกว่าจะสั่งหยุด ถ้าสัญญาณหลุดกลางทาง ข้อความ S จะไม่มาถึง หุ่นจะวิ่งต่อไปเรื่อย ๆ บทนี้จึงให้หุ่น<b>จำเวลา</b>ที่ได้รับข้อความล่าสุดไว้ในตัวแปร <code>last</code> ถ้าเงียบเกิน 0.5 วินาที หรือมือถือหลุด ให้หยุดเอง',
  blocks=['mini_ddc_on', 'mini_ddc_off', 'mini_millis', 'operator_or', 'operator_not'],
  examples=[
    dict(title='ทดลองระบบกันหลุดด้วยไฟ', desc='ยังไม่ขับล้อ ลองให้ปลอดภัยก่อน: กดปุ่มในหน้าจอยค้างไว้ไฟเขียว ปล่อยแล้วผ่านไป 0.5 วินาทีไฟเป็นสีแดง',
         xml=P(setup=ble_setup(NAME) + show_name() + [setvar('last', '0')],
               loop=[ble_poll(), either(lost(), [led(255, 0, 0)], [led(0, 255, 0)])],
               extra=[ble_on_received([setvar('last', millis())])]),
         vars=['last'],
         notes=[('last = millis();', 'ทุกครั้งที่มีข้อความเข้ามา จำเวลาไว้ในตัวแปร <code>last</code>'),
                ('if((!BLE.connected())||((millis() - last) > 500))', '<code>!</code> คือ not: มือถือ<b>ไม่ได้</b>ต่ออยู่ · <code>||</code> คือ or · หรือเงียบมาเกิน 500 ms แล้ว (กดค้างจอยส่งทุก 150 ms ถ้าสัญญาณดีจะไม่เงียบนานขนาดนี้)')]),
    dict(title='กดค้างเดิน ปล่อยหยุด', desc='บล็อกหมวกเปลี่ยนตัวอักษรเป็นกำลังล้อซ้าย <code>l</code> และล้อขวา <code>r</code> ส่วน loop เช็กระบบกันหลุดแล้วสั่งล้อทุกรอบ',
         xml=P(setup=ble_setup(NAME) + [drive_setup()] + show_name(),
               loop=drive_loop(),
               extra=[ble_on_received([setvar('last', millis())] + [when(got(k), wheels(a, b)) for k, a, b in HOLD])]),
         vars=['last', 'l', 'r'],
         notes=[('if(ble_rcvData == "L")', 'เลี้ยวซ้าย: ล้อซ้าย −40 ล้อขวา 40 หมุนอยู่กับที่ช้ากว่าเดินตรง จะได้เล็งง่าย'),
                ('if(ble_rcvData == "S")', 'ปล่อยนิ้ว → จอยส่ง S → ตั้งกำลังเป็น 0 ทั้งสองล้อ'),
                ('MiniR4.DriveDC.Move(l, r);', 'Moving at … สั่งแล้วไปต่อทันทีไม่ต้องรอ loop จึงวนเร็วและรับข้อความได้ตลอด'),
                ('MiniR4.DriveDC.brake(true);', 'หยุดเมื่อ l และ r เป็น 0 ทั้งคู่')]),
  ],
  arduino=['แบ่งหน้าที่ให้ชัด: <code>onBLEWritten</code> แค่จำค่า (<code>l</code>, <code>r</code>, <code>last</code>) ส่วน <code>loop()</code> เป็นคนสั่งล้อ เงื่อนไขความปลอดภัยจึงอยู่ที่เดียว',
           'สัญญาณหายแบบเงียบ ๆ (เดินออกนอกระยะ) บอร์ดอาจใช้เวลาหลายวินาทีกว่า <code>BLE.connected()</code> จะเป็น false การจับเวลาเงียบ 0.5 วินาทีจึงหยุดได้เร็วกว่า',
           'ตัวแปรของบล็อกเป็น float เก็บค่า millis ได้ตรงราว 4 ชั่วโมงแรกหลังเปิดเครื่อง เขียนเองควรใช้ <code>unsigned long last;</code>',
           'ทดสอบบนโต๊ะก่อน: ยกหุ่นให้ล้อลอย กดค้างแล้วปล่อย ดูว่าล้อหยุดจริงก่อนวางลงพื้น'],
  tries=[dict(task='เพิ่มไฟบอกสถานะ: ล้อหมุนอยู่ไฟสีฟ้า หยุดแล้วไฟดับ',
              solution=P(setup=ble_setup(NAME) + [drive_setup()] + show_name(),
                         loop=drive_loop(on_stop=[led(0, 0, 0)], on_move=[led(0, 0, 255)]),
                         extra=[ble_on_received([setvar('last', millis())] + [when(got(k), wheels(a, b)) for k, a, b in HOLD])]),
              vars=['last', 'l', 'r']),
         dict(task='เปลี่ยนการเลี้ยวเป็นแบบโค้ง: <code>L</code> ให้ล้อซ้าย 10 ล้อขวา 50 และ <code>R</code> ให้ล้อซ้าย 50 ล้อขวา 10',
              solution=P(setup=ble_setup(NAME) + [drive_setup()] + show_name(),
                         loop=drive_loop(),
                         extra=[ble_on_received([setvar('last', millis())] + [when(got(k), wheels(a, b)) for k, a, b in
                                                 [('F', 50, 50), ('B', -50, -50), ('L', 10, 50), ('R', 50, 10), ('S', 0, 0)]])]),
              vars=['last', 'l', 'r'],
              answer='ล้อหนึ่งยังเดินหน้าอยู่ หุ่นจึงวิ่งโค้งแทนหมุนอยู่กับที่')],
  quiz=[dict(q='ถ้าลบระบบกันหลุดออก แล้วสัญญาณหายตอนกดเดินหน้าค้างอยู่ จะเกิดอะไร', choices=['หุ่นวิ่งต่อไปเรื่อย ๆ เพราะ l, r ยังเป็น 50 และข้อความ S มาไม่ถึง', 'หุ่นหยุดเองทันที', 'หุ่นถอยกลับมาหามือถือ'], answer=0,
             why='Moving at … ไม่หยุดเอง ต้องมีคำสั่งหยุด'),
        dict(q='มีบล็อก BLE Connected? แล้ว ทำไมยังต้องเช็ก millis − last &gt; 500 ด้วย', choices=['สัญญาณหายแบบเงียบ ๆ บอร์ดอาจรู้ตัวช้าหลายวินาที', 'BLE Connected? ใช้ใน loop ไม่ได้', 'millis ทำให้หุ่นวิ่งเร็วขึ้น'], answer=0,
             why='ระหว่างกดค้าง จอยส่งซ้ำทุก 0.15 วินาที ถ้าเงียบเกิน 0.5 วินาทีแปลว่าสัญญาณมีปัญหา หุ่นจึงหยุดไว้ก่อน'),
        dict(q='ทำไมบทนี้ใช้ Moving at … ใน loop แทน Move(Sync) for 0.5 seconds', choices=['Moving ไม่ต้องรอ loop จึงวนเร็วและรับข้อความได้ตลอด', 'Moving แม่นกว่า', 'Move(Sync) ใช้กับ Bluetooth ไม่ได้'], answer=0,
             why='ถ้าคำสั่งรอจนเดินเสร็จ หุ่นจะหยุดช้าตอนปล่อยปุ่ม')]))

L.append(dict(id='u6-ble-stick', unit=6, cat='iot', rc='stick1', title='คันโยกเดียว: แยกเลขเดียวเป็นกำลังล้อซ้าย-ขวา',
  goals=['แปลงข้อความตัวเลขเป็นค่าตัวเลขด้วย to Number', 'แยกเลขเดียวเป็นสองค่าด้วย ÷ floor และ mod'],
  intro='คันโยกต้องส่งทั้งกำลังล้อซ้ายและล้อขวาใน<b>ข้อความเดียว</b> แต่ MATRIXblock ไม่มีบล็อกตัดข้อความ จอยจึงรวมสองค่าเป็นเลขเดียว: <code>(ซ้าย + 100) × 1000 + (ขวา + 100)</code> เช่น ซ้าย 60 ขวา 40 ส่งเป็น <code>160140</code> หุ่นแยกกลับด้วยการหาร: floor(160140 ÷ 1000) = 160 → 160 − 100 = <b>60</b> และ 160140 mod 1000 = 140 → 140 − 100 = <b>40</b> ระหว่างที่จับคันโยก จอยส่งซ้ำทุก 0.1 วินาที และส่ง <code>S</code> ตอนปล่อย',
  blocks=['operator_toFloat', 'operator_divide', 'operator_mathop', 'operator_mod', 'operator_gte'],
  examples=[
    dict(title='ขับด้วยคันโยก', desc='loop เหมือนบท 6.3 ทุกบล็อก (ระบบกันหลุดเดิม) เปลี่ยนเฉพาะบล็อกหมวก',
         xml=P(setup=ble_setup(NAME) + [drive_setup()] + show_name(), loop=drive_loop(), extra=[stick_hat()]),
         vars=['last', 'v', 'l', 'r'],
         notes=[('v = ble_rcvData.toFloat();', 'ข้อความ "160140" → ตัวเลข 160140 ข้อความที่ไม่ใช่ตัวเลข เช่น "S" ได้ 0'),
                ('if(v >= 1000)', 'เลขคันโยก ≥ 1000 เสมอ ส่วนตัวอักษรได้ 0 จึงตกไปที่ else'),
                ('l = floor((v / 1000)) - 100;', '160140 ÷ 1000 = 160.14 → floor → 160 → −100 → ล้อซ้าย 60'),
                ('r = (fmod(v, 1000)) - 100;', 'เศษจากการหารด้วย 1000 = 140 → −100 → ล้อขวา 40'),
                ('MiniR4.DriveDC.Move(l, r);', 'loop เดิมจากบท 6.3 สั่งล้อตามค่าที่แยกได้')]),
    dict(title='ต่อยอดใน C++: ส่งเป็นข้อความ J,60,40', codeOnly=True, code=STICK_TEXT_CPP,
         desc='ตัวอย่างนี้เป็นโค้ด C++ ล้วน ไม่มีบล็อก ใน Arduino IDE ตัดข้อความได้ด้วย <code>indexOf</code> และ <code>substring</code> แต่จอยของเว็บนี้ส่งเป็นเลขเดียว ถ้าจะใช้แบบนี้ต้องแก้ไฟล์หน้าจอยที่ก๊อปไป (บท 6.6) ให้ส่ง <code>"J," + ซ้าย + "," + ขวา</code> แทน',
         notes=[('if (data.startsWith("J,"))', 'ข้อความคันโยกขึ้นต้นด้วย J และจุลภาค'),
                ("int comma = data.indexOf(',', 2);", 'หาตำแหน่งจุลภาคตัวที่สอง (เริ่มค้นที่ตำแหน่ง 2) ใน "J,60,40" ได้ 4'),
                ('l = data.substring(2, comma).toInt();', 'ตัดตำแหน่ง 2 ถึงก่อนจุลภาค ได้ "60" แล้วแปลงเป็นเลข'),
                ('r = data.substring(comma + 1).toInt();', 'ตัดหลังจุลภาคจนจบ ได้ "40"'),
                ('unsigned long last = 0;', 'เขียนเองเลือกชนิดตัวแปรได้: <code>int</code> สำหรับกำลังล้อ <code>unsigned long</code> สำหรับเวลา')]),
  ],
  arduino=['ทำไมจอยจำกัดแต่ละล้อไว้ที่ −99 ถึง 99: ซ้าย + 100 จึงอยู่ระหว่าง 1 ถึง 199 เลขที่ส่งจึง ≥ 1000 เสมอ (ต่ำสุด ซ้าย −99 ขวา −99 → <code>1001</code>) ส่วน <code>toFloat("S")</code> ได้ 0 หุ่นจึงแยกเลขคันโยกออกจากตัวอักษรได้',
           'float เก็บจำนวนเต็มได้ตรงถึงราว 16 ล้าน เลขคันโยกสูงสุด 199199 จึงไม่คลาด',
           'เขียนเองด้วย <code>long</code> ใช้ <code>v / 1000</code> (หารจำนวนเต็ม ตัดเศษให้เอง) และ <code>v % 1000</code> แทน floor และ fmod ได้',
           'ตัวอย่างที่ 2 คัดลอกไปวางใน Arduino IDE ได้ทั้งไฟล์ (ติดตั้งไลบรารี ArduinoBLE ก่อน)'],
  tries=[dict(task='ทดสอบก่อนขับ: แสดงค่า <code>l</code> และ <code>r</code> บนจอ OLED ทุกครั้งที่ได้รับเลขคันโยก ยังไม่ต้องขับล้อ แล้วลองโยกไปทิศต่าง ๆ',
              solution=P(setup=ble_setup(NAME) + show_name(), loop=[ble_poll()],
                         extra=[ble_on_received([setvar('v', to_float(ble_data())),
                                                 when(cmp('operator_gte', VAR('v'), N(1000)),
                                                      [setvar('l', op('operator_subtract', mathop('floor', op('operator_divide', VAR('v'), N(1000))), N(100))),
                                                       setvar('r', op('operator_subtract', op('operator_mod', VAR('v'), N(1000)), N(100))),
                                                       oled_clear(), oled_print(VAR('l'), 0, 0, 'No'), oled_print(VAR('r'), 0, 16)])])]),
              vars=['v', 'l', 'r'],
              answer='ดันขึ้นสุด l และ r ใกล้ 60 (หน้าจอยตั้งกำลังสูงสุดไว้ 60%) ดันไปทางขวา l เป็นบวก r เป็นลบ หุ่นจึงหมุนขวา')],
  quiz=[dict(q='มือถือส่ง <code>100100</code> หุ่นทำอะไร', choices=['หยุด เพราะ l = 0 และ r = 0', 'เดินหน้าเต็มแรง', 'ไม่ทำอะไร เพราะเป็นตัวอักษร'], answer=0,
             why='100 − 100 = 0 ทั้งสองล้อ คือคันโยกอยู่ตรงกลาง'),
        dict(q='มือถือส่ง <code>40199</code> ค่า l และ r คือเท่าไร', choices=['l = −60, r = 99', 'l = 40, r = 199', 'l = 60, r = −99'], answer=0,
             why='floor(40199 ÷ 1000) = 40 → 40 − 100 = −60 และ 40199 mod 1000 = 199 → 199 − 100 = 99'),
        dict(q='ทำไมจอยจำกัดกำลังแต่ละล้อไว้ไม่เกิน ±99', choices=['ให้เลขที่ส่ง ≥ 1000 เสมอ หุ่นจึงแยกเลขคันโยกออกจากตัวอักษรได้', 'มอเตอร์รับค่า 100 ไม่ได้', 'Bluetooth ส่งเลขเกิน 6 หลักไม่ได้'], answer=0,
             why='ถ้ายอมให้ซ้าย = −100 จะได้ 0 × 1000 + … ต่ำกว่า 1000 หุ่นจะคิดว่าเป็นตัวอักษร (<code>toFloat("S")</code> ได้ 0)')]))

L.append(dict(id='u6-ble-twostick', unit=6, cat='iot', rc='stick2arm', title='สองคันโยก + ปุ่มแขนขึ้น/ลง (เซอร์โว)',
  goals=['ใช้โค้ดขับล้อจากบท 6.4 กับจอยสองคันโยกได้เลยโดยไม่ต้องแก้', 'เพิ่มปุ่มพิเศษ U / D สั่งเซอร์โวยกแขน'],
  intro='จอยแบบ<b>สองคันโยก</b>: คันซ้ายเดินหน้า-ถอย คันขวาเลี้ยว มือถือรวมสองคันเป็นกำลังล้อซ้าย-ขวาให้ก่อน แล้วส่งเป็นเลขเดียวแบบเดิม โค้ดขับล้อของหุ่นจึง<b>เหมือนบท 6.4 ทุกบรรทัด</b> ที่เพิ่มคือปุ่มพิเศษสองปุ่ม: แขนขึ้นส่ง <code>U</code> แขนลงส่ง <code>D</code> หุ่นหมุนเซอร์โวที่ช่อง RC1 ไป 150° หรือ 60°',
  blocks=['mini_RCset'],
  examples=[
    dict(title='ทดสอบแขนอย่างเดียว', desc='เสียบเซอร์โวที่ RC1 ยังไม่ขับล้อ กดปุ่มแขนขึ้น/ลงในหน้าจอยแล้วดูว่าแขนขยับถูกทาง',
         xml=P(setup=ble_setup(NAME) + show_name() + [servo('RC1', 60)], loop=[ble_poll()], extra=[ble_on_received(ARM)]),
         notes=[('if(ble_rcvData == "U")', 'ปุ่มพิเศษส่งข้อความที่ตั้งไว้ในหน้าสร้างจอย ค่าเริ่มต้นคือ U และ D'),
                ('MiniR4.RC1.setAngle(150);', 'แขนขึ้น ถ้าแขนขยับกลับทาง ให้สลับเลข 150 กับ 60'),
                ('MiniR4.RC1.setAngle(60);', 'แขนลง (ใน Setup ก็สั่ง 60 ไว้ เพื่อเริ่มที่แขนลง)')]),
    dict(title='ขับสองคันโยก + แขน', desc='บล็อกหมวกจากบท 6.4 เพิ่ม if สองอันในส่วน else (ข้อความที่ไม่ใช่เลขคันโยก) ส่วน loop เหมือนเดิม',
         xml=P(setup=ble_setup(NAME) + [drive_setup()] + show_name() + [servo('RC1', 60)], loop=drive_loop(), extra=[stick_hat(ARM)]),
         vars=['last', 'v', 'l', 'r'],
         notes=[('if(v >= 1000)', 'เลขคันโยก → แยกเป็น l, r เหมือนบท 6.4'),
                ('if(ble_rcvData == "D")', 'U, S และ D เป็นตัวอักษร <code>toFloat</code> ได้ 0 จึงมาอยู่ส่วน else'),
                ('MiniR4.RC1.setAngle(150);', 'setAngle สั่งแล้วไปต่อทันที ขับไปด้วยยกแขนไปด้วยได้')]),
  ],
  arduino=['หน้าจอยสองคันโยกส่งเลขชุดเดียวกับคันโยกเดียว ใช้หน้าจอยของบท 6.4 กับหุ่นบทนี้ก็ขับได้เหมือนกัน (แต่ไม่มีปุ่มแขน)',
           'ปุ่มพิเศษตั้งได้ทั้งข้อความตอนกดและตอนปล่อย เช่น กดส่ง <code>G</code> ปล่อยส่ง <code>g</code> ทำมือคีบที่คีบเฉพาะตอนกดค้าง',
           'มีเซอร์โวหลายตัว ใช้ช่อง RC2–RC4 กับข้อความใหม่ เช่น <code>O</code> / <code>C</code> เปิด-ปิดมือคีบ'],
  tries=[dict(task='กดแขนขึ้นแต่ละครั้ง ยกขึ้นทีละ 15° (ไม่เกิน 150) กดแขนลงลดทีละ 15° (ไม่ต่ำกว่า 60) ใช้ตัวแปร <code>arm</code> กับบล็อก constrain',
              solution=P(setup=ble_setup(NAME) + show_name() + [setvar('arm', '60'), servo('RC1', VAR('arm'))], loop=[ble_poll()],
                         extra=[ble_on_received([when(got('U'), [setvar('arm', B('operator_constrain', v={'NUM': op('operator_add', VAR('arm'), N(15)), 'MIN': 60, 'MAX': 150}))]),
                                                 when(got('D'), [setvar('arm', B('operator_constrain', v={'NUM': op('operator_subtract', VAR('arm'), N(15)), 'MIN': 60, 'MAX': 150}))]),
                                                 servo('RC1', VAR('arm'))])]),
              vars=['arm'],
              answer='<code>constrain</code> บีบค่าไว้ในช่วง 60–150 กดเกินก็ไม่หมุนเลยขอบ'),
         dict(task='ในหน้าสร้างจอย เพิ่มปุ่มที่ 3 ส่ง <code>M</code> ให้แขนไปตรงกลาง 105°',
              solution=P(setup=ble_setup(NAME) + [drive_setup()] + show_name() + [servo('RC1', 60)], loop=drive_loop(),
                         extra=[stick_hat(ARM + [when(got('M'), [servo('RC1', 105)])])]),
              vars=['last', 'v', 'l', 'r'])],
  quiz=[dict(q='เปลี่ยนจากจอยบท 6.4 มาเป็นสองคันโยก ต้องแก้ส่วนแยกเลขคันโยกในหุ่นไหม', choices=['ไม่ต้อง มือถือรวมสองคันเป็นเลขเดียวแบบเดิม', 'ต้องแยกรับสองข้อความ', 'ต้องเปลี่ยนเป็นเลข 12 หลัก'], answer=0,
             why='มือถือคำนวณคันซ้าย-ขวาเป็นกำลังล้อก่อนส่ง หุ่นได้ข้อมูลแบบเดิม'),
        dict(q='ทำไม if ของ U และ D อยู่ในส่วน else', choices=['U และ D เป็นตัวอักษร toFloat ได้ 0 ซึ่งน้อยกว่า 1000', 'ถ้าวางไว้ที่อื่นจะคอมไพล์ไม่ผ่าน', 'ให้แขนขยับเร็วขึ้น'], answer=0,
             why='ข้อความที่ไม่ใช่เลขคันโยกตกมาที่ else ทั้งหมด'),
        dict(q='กดปุ่มแขนขึ้นระหว่างกำลังโยกคันโยกขับ หุ่นจะเป็นอย่างไร', choices=['ขับต่อได้ และแขนขยับไปพร้อมกัน', 'หุ่นหยุดรอจนแขนขยับเสร็จ', 'แขนไม่ขยับจนกว่าจะปล่อยคันโยก'], answer=0,
             why='<code>setAngle</code> ไม่รอ loop ยังสั่งล้อตาม l, r ต่อไป')]))

# =====================================================================
# หน่วยที่ 6 — หน้าสร้างจอย (6.6) และ WiFi (6.7–6.9)
# MQTT: broker.hivemq.com พอร์ต 1883 · หน้าจอยส่งที่ mr4/<ชื่อหุ่น>/cmd · หุ่นตอบที่ mr4/<ชื่อหุ่น>/msg
# =====================================================================
WIFI = ('MyWiFi', 'MyPassword')  # ตัวแทนชื่อและรหัส WiFi นักเรียนต้องเปลี่ยนเป็นของจริง
MQ = VIA_MQTT


def topic(end, name=NAME):
    return 'mr4/%s/%s' % (name, end)


def mqtt_setup(name=NAME):
    """Setup ของหุ่น MQTT: ไฟส้มระหว่างต่อ → ต่อ WiFi → ต่อ broker (ID = ชื่อหุ่น) → รับหัวข้อ cmd → ไฟเขียว"""
    return [led(255, 120, 0), wifi_connect(*WIFI), mqtt_connect(name), mqtt_subscribe(topic('cmd', name)), led(0, 255, 0)]


def edit(src, *pairs):
    """ต่อยอดจากไฟล์ตัวอย่าง C++: แทนข้อความทีละคู่ (แต่ละข้อความต้องเจอครั้งเดียวพอดี)"""
    for a, b in pairs:
        assert src.count(a) == 1, ('edit: text must appear exactly once', a)
        src = src.replace(a, b)
    return src


# โค้ด C++ ล้วนของบท 6.9 อยู่ในไฟล์ .ino ไฟล์เดียว (บทเรียนอ่านจากไฟล์นี้) ไม่มีคอมเมนต์ เพราะโค้ดแปลภาษาไม่ได้
# คำอธิบายทั้งหมดอยู่ใน notes / arduino ของบทเรียน (build_data ตรวจว่าโค้ดแบบ codeOnly ไม่มีอักษรไทย/ลาว)
WIFI_SERVER_INO = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'code', 'u6_wifi_server.ino'), encoding='utf-8').read()
BUILDER_SETUP = ble_setup(NAME) + [drive_setup()] + show_name() + [servo('RC1', 60)]
MQTT_DRIVE_SETUP = show_name() + [drive_setup(), servo('RC1', 60)] + mqtt_setup()
LIGHT = [when(got('W'), [led(255, 255, 255, 1), led(255, 255, 255, 2)]), when(got('w'), [led(0, 0, 0, 1), led(0, 0, 0, 2)])]
PAGE_B = r'''  "<p><button onclick=\"go('B')\">▼</button></p>"'''

L.append(dict(id='u6-builder', unit=6, cat='iot', rc='stick2arm', title='ออกแบบจอยของตัวเอง: เพิ่มปุ่ม คัดลอก HTML แล้วเปิดทดสอบ',
  goals=['ปรับจอยในหน้าสร้างจอย: เลือกแบบ เพิ่มปุ่ม แก้ชื่อ หมุนลูกศร ลากย้าย และตั้งข้อความที่ปุ่มส่ง',
         'คัดลอก HTML ไปเป็นไฟล์ของตัวเอง อ่านว่าแต่ละส่วนทำอะไร แก้ค่าเอง แล้วเปิดทดสอบ'],
  intro='บทนี้<b>ไม่มีบล็อกใหม่</b> หุ่นใช้โปรแกรมของบท 6.5 ได้เลย ที่เปลี่ยนคือฝั่งมือถือ กด “เปิดจอยของบทนี้” ได้หน้าสร้างจอย มีที่ตั้งค่า 3 ส่วน: '
        '<b>1. เลือกแบบจอย</b> · <b>2. ตั้งค่า</b> (ชื่อหุ่น การเชื่อมต่อ กำลังล้อ) · <b>3. ปุ่มพิเศษ</b> (เพิ่ม แก้ชื่อ หมุน ลากย้าย) '
        'ตัวอย่างจอยเปลี่ยนตามทันที กด <b>ทดสอบกับหุ่น</b> เพื่อลองขับ พอใจแล้วกด <b>คัดลอก HTML</b> หรือ <b>ดาวน์โหลด .html</b> ได้ไฟล์เดียวพร้อมคอมเมนต์ภาษาไทย',
  blocks=[],
  examples=[
    dict(title='หุ่นตัวเดิมจากบท 6.5', desc='จอยใหม่ยังส่งข้อความชุดเดิม (เลขคันโยก, S, U, D) โปรแกรมหุ่นจึงไม่ต้องแก้ ดูว่าค่าในหน้าสร้างจอยคู่กับบรรทัดไหน',
         xml=P(setup=BUILDER_SETUP, loop=drive_loop(), extra=[stick_hat(ARM)]),
         vars=['last', 'v', 'l', 'r'],
         notes=[('BLE.setLocalName("R4-T01");', '<b>ชื่อหุ่น</b> ในจอยตั้งให้ตรงกับชื่อนี้ ถ้าต่อหุ่นชื่ออื่น จอยจะเตือน'),
                ('if(ble_rcvData == "U")', '<b>ข้อความตอนกด</b> ของปุ่มแขนขึ้นคือ <code>U</code> ต้องตรงกับใน if ทุกตัวอักษร'),
                ('if(v >= 1000)', 'ปุ่มอย่าส่งตัวเลขตั้งแต่ 1000 หุ่นจะคิดว่าเป็นคันโยก'),
                ('l = floor((v / 1000)) - 100;', '<b>กำลังล้อสูงสุด</b> 60 → l, r ไม่เกิน ±60 แก้ในจอยได้โดยไม่ต้องแก้หุ่น')]),
    dict(title='ปุ่มที่ส่งทั้งตอนกดและตอนปล่อย: ไฟส่องทาง', desc='เพิ่มปุ่ม “ไฟ” ข้อความตอนกด <code>W</code> ตอนปล่อย <code>w</code> กดค้างไฟติด ปล่อยแล้วดับ',
         xml=P(setup=BUILDER_SETUP, loop=drive_loop(), extra=[stick_hat(ARM + LIGHT)]),
         vars=['last', 'v', 'l', 'r'],
         notes=[('if(ble_rcvData == "W")', 'ข้อความตอนกด → ไฟสองดวงสีขาว'),
                ('if(ble_rcvData == "w")', '<b>ข้อความตอนปล่อย</b> (w ตัวเล็ก) → ไฟดับ ปิดจอหรือสลับแอประหว่างกดค้าง จอยก็ส่ง w ให้')]),
  ],
  arduinoTitle='แก้ไฟล์จอยที่คัดลอกไป',
  arduino=['เปิดไฟล์ด้วยโปรแกรมแก้ข้อความ เช่น VS Code ไฟล์แบ่งเป็นส่วนและมีคอมเมนต์บอก: <code>&lt;style&gt;</code> สีและขนาด · <code>&lt;main id="pad"&gt;</code> คันโยกและปุ่ม · <code>&lt;script&gt;</code> โปรแกรมของจอย',
           '<b>ตั้งค่า</b> อยู่ต้น <code>&lt;script&gt;</code>: <code>const CONFIG = {</code> มีชื่อหุ่นและ <code>speed: 60</code> เช่น แก้เป็น 80 ดันคันโยกสุดแล้วหุ่นแรงขึ้น',
           '<b>การเชื่อมต่อ</b> คือ <code>const Link = {</code> (Bluetooth หรือ MQTT) ทุกปุ่มส่งข้อความผ่าน <code>function send(text)</code>',
           '<b>ปุ่ม</b>: ปุ่มพิเศษหนึ่งปุ่มคือ <code>&lt;button&gt;</code> หนึ่งบรรทัด แก้ <code>data-press="U"</code> เพื่อส่งข้อความอื่น · <b>คันโยก</b>: <code>holdRepeat(…, 100)</code> ส่งค่าซ้ำทุก 100 มิลลิวินาที',
           'ทดสอบไฟล์ของตัวเอง ① หน้าสร้างจอย ช่อง <b>ทดสอบไฟล์ของฉัน</b> วางโค้ดแล้วกด <b>เปิดไฟล์ที่วาง</b> ② ในคอม ดับเบิลคลิกไฟล์ให้เปิดด้วย Chrome',
           '③ ขึ้น GitHub Pages: อัปโหลดไฟล์ชื่อ <code>index.html</code> ใน repository แล้วเปิด Settings → Pages ได้ลิงก์ https · Bluetooth จากเว็บใช้ได้เฉพาะหน้า https หรือไฟล์ในคอม'],
  tries=[dict(task='เพิ่มปุ่มแตร: กด <b>+ เพิ่มปุ่ม</b> ตั้งชื่อปุ่ม “แตร” ข้อความตอนกด <code>G</code> หมุนลูกศรไป 90° ลากไปที่ว่าง แล้วให้หุ่นบี๊บเมื่อได้ <code>G</code>',
              solution=P(setup=BUILDER_SETUP, loop=drive_loop(), extra=[stick_hat(ARM + [when(got('G'), [B('mini_Buzzer_Tone', v={'FREQ': 880, 'VOL': 200})])])]),
              vars=['last', 'v', 'l', 'r'],
              answer='ปุ่มใหม่ 1 ปุ่ม = if ใหม่ 1 อันในส่วน else ข้อความต้องตรงกันทุกตัวอักษร'),
         dict(task='เปลี่ยน<b>ชนิดปุ่มหลัก</b>เป็น “ปุ่ม 4 ทิศ กดค้าง” ต้องเพิ่มอะไรในหุ่นตัวนี้',
              solution=P(setup=BUILDER_SETUP, loop=drive_loop(), extra=[stick_hat([when(got(k), wheels(a, b)) for k, a, b in HOLD if k != 'S'] + ARM)]),
              vars=['last', 'v', 'l', 'r'],
              answer='F B L R ไม่ใช่เลขคันโยก จึงตกไปส่วน else เพิ่ม if ของ F B L R แบบบท 6.3 หุ่นจึงรับได้ทั้งจอยคันโยกและจอยปุ่ม')],
  quiz=[dict(q='เพิ่มปุ่มพิเศษที่ส่ง <code>G</code> ในหน้าสร้างจอย แต่ยังไม่ได้แก้โปรแกรมหุ่น กดแล้วจะเป็นอย่างไร', choices=['หุ่นได้รับ G แต่ไม่ทำอะไร เพราะไม่มี if ที่เทียบกับ G', 'หุ่นค้าง ต้องกดรีเซ็ต', 'จอยไม่ยอมส่ง G'], answer=0,
             why='ข้อความที่ไม่ตรงกับ if ไหนเลยก็ผ่านไปเฉย ๆ ทุกปุ่มใหม่ต้องมี if คู่กันในหุ่น'),
        dict(q='ในไฟล์ที่คัดลอกไป อยากให้ดันคันโยกสุดแล้วหุ่นแรงขึ้น ต้องแก้ตรงไหน', choices=['speed ใน CONFIG', 'data-press ของปุ่ม', 'name ใน CONFIG'], answer=0,
             why='<code>speed</code> คือกำลังล้อสูงสุดที่คันโยกส่ง ค่าเดียวกับ “กำลังล้อสูงสุด” ในหน้าสร้างจอย'),
        dict(q='ปุ่มที่เว้นช่อง “ข้อความตอนปล่อย” ว่างไว้ ยกนิ้วออกจากปุ่มแล้วจอยส่งอะไร', choices=['ไม่ส่งอะไร', 'ส่ง S', 'ส่งข้อความตอนกดซ้ำอีกครั้ง'], answer=0,
             why='จอยส่งเฉพาะข้อความที่ไม่ว่าง ถ้าอยากให้หุ่นรู้ว่าปล่อยแล้ว ต้องตั้งข้อความตอนปล่อย เช่น <code>w</code>')]))

L.append(dict(id='u6-mqtt-hello', unit=6, cat='iot', rc='mqtt-hello', title='WiFi + MQTT: ส่งข้อความผ่านอินเทอร์เน็ต หุ่นส่งค่าแบตกลับ',
  goals=['ต่อบอร์ดเข้า WiFi 2.4 GHz และ MQTT broker แล้วรับข้อความจากหัวข้อของหุ่นตัวเอง', 'ส่งค่าแบตจากหุ่นกลับไปขึ้นบนมือถือด้วย MQTT Publish'],
  intro='Bluetooth ใช้ได้แค่ในห้อง ผ่าน<b>อินเทอร์เน็ต</b>อยู่ห่างกันแค่ไหนก็ได้ บทนี้ใช้ <b>MQTT</b>: เครื่องกลางชื่อ <b>broker</b> (<code>broker.hivemq.com</code>) ส่งข้อความที่ใคร <b>Publish</b> ไปที่<b>หัวข้อ</b>หนึ่ง ต่อให้ทุกเครื่องที่ <b>Subscribe</b> หัวข้อนั้น '
        'จอยส่งคำสั่งที่ <code>mr4/R4-T01/cmd</code> หุ่นตอบที่ <code>mr4/R4-T01/msg</code> · Setup: ต่อ WiFi → ต่อ MQTT → Subscribe · Loop: <b>MQTT Polling</b>',
  blocks=['mini_wifi_connect', 'mini_mqtt_connect', 'mini_mqtt_subscribe', 'mini_mqtt_loop', 'mini_mqtt_on_message', 'mini_mqtt_received_message', 'mini_mqtt_publish'],
  examples=[
    dict(title='สวัสดี MQTT', desc='ไฟส้มระหว่างต่อ WiFi และ broker ต่อเสร็จเป็นสีเขียว ส่งข้อความจากหน้าจอย ข้อความขึ้นจอ OLED และหุ่นตอบ OK กลับมา',
         xml=P(setup=show_name() + mqtt_setup(), loop=[mqtt_loop()],
               extra=[mqtt_on_message([oled_clear(), oled_print(mqtt_msg(), 0, 8), mqtt_publish(topic('msg'), 'OK')])]),
         notes=[('#include &lt;PubSubClient.h&gt;', 'ไลบรารี MQTT (ต้องติดตั้งเพิ่ม)'),
                ('void mqttCallback(', 'บล็อกหมวก ต้องมาก่อน <code>connectMQTT</code> ที่เรียกใช้ จึงวางเหนือ R4 Begin'),
                ('mqtt_rcvMessage += (char)payload[i];', 'ต่อไบต์ที่ได้เป็น String = บล็อก MQTT Received Message'),
                ('mqttClient.publish("mr4/R4-T01/msg", String("OK").c_str());', 'ส่ง OK ไปหัวข้อ msg ขึ้นในหน้าต่างข้อความของจอย'),
                ('connectWiFi("MyWiFi", "MyPassword");', 'เปลี่ยนเป็นชื่อและรหัส WiFi จริง คำสั่งนี้รอจนต่อติด'),
                ('connectMQTT("broker.hivemq.com", 1883, "R4-T01", "", "");', 'broker พอร์ต 1883 ID <code>R4-T01</code>'),
                ('mqttClient.subscribe("mr4/R4-T01/cmd", 0);', 'รับหัวข้อคำสั่งของหุ่นตัวเอง'),
                ('mqttClient.loop();', 'ต้องวนบ่อย ๆ ข้อความจึงเข้า อย่าใส่ wait นาน')]),
    dict(title='ส่งค่าแบตไปมือถือทุก 2 วินาที', desc='ค่าแบตขึ้นในหน้าต่างข้อความของจอยทุก 2 วินาที จับเวลาด้วย millis แบบบท 6.1 Loop จึงยังวนเร็ว',
         xml=P(setup=show_name() + mqtt_setup() + [setvar('last', '0')],
               loop=[mqtt_loop(), when(since_last(2000), [setvar('last', millis()), mqtt_publish(topic('msg'), B('mini_PWR_getVolt'))])],
               extra=[mqtt_on_message([oled_clear(), oled_print(mqtt_msg(), 0, 8)])]),
         vars=['last'],
         notes=[('MiniR4.OLED.print(mqtt_rcvMessage);', 'บล็อกหมวกต้องมีเสมอ ใส่อะไรง่าย ๆ ไว้ก็ได้'),
                ('if((millis() - last) > 2000)', 'เกิน 2000 ms จากครั้งก่อนหรือยัง'),
                ('mqttClient.publish("mr4/R4-T01/msg", String(MiniR4.PWR.getBattVoltage()).c_str());', 'ส่งค่าแบตเป็นข้อความ เช่น 7.85')]),
  ],
  arduino=['บอร์ดต่อได้เฉพาะ WiFi <b>2.4 GHz</b> ใช้ hotspot มือถือได้ (iPhone เปิด “เพิ่มความเข้ากันได้สูงสุด” · Android เลือกย่าน 2.4 GHz) WiFi โรงเรียนบางแห่งปิดพอร์ต 1883 ต่อไม่ได้ให้ลอง hotspot',
           'ไฟส้มค้าง เปิด Serial Monitor (9600): ค้างที่ <code>WiFi Connection..</code> = ชื่อ/รหัสผิด หรือเป็น 5 GHz · ค้างที่ <code>MQTT Connection..</code> = พอร์ต 1883 ถูกปิด หรือไม่มีเน็ต',
           '<b>broker สาธารณะ</b>: ใครรู้ชื่อหัวข้อก็ส่งเข้าหุ่นเราได้ ทุกทีมจึงใช้ชื่อหุ่นตัวเองในหัวข้อและ ID (ID ซ้ำ broker จะตัดเครื่องที่ต่อก่อนออก) และอย่าส่งข้อมูลส่วนตัว',
           '<b>ข้อควรระวัง 1:</b> มี MQTT Connect แต่ไม่มีบล็อกหมวก When MQTT Message Received → คอมไพล์ไม่ผ่าน <code>\'mqttCallback\' was not declared</code>',
           '<b>ข้อควรระวัง 2:</b> บล็อกหมวก MQTT ต้องอยู่<b>เหนือ</b> R4 Begin (ตรงข้ามกับ Bluetooth) ถ้าอยู่ใต้ก็คอมไพล์ไม่ผ่านด้วยข้อความเดียวกัน',
           'Arduino IDE: ติดตั้งไลบรารี <b>PubSubClient</b> (WiFiS3 มากับบอร์ด) ถ้าต่อ WiFi ไม่ติดทั้งที่ถูกหมด ลองอัปเดตเฟิร์มแวร์ไร้สาย: Tools → <b>Firmware Updater</b>'],
  tries=[dict(task='พิมพ์ <code>bat</code> ในหน้าต่างข้อความ ให้หุ่นตอบค่าแบตทันที ข้อความอื่นขึ้นจอเหมือนเดิม',
              solution=P(setup=show_name() + mqtt_setup(), loop=[mqtt_loop()],
                         extra=[mqtt_on_message([either(got('bat', MQ), [mqtt_publish(topic('msg'), B('mini_PWR_getVolt'))], [oled_clear(), oled_print(mqtt_msg(), 0, 8)])])]),
              answer='Publish ในบล็อกหมวกได้ ข้อความที่ได้รับเก็บไว้ใน <code>mqtt_rcvMessage</code> แล้ว'),
         dict(task='เปลี่ยนตัวอย่างที่ 1 เป็นหุ่นทีม 7 ชื่อ <code>R4-T07</code> ต้องแก้บล็อกกี่ที่ และในหน้าสร้างจอยแก้อะไร',
              solution=P(setup=show_name('R4-T07') + mqtt_setup('R4-T07'), loop=[mqtt_loop()],
                         extra=[mqtt_on_message([oled_clear(), oled_print(mqtt_msg(), 0, 8), mqtt_publish(topic('msg', 'R4-T07'), 'OK')])]),
              answer='4 ที่: ชื่อบนจอ, ID, หัวข้อ Subscribe และ Publish ในหน้าสร้างจอยแก้แค่ชื่อหุ่น จอยสร้างหัวข้อ <code>mr4/R4-T07/…</code> ให้เอง')],
  quiz=[dict(q='หน้าจอยส่งคำสั่งไปที่หัวข้อ <code>mr4/R4-T01/cmd</code> หุ่นต้องมีบล็อกไหนถึงจะได้รับ', choices=['MQTT Subscribe mr4/R4-T01/cmd', 'MQTT Publish mr4/R4-T01/cmd', 'MQTT Connect ที่ใส่ ID เป็น mr4/R4-T01/cmd'], answer=0,
             why='Subscribe = สมัครรับ broker จะส่งข้อความของหัวข้อนั้นมาให้ ส่วน Publish คือส่งออก'),
        dict(q='วางบล็อกหมวก When MQTT Message Received ไว้ใต้ R4 Begin แบบเดียวกับ Bluetooth จะเกิดอะไร', choices=["คอมไพล์ไม่ผ่าน 'mqttCallback' was not declared", 'ทำงานได้ปกติ', 'อัปโหลดได้ แต่ต่อ WiFi ไม่ติด'], answer=0,
             why='ตัวสร้างโค้ดเรียงจากบนลงล่าง ฟังก์ชัน <code>mqttCallback</code> ต้องมาก่อน <code>connectMQTT</code>'),
        dict(q='อัปโหลดแล้วไฟส้มค้าง ไม่เป็นสีเขียวสักที ข้อใดเป็นสาเหตุได้', choices=['WiFi เป็น 5 GHz รหัสผิด หรือเครือข่ายปิดพอร์ต 1883', 'ลืมวางบล็อกหมวก', 'ลืมใส่ MQTT Polling ใน Loop'], answer=0,
             why='ไฟเขียวติดหลังต่อ WiFi และ broker สำเร็จ ลืมบล็อกหมวกจะคอมไพล์ไม่ผ่านตั้งแต่แรก ส่วนลืม Polling ไฟยังเขียวแต่ไม่ได้รับข้อความ')]))

L.append(dict(id='u6-mqtt-drive', unit=6, cat='iot', rc='mqtt-drive', title='บังคับผ่าน MQTT ด้วยจอยเดิม และเทียบความหน่วงกับ Bluetooth',
  goals=['ย้ายโปรแกรมขับจากบท 6.5 มาใช้ MQTT โดยเปลี่ยนแค่บล็อกที่ใช้เชื่อมต่อ', 'ตั้งระบบกันหลุดเป็น 1000 ms ให้เหมาะกับเน็ต แล้วเทียบความหน่วงกับ Bluetooth'],
  intro='จอยของบทนี้คือสองคันโยก + แขนของบท 6.5 ที่เลือก<b>การเชื่อมต่อ</b>เป็น <b>อินเทอร์เน็ต (MQTT)</b> ข้อความเหมือนเดิม หุ่นจึงใช้ตรรกะเดิม เปลี่ยนแค่: BLE Polling → <b>MQTT Polling</b> · BLE Connected? → <b>MQTT Connected?</b> · '
        'หมวก Bluetooth → <b>When MQTT Message Received</b> · Received Data → <b>MQTT Received Message</b> · ระบบกันหลุด 500 → <b>1000 ms</b> เพราะผ่านเน็ตข้อความมาช้าบ้างเร็วบ้าง',
  blocks=['mini_mqtt_is_connected'],
  examples=[
    dict(title='ทดลองระบบกันหลุดผ่านเน็ตด้วยไฟ', desc='ยังไม่ขับล้อ: จับคันโยกค้างไว้ไฟเขียว ปล่อยแล้วผ่านไป 1 วินาทีไฟแดง ลองปิด hotspot ระหว่างจับคันโยก ไฟต้องแดงเอง',
         xml=P(setup=show_name() + mqtt_setup() + [setvar('last', '0')],
               loop=[mqtt_loop(), either(lost(via=MQ), [led(255, 0, 0)], [led(0, 255, 0)])],
               extra=[mqtt_on_message([setvar('last', millis())])]),
         vars=['last'],
         notes=[('last = millis();', 'ทุกข้อความที่เข้ามา จำเวลาไว้ใน <code>last</code> เหมือนบท 6.3'),
                ('if((!mqttClient.connected())||((millis() - last) > 1000))', 'MQTT หลุด หรือเงียบเกิน 1000 ms (จับคันโยกอยู่ จอยส่งทุก 100 ms) → ถือว่าสัญญาณหาย')]),
    dict(title='สองคันโยก + แขน ผ่านเน็ต', desc='บล็อกในหมวกและใน Loop เรียงเหมือนบท 6.5 ทุกอัน เปลี่ยนแค่บล็อกเชื่อมต่อเป็นของ MQTT และ 500 เป็น 1000',
         xml=P(setup=MQTT_DRIVE_SETUP, loop=drive_loop(via=MQ), extra=[stick_hat(arm(MQ), via=MQ)]),
         vars=['last', 'v', 'l', 'r'],
         notes=[('v = mqtt_rcvMessage.toFloat();', 'แยกเลขคันโยกแบบเดิม อ่านจาก <code>mqtt_rcvMessage</code> แทน <code>ble_rcvData</code>'),
                ('if(mqtt_rcvMessage == "U")', 'ปุ่มแขนแบบเดิม'),
                ('mqttClient.loop();', 'แทน <code>BLE.poll()</code>'),
                ('if((!mqttClient.connected())||((millis() - last) > 1000))', 'แทน <code>!BLE.connected()</code> และ 500'),
                ('MiniR4.DriveDC.Move(l, r);', 'สั่งล้อแบบเดิม')]),
  ],
  arduino=['หน้าจอยต่อ broker ตัวเดียวกันทาง <code>wss://broker.hivemq.com:8884/mqtt</code> (เบราว์เซอร์ใช้ WebSocket พอร์ต 8884) ส่วนหุ่นใช้พอร์ต 1883 ข้อความจึงถึงกัน',
           'ทำไม 1000 ms: ข้อความวิ่ง มือถือ → broker → หุ่น ผ่านเน็ตที่ใช้ร่วมกับคนอื่น จึงมาไม่สม่ำเสมอ ตั้ง 500 หุ่นอาจหยุดกระตุกทั้งที่ยังจับคันโยกอยู่ แลกกับเมื่อสัญญาณหายจริง หุ่นวิ่งต่อได้ถึง 1 วินาที',
           'ปล่อยคันโยกแล้วหุ่นหยุดช้ากว่าแบบ Bluetooth ตั้งกำลังล้อไม่ให้แรงเกิน ขับช้า ๆ ในที่โล่ง และเผื่อระยะเบรก',
           'เน็ตหายแบบเงียบ ๆ (เช่น WiFi อ่อน) <code>mqttClient.connected()</code> อาจรู้ตัวช้าหลายวินาที การจับเวลาเงียบ 1000 ms จึงยังจำเป็น',
           'โปรแกรมนี้ต่อ broker ครั้งเดียวใน Setup ถ้าหลุด หุ่นจะหยุดรอ กดรีเซ็ตบอร์ดเพื่อต่อใหม่ หรือทำลองทำข้อ 2 ให้หุ่นต่อใหม่เอง'],
  tries=[dict(task='เทียบความหน่วงกับ Bluetooth: ล้อหมุนไฟสีฟ้า หยุดแล้วไฟดับ ยกหุ่นให้ล้อลอย ดันคันโยกแล้วปล่อย ดูว่าไฟดับช้าแค่ไหน แล้วลองแบบเดียวกันกับโปรแกรม Bluetooth บท 6.5 แบบไหนหยุดช้ากว่า',
              solution=P(setup=MQTT_DRIVE_SETUP, loop=drive_loop(on_stop=[led(0, 0, 0)], on_move=[led(0, 0, 255)], via=MQ), extra=[stick_hat(arm(MQ), via=MQ)]),
              vars=['last', 'v', 'l', 'r'],
              answer='MQTT มักหยุดช้ากว่าจนเห็นได้ เพราะ S ต้องผ่าน broker ก่อนถึงหุ่น ช้าแค่ไหนขึ้นกับเน็ตตอนนั้น'),
         dict(task='ต่อใหม่เองเมื่อหลุด: ท้าย Loop ถ้า MQTT ไม่ได้ต่ออยู่ ให้หยุดล้อ ไฟส้ม แล้ว MQTT Connect และ Subscribe ใหม่ เสร็จแล้วไฟเขียว',
              solution=P(setup=MQTT_DRIVE_SETUP,
                         loop=drive_loop(via=MQ) + [when(B('operator_not', v={'OPERAND': mqtt_connected()}),
                                                         [stop_moving(), led(255, 120, 0), mqtt_connect(NAME), mqtt_subscribe(topic('cmd')), led(0, 255, 0)])],
                         extra=[stick_hat(arm(MQ), via=MQ)]),
              vars=['last', 'v', 'l', 'r'],
              answer='ต่อใหม่ต้อง Subscribe ใหม่ด้วย (broker ลืมหัวข้อเมื่อหลุด) และหยุดล้อก่อน เพราะ MQTT Connect รอจนต่อติด ระหว่างนั้น Loop ไม่วน')],
  quiz=[dict(q='ทำไมระบบกันหลุดแบบ MQTT ใช้ 1000 ms แต่ Bluetooth ใช้ 500 ms', choices=['ข้อความผ่านเน็ตมาช้าและไม่สม่ำเสมอ ถ้าตั้งสั้นไปหุ่นจะหยุดกระตุกทั้งที่ยังจับคันโยกอยู่', 'MQTT ส่งข้อความได้วินาทีละครั้ง', 'บอร์ดนับเวลาช้าลงเมื่อใช้ WiFi'], answer=0,
             why='จอยยังส่งทุก 100 ms เหมือนเดิม แต่ระหว่างทางผ่าน broker บางข้อความมาถึงห่างกันนาน'),
        dict(q='ย้ายโปรแกรมบท 6.5 มาใช้ MQTT ส่วนแยกเลขคันโยกต้องแก้ไหม', choices=['ไม่ต้อง แค่อ่านจาก MQTT Received Message แทน', 'ต้องแก้สูตร เพราะ MQTT ส่งเลขเป็นไบต์', 'ต้องแยกรับสองหัวข้อ ล้อซ้ายกับล้อขวา'], answer=0,
             why='จอยส่งข้อความชุดเดิมไม่ว่าจะต่อแบบไหน'),
        dict(q='หุ่นกำลังวิ่งอยู่แล้ว hotspot ดับ หุ่นจะหยุดเพราะอะไร', choices=['ไม่มีข้อความเข้ามาเกิน 1000 ms ระบบกันหลุดจึงตั้ง l และ r เป็น 0', 'mqttClient.loop() สั่งหยุดล้อให้เอง', 'บอร์ดรีเซ็ตตัวเองเมื่อ WiFi หาย'], answer=0,
             why='Moving at … ไม่หยุดเอง ต้องมีระบบกันหลุดเสมอ')]))

L.append(dict(id='u6-wifi-server', unit=6, cat='iot', title='(เสริม C++) หุ่นปล่อย WiFi เอง + หน้าเว็บปุ่ม 5 ปุ่ม',
  goals=['ให้หุ่นสร้าง WiFi ของตัวเอง (โหมด AP) และเป็นเว็บเซิร์ฟเวอร์ ไม่ต้องมีอินเทอร์เน็ต', 'อ่านบรรทัดคำขอ เช่น GET /F แล้วสั่งหุ่นเดิน 0.5 วินาที'],
  intro='บทเสริม <b>C++ ล้วน</b> (มีบล็อกสร้าง WiFi แต่ไม่มีบล็อกเว็บเซิร์ฟเวอร์) หุ่นปล่อย WiFi <code>R4-T01</code> รหัส <code>12345678</code> มือถือต่อแล้วเปิด <code>192.168.4.1</code> ได้หน้าเว็บปุ่ม ▲ ◀ ■ ▶ ▼ '
        'กดแล้วหน้าเว็บ <code>fetch</code> ที่อยู่ เช่น <code>/F</code> หุ่นอ่านบรรทัดแรก <code>GET /F HTTP/1.1</code> แล้วเดิน 0.5 วินาที ไม่ต้องมีเน็ต ใช้ได้ทุกเบราว์เซอร์ รวมถึง Safari ใน iPhone',
  blocks=['mini_wifi_config', 'mini_wifi_create_ap', 'mini_wifi_localip'],
  examples=[
    dict(title='หุ่นเป็นเว็บเซิร์ฟเวอร์ (ทั้งไฟล์)', codeOnly=True, code=WIFI_SERVER_INO,
         desc='โค้ด C++ ล้วน คัดลอกไปวางใน Arduino IDE ได้ทั้งไฟล์ ไม่ต้องติดตั้งไลบรารีเพิ่ม (WiFiS3 มากับบอร์ด) เปลี่ยนชื่อ WiFi ให้ไม่ซ้ำกับทีมอื่นก่อนอัปโหลด',
         notes=[('const char* NAME = "R4-T01";', 'ชื่อ WiFi ของหุ่น ห้ามซ้ำกับทีมอื่น · <code>PASS</code> รหัสผ่านอย่างน้อย 8 ตัว'),
                ('WiFiServer server(80);', 'เว็บเซิร์ฟเวอร์ พอร์ต 80 = พอร์ตปกติของ http'),
                ("fetch('/'+c)", 'หน้าเว็บในตัวแปร <code>PAGE</code>: กด ▲ → <code>go(\'F\')</code> → ขอ <code>/F</code> จากหุ่น'),
                ('WiFi.config(IPAddress(192, 168, 4, 1));', 'ที่อยู่ของหุ่น = บล็อก WiFi Config IP'),
                ('if (WiFi.beginAP(NAME, PASS) != WL_AP_LISTENING) {', 'เปิด WiFi ของหุ่น (บล็อก WiFi Create AP ก็ใช้คำสั่งนี้) ไม่สำเร็จจอขึ้น AP fail'),
                ('MiniR4.OLED.print(WiFi.localIP());', 'ที่อยู่ขึ้นจอ = บล็อก WiFi Device Local IP'),
                ("String line = client.readStringUntil('\\n');", 'มีคำขอเข้ามา อ่านบรรทัดแรก'),
                ("while (client.connected() &amp;&amp; client.readStringUntil('\\n').length() > 1) {}", 'อ่านบรรทัดที่เหลือทิ้ง จนถึงบรรทัดว่าง'),
                ("String path = line.substring(a, line.indexOf(' ', a));", 'ตัดคำที่สอง: <code>a</code> = 4 ตัดถึงช่องว่างถัดไป ได้ <code>"/F"</code>'),
                ('client.stop();', 'ตอบ (หน้าเว็บ หรือ OK) แล้วปิดก่อน ค่อยเดิน หน้าเว็บจึงไม่ต้องรอ'),
                ('if (path == "/S") MiniR4.DriveDC.brake(true);', '■ สั่งเบรก ถ้ากดระหว่างที่หุ่นกำลังเดิน จะเบรกหลังเดินครบ 0.5 วินาที เพราะ MoveSyncTime รอจนเดินเสร็จ')]),
  ],
  arduino=['ต่อ WiFi <code>R4-T01</code> แล้วพิมพ์ <code>192.168.4.1</code> (http ไม่ใช่ https) มือถือบางเครื่องเตือนว่า WiFi นี้ไม่มีอินเทอร์เน็ต ให้เลือกใช้ต่อ ถ้าหน้าเว็บไม่ขึ้น ลองปิดข้อมูลมือถือชั่วคราว',
           'ถ้าจอขึ้น <code>AP fail</code> ลองเปลี่ยนชื่อหรือรหัส (อย่างน้อย 8 ตัว) หรืออัปเดตเฟิร์มแวร์ไร้สาย: Tools → <b>Firmware Updater</b>',
           'ระหว่างที่มือถือต่อ WiFi ของหุ่น มือถือจะไม่มีเน็ตผ่าน WiFi เลิกเล่นแล้วกลับไปต่อ WiFi เดิม',
           '<code>MoveSyncTime</code> รอจนเดินเสร็จเหมือนบท 6.2 ระหว่างนั้นหุ่นไม่รับคำขอใหม่ จึงตอบและ <code>client.stop()</code> ก่อน แล้วค่อยเดิน',
           'เทียบสามแบบ: <b>Bluetooth</b> ไม่ต้องมีเน็ต แต่ต้องใช้ Chrome/Bluefy · <b>MQTT</b> ไกลแค่ไหนก็ได้ แต่ต้องมีเน็ตและหน่วงกว่า · <b>เว็บเซิร์ฟเวอร์ในหุ่น</b> ไม่ต้องมีเน็ต ทุกเบราว์เซอร์ แต่ต้องอยู่ในระยะ WiFi ของหุ่น'],
  tries=[dict(task='เพิ่มปุ่มแตร ♪ ในหน้าเว็บที่เรียก <code>go(\'H\')</code> แล้วให้หุ่นบี๊บ 0.2 วินาทีเมื่อได้ <code>/H</code>', codeOnly=True,
              code=edit(WIFI_SERVER_INO,
                        (PAGE_B, PAGE_B + '\n' + r'''  "<p><button onclick=\"go('H')\">♪</button></p>"'''),
                        ('  if (path == "/S") MiniR4.DriveDC.brake(true);\n', '  if (path == "/S") MiniR4.DriveDC.brake(true);\n  if (path == "/H") MiniR4.Buzzer.Tone(880, 200);\n')),
              answer='แก้สองที่คู่กัน: ปุ่มขออะไร หุ่นต้องมี if รอสิ่งนั้น เหมือนปุ่มพิเศษในหน้าสร้างจอย'),
         dict(task='เพิ่มปุ่ม <code>V</code> ที่ขอ <code>/V</code> ให้หุ่นตอบเป็นค่าแบต และให้หน้าเว็บแสดงคำตอบของหุ่นใต้ปุ่ม', codeOnly=True,
              code=edit(WIFI_SERVER_INO,
                        (PAGE_B, PAGE_B + '\n' + r'''  "<p><button onclick=\"go('V')\">V</button></p><p id='o'></p>"'''),
                        ("<script>function go(c){fetch('/'+c)}</script>",
                         "<script>function go(c){fetch('/'+c).then(r=>r.text()).then(t=>{document.getElementById('o').textContent=t})}</script>"),
                        (r'''  client.print(path == "/" ? "text/html; charset=utf-8\r\n\r\n" : "text/plain\r\n\r\nOK");
  if (path == "/") client.print(PAGE);''',
                         r'''  client.print(path == "/" ? "text/html; charset=utf-8\r\n\r\n" : "text/plain\r\n\r\n");
  if (path == "/") client.print(PAGE);
  else if (path == "/V") client.print(MiniR4.PWR.getBattVoltage());
  else client.print("OK");''')),
              answer='หน้าเว็บอ่านคำตอบด้วย <code>r.text()</code> แล้วเขียนลงใน <code>&lt;p id=\'o\'&gt;</code> ปุ่มอื่นขึ้น OK ให้รู้ว่าหุ่นได้รับแล้ว')],
  quiz=[dict(q='กดปุ่ม ◀ ในหน้าเว็บ บรรทัดแรกที่หุ่นอ่านได้คืออะไร', choices=['GET /L HTTP/1.1', 'GET /F HTTP/1.1', 'L'], answer=0,
             why='ปุ่ม ◀ เรียก <code>go(\'L\')</code> → <code>fetch(\'/L\')</code> เบราว์เซอร์ส่งคำขอแบบ GET ไปที่ /L'),
        dict(q='ทำไมหุ่นตอบกลับและ client.stop() ก่อนสั่ง MoveSyncTime', choices=['MoveSyncTime รอ 0.5 วินาที ถ้าตอบทีหลัง หน้าเว็บจะรอนาน', 'ถ้าเดินก่อนจะคอมไพล์ไม่ผ่าน', 'client.stop() ทำให้หุ่นเดินเร็วขึ้น'], answer=0,
             why='ตอบให้เสร็จก่อน มือถือก็รู้ทันทีว่าหุ่นได้รับแล้ว'),
        dict(q='ใช้หน้าเว็บของบทนี้ ต้องมีอินเทอร์เน็ตไหม', choices=['ไม่ต้อง มือถือต่อ WiFi ของหุ่นโดยตรง', 'ต้องมี เพราะข้อความผ่าน broker', 'ต้องมี เพราะหน้าเว็บโหลดจาก GitHub'], answer=0,
             why='หุ่นเป็นทั้ง WiFi และเว็บเซิร์ฟเวอร์ หน้าเว็บอยู่ในโค้ดหุ่นเอง (<code>PAGE</code>)')]))

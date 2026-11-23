# English text for the lessons (code snippets stay in lessons_src.py, only words are here)
UNITS = {
  1: dict(title='R4 Core · Movement · Looks', sub='Board, motors, driving, light, sound, screen'),
  2: dict(title='Sensing', sub='IMU · Grayscale · Potentiometer · Color V3 · Laser V2'),
  3: dict(title='Control', sub='Wait · If · Repeat · Timing'),
  4: dict(title='Operators · Variables', sub='Math · Compare · Variables · Text'),
  5: dict(title='My Blocks', sub='Make your own block = a function'),
  6: dict(title='Phone Remote Control', sub='Bluetooth · WiFi · MQTT'),
}

L = {}
L['u1-begin'] = dict(
  title='Program frame: R4 Begin = setup + loop',
  goals=['Know which part of the code the R4 Begin block becomes', 'Decide which commands belong in Setup and which in Loop'],
  intro='Every MATRIXblock program starts with the <b>R4 Begin</b> block. Look at the code panel on the right of the app: this one block builds the whole frame of an Arduino program for you.',
  examples=[
    dict(title='An empty program', desc='No other blocks yet, but the code frame is already complete. Point at a block or a line of code to see which parts belong together.',
         notes=['Brings in the board library so you can use the word <code>MiniR4</code>. When you write code yourself in the Arduino IDE this line must always be there.',
                'Runs once when the board is switched on or reset.',
                'Prepares the whole board (motors, screen, lights, buttons). It must come before any other command.',
                'Tells the board you are using two 18650 batteries.',
                'Opens the channel for sending messages to the computer (UART: On).',
                'Runs again and again for as long as the board is on.']),
    dict(title='Setup vs Loop', desc='The green light turns on once at the start, while the beep repeats every second.',
         notes=['Blocks in Setup are added at the end of <code>setup()</code>, after the board preparation commands.',
                'Blocks in Loop go inside <code>loop()</code> and repeat forever.']),
  ],
  arduino=['Every C++ statement ends with a <code>;</code>', 'Curly braces <code>{ }</code> show which commands belong to which part, like the slots of a block.',
           '<code>MiniR4.LED.setColor(…)</code> reads as “board MiniR4 → its LED part → the setColor command”. The dot means “go into this part”.'],
  tries=[dict(task='Set UART to <b>Off</b> and see which line disappears from the code.', answer='<code>Serial.begin(9600);</code> disappears because Serial is not opened.'),
         dict(task='Switch to three 18650 batteries (18650x3). What changes in the code?', answer='<code>MiniR4.PWR.setBattCell(3);</code>')],
  quiz=[dict(q='You want a light to turn on once when the board starts. Where should the block go?', choices=['In the Setup slot', 'In the Loop slot', 'Outside R4 Begin'],
             why='Setup runs once. Blocks placed outside R4 Begin are not turned into code at all.'),
        dict(q='Which line must always be there when you write code yourself in the Arduino IDE to use MiniR4 commands?', choices=['#include "MatrixMiniR4.h"', 'Serial.begin(9600);', 'delay(1000);'],
             why='Without the include, the compiler does not know what MiniR4 is.'),
        dict(q='How many R4 Begin blocks can one program have?', choices=['1', '2 (Setup and Loop)', 'As many as you like'],
             why='The app warns that only one is allowed. Two will make the program behave strangely.')])

L['u1-led'] = dict(
  title='RGB LED and blinking',
  goals=['Mix colours with R G B values', 'Make a light blink with wait and read it as delay() in the code'],
  intro='The Mini R4 has two RGB lights (LED1, LED2). Each one mixes <b style="color:#d33">red</b>, <b style="color:#2a2">green</b> and <b style="color:#36c">blue</b> light from 0 to 255. This lesson also uses the <b>wait</b> block from the Control category (covered in detail in Unit 3).',
  examples=[
    dict(title='Blinking red', desc='On for 0.5 s, off for 0.5 s, again and again.',
         notes=['The numbers follow the block: light 1, R=255, G=0, B=0', 'All colours 0 = off', 'Wait 500 ms = half a second']),
    dict(title='Two-light traffic signal', desc='LED1 green and LED2 red, then they swap every 2 seconds.', notes=[]),
  ],
  arduino=['The first number in <code>setColor</code> is the light (1 or 2), not the brightness.', 'Once you are used to it, changing a number in the code is faster than dragging a new block.'],
  tries=[dict(task='Make a purple light (red mixed with blue) that blinks faster, every 0.2 seconds.', answer='Purple is R=255 G=0 B=255, with delay(200).'),
         dict(task='Change colour red → green → blue, one second each.', answer='')],
  quiz=[dict(q='What does MiniR4.LED.setColor(2, 0, 0, 255); do?', choices=['LED2 turns blue', 'LED1 becomes twice as bright', 'LED2 turns red'], why='2 is the second light, then R=0 G=0 B=255.'),
        dict(q='If you remove every wait from the blinking example, what do you see?', choices=['The light looks dimly on all the time because it switches very fast', 'The light blinks more slowly', 'It does not compile'], why='The board switches on and off faster than your eyes can follow.')])

L['u1-buzzer'] = dict(
  title='Sound: buzzer frequency and notes',
  goals=['Play a sound by frequency and by note name', 'Understand that sound commands do not wait, so you need wait'],
  intro='The buzzer on the board can play a frequency (Hz) or a musical note. Sound commands <b>do not wait</b>: the program moves on immediately.',
  examples=[
    dict(title='Do Re Mi', desc='Each note plays for 300 ms, and the program waits for it to finish before the next one.',
         notes=['<code>NOTE_C4</code> is a name for the number 262 Hz. The second value is the time in ms.',
                'Wait for the sound to end (300) plus a small gap. Without waiting, the notes overlap and you only hear the last one.']),
    dict(title='Siren', desc='High and low sounds take turns.', notes=[]),
  ],
  arduino=['<code>MiniR4.Buzzer.Tone(frequency, time)</code> uses Arduino’s <code>tone()</code> inside.', 'Double the frequency = the same note one octave higher (C4 262 Hz, C5 523 Hz).'],
  tries=[dict(task='Play C4 D4 E4 F4 G4 going up, 200 ms each, once when the board starts.', answer=''),
         dict(task='Make a beep-beep alarm twice, then 1 second of silence, again and again.', answer='')],
  quiz=[dict(q='Three Tone commands in a row with no delay. What do you hear?', choices=['Almost only the last note', 'All three notes', 'No sound'], why='The command does not wait, so each new note replaces the old one immediately.'),
        dict(q='What is NOTE_C4 in the code?', choices=['A name for the frequency number of the note C', 'A sound file name', 'Port C4'], why='It is a constant already defined in the library.')])

L['u1-oled'] = dict(
  title='OLED screen: showing text and numbers',
  goals=['Print text on the screen at position x, y', 'Understand that one block becomes 3 lines of code, and use Update to avoid flicker'],
  intro='The OLED screen on the board is 128 × 32 pixels. Point (0, 0) is the top-left corner; x grows to the right and y grows downwards.',
  examples=[
    dict(title='Hello MATRIX', desc='Set the text size once in Setup, then print 2 lines.',
         notes=['Move the writing position to x=0, y=0', 'Draws the text into the screen’s memory; it is not shown yet', 'Sends the whole picture to the screen. This line only appears when Update is Yes.']),
    dict(title='Counting on the screen', desc='Uses a variable <code>count</code> (covered in Unit 4). The screen is cleared before every print so numbers do not overlap.',
         notes=['Clears the old picture. Without it, 10 is drawn on top of 9 and becomes unreadable.', 'Variables from blocks are float, so the screen shows 0.00, 1.00 …']),
  ],
  arduino=['<code>print</code> shows 2 decimal places for a float. For whole numbers write <code>MiniR4.OLED.print((int)count);</code> in the Arduino IDE.',
           'Text size 1 is 8 pixels tall, size 2 is 16, size 3 is 24.'],
  tries=[dict(task='Show your nickname in size 2 at the top-left, and a number underneath in size 1.', answer=''),
         dict(task='Make “GO!” blink on the screen (0.5 s on, 0.5 s off).', answer='Clearing the screen also needs display() to show. In blocks you can do that by printing empty text with Update: Yes.')],
  quiz=[dict(q='You print 3 lines in a row. How should you set Update so the screen does not flicker?', choices=['No for the first two, Yes for the last one', 'Yes on every line', 'No on every line'], why='One display() at the end shows everything at once.'),
        dict(q='The screen is 32 pixels tall. How many lines of size-1 text fit?', choices=['4 lines', '2 lines', '8 lines'], why='Size 1 is 8 pixels tall: 32 ÷ 8 = 4.')])

L['u1-button'] = dict(
  title='Board buttons and battery voltage',
  goals=['Read the Up/Down buttons as true/false', 'Read the battery voltage and show it on the screen'],
  intro='Hexagon blocks give a <b>true/false</b> value. Round blocks give a <b>number</b>. Neither can be used on its own: they must be plugged into a slot of another block.',
  examples=[
    dict(title='Press the button, light turns on', desc='Uses if/else from Control. Hold Up for a green light, release to turn it off.',
         notes=['<code>getState()</code> is true while the button is pressed', 'Not pressed']),
    dict(title='Show the battery voltage', desc='Read it every second and print it on the screen.',
         notes=['The value block is plugged into the text slot, so the code puts the reading command inside the brackets of print']),
  ],
  arduino=['Value blocks (round/hexagon) become <b>expressions</b> with no <code>;</code> and always sit inside the brackets of another command.'],
  tries=[dict(task='Press Up for a red light, press Down for a blue light, no button = off.', answer=''),
         dict(task='If the voltage is below 7.0V, show a red warning light (use the &lt; block from Operators).', answer='')],
  quiz=[dict(q='What kind of value does MiniR4.BTN_DOWN.getState() give?', choices=['true or false', 'A number 0–1023', 'Text'], why='Hexagon block = a true/false value.'),
        dict(q='Why does getBattVoltage() have no ; in the example?', choices=['It is inside the brackets of print, a value handed to another command', 'Someone forgot it', 'Reading commands never need ;'], why='An expression inside brackets is not a statement on its own.')])

L['u1-gpio'] = dict(
  title='Mini GPIO: digital D ports and analog A ports',
  goals=['Read/write the Left/Right digital pins of ports D1–D4', 'Read analog values 0–1023 from ports A1–A3'],
  intro='Each D and A port has 4 pins: <b>Left</b>, <b>Right</b>, VCC and GND. There are 2 signal pins, so the block asks you to choose Left or Right.',
  examples=[
    dict(title='External switch on D1 controls the light', desc='Read the Left pin of D1. If it is HIGH, show green.',
         notes=['L = Left pin. Choosing Right gives <code>getR()</code>']),
    dict(title='Show analog A1 on the screen', desc='Turn the sensor or knob plugged into A1 and watch the number change.',
         notes=['AIL = Analog Input, Left pin, gives 0–1023']),
  ],
  arduino=['Port names are members of MiniR4, for example <code>MiniR4.D3.setR(LOW);</code>', 'HIGH is 1 and LOW is 0.'],
  tries=[dict(task='Connect an external LED to the Right pin of D2 and make it blink every 0.5 seconds.', answer='')],
  quiz=[dict(q='Where does MiniR4.A2.getAIR() read from?', choices=['Port A2, Right pin', 'Port A2, Left pin', 'The Right button'], why='AIR = Analog Input Right.'),
        dict(q='What is the range of an analog value?', choices=['0–1023', '0–255', '0–1'], why='The converter is 10-bit.')])

L['u1-motor'] = dict(
  title='One DC motor: Power, Speed, brake, encoder',
  goals=['Tell Power (direct power) apart from Speed (speed held by the encoder)', 'Count how many degrees a wheel turned with the encoder'],
  intro='The R4 Core category controls one motor at a time (M1–M4). It suits arms, conveyors and motor tests. Driving a two-wheeled robot uses the Movement category in the next lessons.',
  examples=[
    dict(title='Spin for 2 s, then brake', desc='Give M1 60% power.',
         notes=['The motor keeps spinning and the program moves on immediately', 'Let it spin for 2 seconds', 'true = Brake, false = Coast']),
    dict(title='Exactly one turn', desc='Reset the counter, then spin until the degrees reach 360 and brake.',
         notes=['Start counting from 0', 'wait until becomes “keep waiting while it has not reached 360”', 'Speed uses the encoder to keep the speed steady']),
  ],
  arduino=['<code>setPower</code> = raw power, slower when the battery is low / <code>setSpeed</code> = the board measures the real speed and keeps it steady.',
           'MATRIX TT motors use PPR 545 and RPM 200, which are already the defaults.'],
  tries=[dict(task='Make M2 spin forward for 1 second, stop 0.5 s, then spin backward for 1 second.', answer=''),
         dict(task='Show M1’s degrees on the screen all the time, then turn the wheel by hand.', answer='')],
  quiz=[dict(q='The battery gets weaker. Which command keeps the speed close to the same?', choices=['setSpeed()', 'setPower()', 'Both are the same'], why='setSpeed reads the encoder and compensates.'),
        dict(q='getDegrees() returns 720. What does it mean?', choices=['The wheel turned 2 times', 'The wheel turned 720 times', 'The speed is 720 rpm'], why='360 degrees = 1 turn.')])

L['u1-servo'] = dict(
  title='RC servo: set an angle 0–180°',
  goals=['Move a servo to the angle you want', 'Know that you must wait for the servo to finish moving'],
  intro='Servos are used for grippers, gates and turning heads. Plug them into RC1–RC4 and command an angle from 0 to 180 degrees.',
  examples=[
    dict(title='Sweep left and right', desc='Move to 30° and 150° in turn.',
         notes=['The program moves on immediately, the servo has not finished turning', 'Wait until it arrives before giving the next angle']),
    dict(title='Turn slowly, 10° at a time', desc='Use repeat and a variable <code>angle</code> to make the movement smooth.', notes=[]),
  ],
  arduino=['If the arm moves the wrong way, use the Enable Reverse On block → <code>setHWDir(false)</code> in Setup.'],
  tries=[dict(task='Make a gripper: open 150°, wait 1 s, close 60°, wait 1 s.', answer='')],
  quiz=[dict(q='setAngle(0) then setAngle(180) straight away. What happens?', choices=['The servo hardly moves towards 0, because the 180 command replaces it immediately', 'It goes to 0 and then to 180 fully', 'It does not compile'], why='setAngle does not wait; put a delay between them.')])

L['u1-move'] = dict(
  title='Movement 1: wheel setup and driving a set distance',
  goals=['Set up Set Movement correctly before using Movement blocks', 'Drive by wheel degrees or by time, and choose Brake/Coast'],
  intro='The Movement category drives both wheels together (the code starts with <code>MiniR4.DriveDC</code>). First you must tell the board which motors the left and right wheels are on.',
  examples=[
    dict(title='Forward 2 wheel turns, then back', desc='Always put Set Movement in Setup.',
         notes=['Comes from Brake Settle: Yes. It must be <b>before</b> #include to work.',
                'Left wheel M1, right wheel M2, only the right wheel reversed (the motors face opposite ways)',
                'Left power, right power, wheel degrees, brake — the program waits until the move is finished',
                'Negative power = backwards (the app adds brackets around negative numbers)']),
    dict(title='Driving by time', desc='Switch the unit to seconds and the command becomes MoveTime.',
         notes=['Drive for 1.5 seconds, then coast']),
  ],
  arduino=['Move…Degs / Move…Time commands <b>wait until finished</b>, unlike setPower which moves on immediately.',
           'A wheel with diameter d cm travels π × d cm per 360°. Use this to turn a distance into degrees.'],
  tries=[dict(task='Drive forward 1 wheel turn, stop 1 s, 3 times (use repeat).', answer=''),
         dict(task='Left wheel 60, right wheel 20, drive for 2 seconds. Which way does the robot turn?', answer='The left wheel is faster, so the robot curves to the right.')],
  quiz=[dict(q='What happens if you forget the Set Movement block?', choices=['The Movement blocks do not know which motors the wheels use, so the robot does not drive', 'The robot drives normally', 'The light blinks'], why='begin() must always come first.'),
        dict(q='MoveDegs(50, 50, 360, true) — what is 360?', choices=['The degrees the wheels turn', '360 cm', '360 ms'], why='The unit is wheel degrees.')])

L['u1-sync'] = dict(
  title='Movement 2: driving straight with Sync and Gyro',
  goals=['Compare power / Sync / Gyro', 'Meet the Set PID block'],
  intro='Two motors are never exactly the same, so a robot driven with plain power usually drifts. Movement has two helpers: <b>Sync</b> uses the encoders to keep both wheels turning equally, and <b>Gyro</b> uses the gyroscope on the board to hold the direction.',
  examples=[
    dict(title='Test all three', desc='Press Up and the robot drives 3 wheel turns with each method. Which one is the straightest?',
         notes=['Sync: the board watches both encoders and evens them out', 'Gyro: speed, target heading (the block always puts 0), wheel degrees, brake']),
    dict(title='Tuning the Gyro drive PID', desc='Recommended values from the MATRIX manual for TT motors (put in Setup before driving).',
         notes=['Kp corrects drift immediately, Ki corrects what builds up, Kd reduces wobbling']),
  ],
  arduino=['Default PID values for TT motors from the manual: MoveSync (0.02, 0, 0.04) · MoveGyro (6.01, 0, 2.15) · TurnGyro (22.75, 0.08, 0.25)',
           'Too much Kp makes the robot wobble; too little Kp makes it correct slowly.'],
  tries=[dict(task='Drive with Gyro for 2 seconds at speed 50, then coast.', answer='')],
  quiz=[dict(q='Which method uses the gyroscope on the board to hold the direction?', choices=['Move(Gyro)', 'Move(Sync)', 'Move for … power'], why='Sync uses the encoders; Gyro uses the IMU.'),
        dict(q='The robot wobbles left and right quickly while driving with Gyro. What should you try first?', choices=['Lower Kp or raise Kd', 'Raise Kp even more', 'Set Ki to 100'], why='Too much Kp causes swinging; Kd damps it.')])

L['u1-moving'] = dict(
  title='Movement 3: continuous driving, stopping yourself, measuring distance',
  goals=['Use Moving at … together with Stop moving', 'Measure distance with degrees counted'],
  intro='The <b>Moving</b> blocks start the robot and the program moves on immediately. That lets you check other conditions while driving — distance, time or sensors — and then use Stop moving yourself.',
  examples=[
    dict(title='Drive until a distance you measure', desc='Reset the distance, drive with Sync, wait until the distance is ≥ 1000 degrees, then stop.',
         notes=['Starts driving and goes to the next line immediately', 'Keep waiting until the distance is reached', 'Stop moving with Brake']),
    dict(title='Drive until the button is pressed', desc='Press Down to stop immediately, then show the distance on the screen.', notes=[]),
  ],
  arduino=['Moving = <code>Move</code> / <code>MoveSync</code> / <code>MoveGyro</code> — no Degs/Time in the name, so they never stop by themselves.',
           'Moving at … % power (<code>Move</code>) has no PID. It suits line-following algorithms that calculate the wheel power themselves.'],
  tries=[dict(task='Drive for 3 seconds with Moving(Sync), then stop (use wait instead of measuring distance).', answer='')],
  quiz=[dict(q='You use Moving at … and never use Stop moving. What happens?', choices=['The robot keeps driving', 'The robot stops after 1 second', 'The robot does not move'], why='The command has no distance or time to stop at.'),
        dict(q='What does DriveDC getDegrees() measure?', choices=['The average of the left and right wheel degrees', 'The gyro angle', 'The driving time'], why='(|left| + |right|) ÷ 2')])

L['u1-turn'] = dict(
  title='Movement 4: gyro turns, single wheel / two wheels',
  goals=['Choose between Turn Single-Wheel and Turn Two-Wheel', 'Experiment to see what happens when you turn several times in a row'],
  intro='Both turn blocks use the <b>gyro (IMU)</b> to measure the angle. A positive angle = clockwise (right), negative = anticlockwise (left). In the code both are the same command, <code>TurnGyro</code>, with a different mode number.',
  examples=[
    dict(title='Drive a square', desc='Drive and turn 4 times (use repeat).',
         notes=['Reset the gyro before starting (a block from the Sensing category)', 'Speed 40, angle 90, mode 1 = two wheels, brake']),
  ],
  arduino=['Turn Single-Wheel → mode <code>0</code>, one wheel turns, wide curve · Turn Two-Wheel → mode <code>1</code>, spins on the spot.',
           'The manual calls this angle the gyro <i>heading</i>. Try the experiment below to find out how your robot counts the angle.'],
  tries=[dict(task='<b>Experiment:</b> use Turn Two-Wheel 90° twice in a row. Does the robot turn 180° in total, or only 90° and then stay? Write down the result, then try changing the second turn to 180°.',
              answer='If it only turns 90°, the angle is a target heading counted from the gyro reset, so you need 90, 180, 270 … If it turns 180°, the angle is added to the current direction.'),
         dict(task='Turn left 90° with one wheel.', answer='Use a negative angle, −90.')],
  quiz=[dict(q='How does TurnGyro(40, 90, 0, true) turn?', choices=['With one wheel', 'With two wheels turning opposite ways', 'Backwards'], why='Mode 0 = Single-Wheel.'),
        dict(q='You need to spin round in a tight space. Which block should you use?', choices=['Turn Two-Wheel', 'Turn Single-Wheel', 'Move for'], why='It turns around the centre of the robot.')])

L['u3-wait'] = dict(
  title='Time: wait and millis',
  goals=['Use wait (delay) to pause', 'Use millis to measure time without stopping the program'],
  intro='<b>wait</b> makes the board pause and do nothing else. <b>millis</b> is a clock that keeps running; you read the time and decide yourself, so the board can do other work at the same time.',
  examples=[
    dict(title='Stopwatch', desc='Show the number of seconds since the board was switched on.',
         notes=['millis counts in milliseconds; divide by 1000 to get seconds']),
    dict(title='Blink and read a button at the same time', desc='No long wait, so the button responds instantly. The variable <code>last</code> remembers when the light last changed.',
         notes=['Has more than 500 ms passed since last time?', 'Swap 0 ↔ 1']),
  ],
  arduino=['During <code>delay()</code> the board does not read buttons or sensors. A button press at that moment is missed.', 'The pattern <code>millis() - last &gt; interval</code> is a standard Arduino technique.'],
  tries=[dict(task='5-second timer: when millis passes 5000, turn on a red light.', answer='')],
  quiz=[dict(q='How many seconds is wait 2000?', choices=['2 seconds', '20 seconds', '0.2 seconds'], why='1000 ms = 1 s'),
        dict(q='Why does the second example not use wait 500?', choices=['So it can read the button all the time', 'wait does not work with lights', 'millis is always more accurate'], why='wait stops the board from doing anything else.')])

L['u3-if'] = dict(
  title='Decisions: if and if … else',
  goals=['Write a condition with if', 'Read if(…) { } else { } in code'],
  intro='if takes a hexagon block (true/false) as its condition, for example a button press or a number comparison.',
  examples=[
    dict(title='Battery warning light', desc='if inside if: above 7.6V green, above 7.0V yellow, otherwise red.',
         notes=['The condition sits in the brackets after if', 'What runs when the condition is false']),
  ],
  arduino=['An if without else in code is just <code>if(condition) { … }</code>', 'Braces must open and close in pairs. If one is missing when you write code yourself, it will not compile.'],
  tries=[dict(task='Press Up for a high beep; when not pressed, show a dim blue light.', answer='')],
  quiz=[dict(q='An if without else: what happens when the condition is false?', choices=['It skips to the next block', 'The program stops', 'It runs the inside anyway'], why='There is nothing else to do.')])

L['u3-loop'] = dict(
  title='Repeat: repeat and forever',
  goals=['Use repeat for a set number of times', 'Read for loops and while(true) in code'],
  intro='repeat becomes a <code>for</code> loop with a counter. forever becomes <code>while(true)</code>, which never ends.',
  examples=[
    dict(title='3 beeps at start-up', desc='Then the green light turns on.',
         notes=['Start with i_0 = 0, continue while i_0 &lt; 3, add 1 each time → 3 rounds (0, 1, 2)']),
    dict(title='forever in Setup', desc='Works like Loop, but any block placed after forever will never run.',
         notes=['The condition is always true, so it never ends']),
  ],
  arduino=['The counter name <code>i_0</code> is made automatically. With several repeats you get i_1, i_2 …', 'When writing yourself in Arduino, people usually write <code>for (int i = 0; i &lt; 3; i++)</code>'],
  tries=[dict(task='Blink 5 times and then stay off.', answer=''),
         dict(task='repeat inside repeat: beep twice, pause 1 second, 3 sets in total.', answer='The inner loop uses the counter i_1, the outer loop uses i_0.')],
  quiz=[dict(q='How many rounds does for(int i_0 = 0; i_0 &lt; 10; i_0++) run?', choices=['10', '11', '9'], why='0 to 9.'),
        dict(q='What happens to blocks placed under forever?', choices=['They never run', 'They run after forever finishes', 'They run at the same time'], why='while(true) never exits.')])

L['u3-until'] = dict(
  title='Wait and loop until: wait until · repeat until',
  goals=['Wait for a condition with wait until', 'Repeat until a condition becomes true with repeat until'],
  intro='Both blocks become a <code>while(!condition)</code> loop, read as “as long as it is <b>not</b> true yet”. The <code>!</code> sign means not.',
  examples=[
    dict(title='Press the button to start', desc='As used in competitions: wait for the button, then drive.',
         notes=['An empty waiting loop (the ; comes right away) until the button is pressed']),
    dict(title='Blink until Down is pressed', desc='repeat until has commands inside to run while waiting.', notes=[]),
  ],
  arduino=['<code>while(!x);</code> — if the condition never becomes true, the program is stuck here forever. Check your condition carefully.'],
  tries=[dict(task='Drive with Moving(Gyro) until Down is pressed, then stop.', answer='')],
  quiz=[dict(q='repeat until (button pressed): when does it stop repeating?', choices=['When the button is pressed', 'When the button is released', 'After 10 rounds'], why='until = up to the moment that.')])

L['u4-vars'] = dict(
  title='Variables: make, set, change',
  goals=['Make a variable and use set / change', 'Know that variables from blocks are float'],
  intro='A variable is a named box that stores a value. Make one in the Variables category with Make a Variable. Use English letters, no spaces, and do not start with a number.',
  examples=[
    dict(title='Count button presses', desc='Each press adds 1 (wait for the release first so it is not counted twice).',
         notes=['The variable is declared at the top, outside setup/loop, so every part can use it', 'set → give it a value', 'change by 1 → take the old value, add 1, store it back']),
  ],
  arduino=['Every variable from blocks is a <code>float</code> (decimal), so the screen shows 3.00. When writing yourself, use <code>int</code> for counting.',
           'Variable names are case-sensitive: <code>Score</code> and <code>score</code> are different variables.'],
  tries=[dict(task='Variable speed starts at 30. Each press of Up adds 10, then show it on the screen.', answer='')],
  quiz=[dict(q='Which code does change score by -2 give?', choices=['score = score + -2;', 'score = -2;', 'score - 2;'], why='change = add to the old value.'),
        dict(q='What type are variables made with blocks?', choices=['float', 'int', 'String'], why='The code generator declares every one as float.')])

L['u4-math'] = dict(
  title='Math: + − × ÷ mod round and math functions',
  goals=['Nest math blocks', 'Watch out for integer division and an option that does not compile'],
  intro='Math blocks are round, so they fit into any number slot. Nested blocks become brackets in the code.',
  examples=[
    dict(title='Distance from wheel degrees', desc='Wheel diameter 6.5 cm. Distance (cm) = degrees × 3.14 × 6.5 ÷ 360. Push the robot by hand and watch the number.',
         notes=['Inner blocks are calculated first, like brackets in maths', 'This value is a whole number, so <b>multiply before dividing</b>. Dividing by 360 first, 500 ÷ 360 gives 1 instead of 1.39']),
    dict(title='Careful! Integer division', desc='7 ÷ 2 gives 3 in code, not 3.5, but storing it in a variable first gives 3.5.',
         notes=['int ÷ int = int, gives 3', 'a is a float, so the result is 3.50']),
  ],
  arduino=['mod in blocks uses <code>fmod(a, b)</code>, which works with decimals. With int when writing yourself, use <code>a % b</code>.',
           'The <b>ceiling</b> option in the abs/floor… block makes <code>ceiling()</code>, which does not compile. In Arduino change it to <code>ceil()</code>.',
           'Plain sin/cos use radians. For degrees choose “sin (degrees)”.'],
  tries=[dict(task='Show EVEN or ODD for the number of button presses (use mod 2 and compare with 0).', answer='')],
  quiz=[dict(q='What does Serial.println((7 / 2)); show?', choices=['3', '3.5', '4'], why='Integer division throws the remainder away.'),
        dict(q='What is 10 mod 4?', choices=['2', '2.5', '0'], why='10 = 4×2 + 2')])

L['u4-logic'] = dict(
  title='Compare and logic: &lt; = &gt; and or not',
  goals=['Build conditions from comparisons', 'Combine conditions with and / or / not'],
  intro='Hexagon blocks give true/false. Use them in if, wait until and repeat until.',
  examples=[
    dict(title='Press both buttons together', desc='Green light only when Up <b>and</b> Down are pressed together.',
         notes=['and = true when both sides are true']),
    dict(title='Is the value in range?', desc='Analog A1 between 300 and 700: green; outside the range: red.', notes=[]),
  ],
  arduino=['<code>=</code> in blocks becomes <code>==</code> in code. If you write a single = inside if yourself, it becomes an assignment (a common bug).',
           'or → <code>||</code> · not → <code>!</code>'],
  tries=[dict(task='Red light when the battery is below 7V <b>or</b> Down is pressed.', answer='')],
  quiz=[dict(q='What is !(5 &gt; 3)?', choices=['false', 'true', '2'], why='5 > 3 is true, and not flips it to false.'),
        dict(q='What is wrong with if (x = 5) in code you write yourself?', choices=['It assigns a value instead of comparing', 'Nothing', 'You must use === like JavaScript'], why='Comparison needs ==.')])

L['u4-range'] = dict(
  title='Random and value ranges: random · map · constrain',
  goals=['Pick random numbers', 'Convert a sensor range to a useful range and stop values going too far'],
  intro='map and constrain are used all the time with sensors and motors, for example turning 0–1023 into a speed of 0–100.',
  examples=[
    dict(title='Dice', desc='Press the button to roll 1–6 (Arduino excludes the last number, so we put 7).',
         notes=['Uses the value of an unconnected pin (which jitters) as the seed, so the numbers differ every time the board starts', 'gives 1–6']),
    dict(title='Knob controls motor speed', desc='Analog 0–1023 → speed 0–100, then limited to at most 80.',
         notes=['Value, old range (low high), new range (low high)', 'The result is always within 0–80']),
  ],
  arduino=['Arduino’s <code>map()</code> works with whole numbers (decimals are dropped).', '<code>random(a, b)</code> gives a to b−1.'],
  tries=[dict(task='Random light colour, each of R G B 0–255, every 0.5 seconds.', answer='')],
  quiz=[dict(q='About how much is map(512, 0, 1023, 0, 100)?', choices=['50', '512', '100'], why='512 is in the middle of the old range, so it gives the middle of the new range.'),
        dict(q='What is constrain(130, 0, 100)?', choices=['100', '130', '0'], why='Above the maximum, so you get the maximum.')])

L['u4-text'] = dict(
  title='Text: join · letter of · length · converting types',
  goals=['Join text with numbers for display', 'Know the difference in how letter positions are counted'],
  intro='Text blocks use Arduino’s <code>String</code> class. They are handy for showing results on the screen or in Serial.',
  examples=[
    dict(title='Battery with its unit', desc='Join the word BAT with the voltage and the letter V.',
         notes=['Turn every piece into a String and join them with +']),
    dict(title='Letter position', desc='letter 1 of “world” in blocks, but <code>charAt(1)</code> in code counts from 0, so you get <b>o</b>.', notes=[]),
  ],
  arduino=['<code>String("world").charAt(0)</code> is w — C++ counts positions from 0.',
           'The to Number block with a number typed straight into the slot does not compile. In Arduino write <code>String("100.1").toFloat()</code>.'],
  tries=[dict(task='Show “SPEED: ” followed by the value of the variable speed.', answer='')],
  quiz=[dict(q='What is String("robot").length()?', choices=['5', '4', '6'], why='r-o-b-o-t'),
        dict(q='What is String("robot").charAt(0)?', choices=['r', 'o', 'b'], why='Position 0 is the first letter.')])

# ---------------- Unit 6: phone remote control (Bluetooth 6.1–6.5, builder 6.6, WiFi 6.7–6.9) ----------------
L['u6-ble-hello'] = dict(
  title='First Bluetooth: name the robot, send a message, the robot replies',
  goals=['Turn on Bluetooth, give the robot a name no classmate uses, and connect from a phone', 'Receive messages from the phone with a hat block, and send messages back to the phone'],
  intro='The UNO R4 WiFi board has Bluetooth LE built in. With the <b>IoT</b> blocks it can talk to a phone with no internet. On the phone, open this site’s <b>controller page</b> (the purple “Open this lesson’s controller” button below), tap “Connect” and choose your robot’s name. The program has two parts: <b>R4 Begin</b> turns on Bluetooth and runs <b>BLE Polling</b> again and again, and the <b>When BLE UART Data Received</b> hat block sits on its own <b>below</b> R4 Begin. It runs every time the phone sends a message.',
  examples=[
    dict(title='Hello Bluetooth', desc='The screen shows the robot’s name and the light is red while it waits. When the phone connects, the light turns green. Type a message on the controller page and tap Send: it appears on the OLED and the robot replies OK.',
         notes=['Arduino’s Bluetooth library. The BLE blocks add this line for you.',
                'The name the phone sees when it searches. Every robot in the room needs a different name.',
                'The hat block becomes this function. It sits outside <code>setup()</code> and <code>loop()</code> and is called every time the phone sends a message.',
                'Stores the message in <code>ble_rcvData</code> (a String). The Received Data block is this variable.',
                'Sends a message back to the phone. It shows in the message window of the controller page.',
                'Lets the board check Bluetooth every round. <code>onBLEWritten</code> is called from inside this command, so a long wait in loop makes messages arrive late.',
                'Is a phone connected? Used for the status light.']),
    dict(title='Send the battery voltage to the phone every second', desc='The battery voltage appears in the controller’s message window every second. millis does the timing (the time lesson in Unit 3), so loop still runs fast and can receive messages at any time.',
         notes=['Has more than 1 second passed since the last send?',
                'Turns the number into text and sends it. The phone gets a message such as 7.85.',
                'The hat block must always be there. Even if you hardly need it, give it a simple job, such as showing the message it received.']),
  ],
  arduino=['On <b>Android</b>, open the controller page in <b>Chrome</b> · on <b>iPhone/iPad</b>, use the <b>Bluefy</b> app (Safari cannot use Bluetooth from a web page). You do not need to pair in the phone’s Bluetooth settings: tap “Connect” on the controller page and choose the robot’s name.',
           'Every robot in the room needs its own name. Change <code>R4-T01</code> to your team number (English letters, numbers and - only), and when you connect, pick your own team’s robot name from the list.',
           '<b>Watch out 1:</b> a BLE Enable Nordic UART Service block without the When BLE UART Data Received hat block → it does not compile: <code>\'onBLEWritten\' was not declared</code>. The hat block must always be there, even while it is still empty.',
           '<b>Watch out 2:</b> put the hat block <b>below</b> R4 Begin. If it is higher → it does not compile: <code>\'rxChar\' was not declared</code>, because the code generator orders the blocks from top to bottom.',
           'To write it yourself in Arduino IDE, install the <b>ArduinoBLE</b> library first (Sketch → Include Library → Manage Libraries). If the phone cannot find the robot, try updating the board’s wireless firmware: Tools → <b>Firmware Updater</b>.'],
  tries=[dict(task='When you type <code>hi</code>, the robot replies <code>hello</code>. Any other message still gets <code>OK</code> (use if … else with the = block).',
              answer='Compare with <code>ble_rcvData == "hi"</code>. Small and capital letters must match: <code>hi</code> and <code>Hi</code> are different words.'),
         dict(task='Send the battery voltage only while a phone is connected, and only every 2 seconds (use the and block).', answer='')],
  quiz=[dict(q='You have the BLE Enable Nordic UART Service block but forgot the When BLE UART Data Received hat block. What happens?', choices=['It does not compile, because there is no onBLEWritten function', 'It uploads, but cannot receive messages', 'The phone cannot find the robot’s name'],
             why='The UART enable code uses <code>onBLEWritten</code>, which is made by the hat block.'),
        dict(q='There are 10 robots in the room. Why must each one have a different Bluetooth name?', choices=['The phone shows the same name several times, so you may pick the wrong one and drive a classmate’s robot', 'Only one Bluetooth connection works in a room at a time', 'Same names stop the code from compiling'],
             why='All the robots advertise their names at the same time. If the names are the same, you cannot tell them apart.'),
        dict(q='Why does example 2 not use wait 1000 in loop?', choices=['During wait the board does not call BLE.poll(), so messages from the phone arrive late', 'wait cannot be used with Bluetooth; it does not compile', 'millis sends messages faster'],
             why='<code>BLE.poll()</code> must be called often so the hat block runs as soon as a message arrives.')])

L['u6-ble-tap'] = dict(
  title='4 direction buttons: one tap, drive 0.5 seconds',
  goals=['Compare the received message with the letters F B L R', 'Drive or turn for a short time with Move(Sync) for … seconds'],
  intro='The <b>4 direction buttons (tap once)</b> controller sends one letter per tap: <code>F</code> forward, <code>B</code> backward, <code>L</code> turn left, <code>R</code> turn right. In the hat block we compare <b>BLE UART Received Data</b> with a letter using the <b>=</b> block. If it matches, the robot drives for 0.5 seconds.',
  examples=[
    dict(title='Forward and backward', desc='Start with two buttons. Tap ▲ or ▼ on the controller and the robot moves a little each time.',
         notes=['Compares the whole message. Every letter must match, so a small <code>f</code> does not count.',
                'Drives with Sync at power 50 for 0.5 seconds, then brakes. This command waits until the move is finished.',
                'Do not forget Set Movement in Setup, or the wheels will not turn.']),
    dict(title='All 4 directions, and the command on the screen', desc='Turns by spinning the wheels in opposite directions, and shows the received letter after the robot’s name. If the robot does not move, first check the screen to see what it received.',
         notes=['The received letter appears to the right of the robot’s name, so the name stays on the screen.',
                'Left wheel backward, right wheel forward → spins left on the spot.',
                'The other way round → spins right.']),
  ],
  arduino=['The received message is a <code>String</code> called <code>ble_rcvData</code>, but every variable made with blocks is a float and cannot hold letters. So we compare the Received Data block with = right inside the hat block.',
           'Move(Sync) for … seconds → <code>MoveSyncTime(left, right, seconds, brake)</code> <b>waits until the move is finished</b>. Meanwhile the board does not read new messages, so if you tap too fast the robot cannot keep up.',
           'In C++ you can chain if … else if, for example <code>if (ble_rcvData == "F") { … } else if (ble_rcvData == "B") { … }</code>'],
  tries=[dict(task='Add a horn: in the controller builder, tap “+ Add button”, set Text on press to <code>H</code>, then make the robot beep for 0.2 seconds when it receives <code>H</code>.',
              answer='An extra button can send any text you set. The robot only needs an if that compares with that text.')],
  quiz=[dict(q='The phone sends <code>f</code> (small letter). What does the robot in the example do?', choices=['It does not move, because "f" is not equal to "F"', 'It drives forward as usual', 'It does not compile'],
             why='Text comparison treats small and capital letters as different.'),
        dict(q='Why do we compare Received Data with the = block directly, instead of storing it in a variable first?', choices=['Block variables are float and cannot hold letters', 'Variables make the robot slower', 'Hat blocks cannot use variables'],
             why='MATRIXblock declares every variable as a float, while the message is in <code>ble_rcvData</code>, which is a String.'),
        dict(q='While the robot is driving for 0.5 seconds, you keep tapping other buttons. What happens?', choices=['The board does not read new messages until the move is finished', 'The robot stops at once and does the new command', 'The robot drives faster'],
             why='<code>MoveSyncTime</code> waits until the move is done and does not call <code>BLE.poll()</code> meanwhile. That is why the next lesson uses Moving, which does not wait.')])

L['u6-ble-hold'] = dict(
  title='Hold to drive, release to stop, and stop by itself when the signal is lost',
  goals=['Let the hat block only remember the command, and let loop drive the wheels with Moving at …', 'Build a fail-safe: if the phone disconnects or goes quiet for more than 0.5 seconds, the robot must stop by itself'],
  intro='The <b>4 direction buttons (hold down)</b> controller sends the letter again every 0.15 seconds while your finger stays down, and sends <code>S</code> when you let go. The <b>Moving at …</b> block keeps the robot driving until it is told to stop. If the signal drops on the way, the S never arrives and the robot keeps going. So in this lesson the robot <b>remembers the time</b> of the last message in the variable <code>last</code>. If it has been quiet for more than 0.5 seconds, or the phone has disconnected, it stops by itself.',
  examples=[
    dict(title='Test the fail-safe with a light', desc='No wheels yet, make it safe first: hold a button on the controller and the light is green. Let go, and after 0.5 seconds the light turns red.',
         notes=['Every time a message comes in, remember the time in the variable <code>last</code>.',
                '<code>!</code> is not: the phone is <b>not</b> connected · <code>||</code> is or · or it has been quiet for more than 500 ms (while you hold a button the controller sends every 150 ms, so with a good signal it is never quiet this long)']),
    dict(title='Hold to drive, release to stop', desc='The hat block turns the letter into left wheel power <code>l</code> and right wheel power <code>r</code>. loop checks the fail-safe and drives the wheels every round.',
         notes=['Turn left: left wheel −40, right wheel 40. It spins on the spot, slower than driving straight, so it is easy to aim.',
                'Finger up → the controller sends S → both wheels are set to power 0.',
                'Moving at … moves on at once without waiting, so loop runs fast and can receive messages all the time.',
                'Stops when l and r are both 0.']),
  ],
  arduino=['Keep the jobs separate: <code>onBLEWritten</code> only remembers values (<code>l</code>, <code>r</code>, <code>last</code>) and <code>loop()</code> drives the wheels. That way the safety check lives in one place.',
           'When the signal fades quietly (you walk out of range), it can take several seconds before <code>BLE.connected()</code> becomes false. Timing 0.5 seconds of silence stops the robot sooner.',
           'Block variables are float, which keeps millis exact for only about the first 4 hours after switching on. When you write it yourself, use <code>unsigned long last;</code>',
           'Test on the table first: lift the robot so the wheels are in the air, hold and release, and check that the wheels really stop before you put it on the floor.'],
  tries=[dict(task='Add a status light: blue while the wheels turn, off when stopped.', answer=''),
         dict(task='Change the turns into curves: <code>L</code> gives left wheel 10, right wheel 50, and <code>R</code> gives left wheel 50, right wheel 10.',
              answer='One wheel still drives forward, so the robot curves instead of spinning on the spot.')],
  quiz=[dict(q='You remove the fail-safe, and the signal is lost while you are holding forward. What happens?', choices=['The robot keeps driving, because l, r are still 50 and the S message never arrives', 'The robot stops by itself at once', 'The robot backs up towards the phone'],
             why='Moving at … never stops by itself; something must tell it to stop.'),
        dict(q='There is already a BLE Connected? block. Why also check millis − last &gt; 500?', choices=['When the signal fades quietly, the board may take several seconds to notice', 'BLE Connected? cannot be used in loop', 'millis makes the robot drive faster'],
             why='While you hold a button, the controller repeats every 0.15 seconds, so more than 0.5 seconds of silence means the signal has a problem, and the robot stops to be safe.'),
        dict(q='Why does this lesson use Moving at … in loop instead of Move(Sync) for 0.5 seconds?', choices=['Moving does not wait, so loop runs fast and can receive messages all the time', 'Moving is more accurate', 'Move(Sync) does not work with Bluetooth'],
             why='If the command waits until the move is done, the robot stops late when you release the button.')])

L['u6-ble-stick'] = dict(
  title='One stick: split one number into left and right wheel power',
  goals=['Turn a message made of digits into a number with to Number', 'Split one number into two values with ÷, floor and mod'],
  intro='The stick must send both the left and the right wheel power in <b>one message</b>, but MATRIXblock has no block for cutting up text. So the controller packs the two values into one number: <code>(left + 100) × 1000 + (right + 100)</code>. For example, left 60 and right 40 is sent as <code>160140</code>. The robot splits it back by dividing: floor(160140 ÷ 1000) = 160 → 160 − 100 = <b>60</b>, and 160140 mod 1000 = 140 → 140 − 100 = <b>40</b>. While you hold the stick, the controller repeats every 0.1 seconds, and it sends <code>S</code> when you let go.',
  examples=[
    dict(title='Drive with the stick', desc='loop is the same as in lesson 6.3, block for block (the same fail-safe). Only the hat block changes.',
         notes=['The text "160140" → the number 160140. Text that is not a number, such as "S", gives 0.',
                'A stick number is always ≥ 1000, while a letter gives 0 and so goes to else.',
                '160140 ÷ 1000 = 160.14 → floor → 160 → −100 → left wheel 60',
                'The remainder after dividing by 1000 = 140 → −100 → right wheel 40',
                'The same loop from lesson 6.3 drives the wheels with the split values.']),
    dict(title='Going further in C++: send it as the text J,60,40',
         desc='This example is plain C++ with no blocks. In Arduino IDE you can cut up text with <code>indexOf</code> and <code>substring</code>, but this site’s controller sends one number. To use this way, edit the controller file you copied (lesson 6.6) so it sends <code>"J," + left + "," + right</code> instead.',
         notes=['A stick message starts with J and a comma.',
                'Finds the position of the second comma (searching from position 2). In "J,60,40" that is 4.',
                'Cuts from position 2 up to the comma, giving "60", then turns it into a number.',
                'Cuts from after the comma to the end, giving "40".',
                'Writing it yourself, you can choose the variable types: <code>int</code> for wheel power, <code>unsigned long</code> for time.']),
  ],
  arduino=['Why the controller limits each wheel to −99 … 99: left + 100 is then between 1 and 199, so the number sent is always ≥ 1000 (the lowest is left −99, right −99 → <code>1001</code>). <code>toFloat("S")</code> gives 0, so the robot can tell stick numbers from letters.',
           'A float holds whole numbers exactly up to about 16 million, so the largest stick number, 199199, is never off.',
           'Writing it yourself with <code>long</code>, you can use <code>v / 1000</code> (integer division drops the remainder for you) and <code>v % 1000</code> instead of floor and fmod.',
           'You can copy example 2 into Arduino IDE as a whole file (install the ArduinoBLE library first).'],
  tries=[dict(task='Test before driving: show <code>l</code> and <code>r</code> on the OLED every time a stick number arrives. Do not drive the wheels yet. Then move the stick in different directions.',
              answer='Push it all the way up: l and r are close to 60 (the controller’s top power is set to 60%). Push it to the right: l is positive and r is negative, so the robot spins right.')],
  quiz=[dict(q='The phone sends <code>100100</code>. What does the robot do?', choices=['It stops, because l = 0 and r = 0', 'It drives forward at full power', 'Nothing, because it is a letter'],
             why='100 − 100 = 0 for both wheels: the stick is in the middle.'),
        dict(q='The phone sends <code>40199</code>. What are l and r?', choices=['l = −60, r = 99', 'l = 40, r = 199', 'l = 60, r = −99'],
             why='floor(40199 ÷ 1000) = 40 → 40 − 100 = −60, and 40199 mod 1000 = 199 → 199 − 100 = 99'),
        dict(q='Why does the controller keep each wheel’s power within ±99?', choices=['So the number sent is always ≥ 1000 and the robot can tell stick numbers from letters', 'The motors cannot take the value 100', 'Bluetooth cannot send numbers longer than 6 digits'],
             why='If left could be −100, you would get 0 × 1000 + …, which is below 1000, and the robot would think it was a letter (<code>toFloat("S")</code> gives 0).')])

L['u6-ble-twostick'] = dict(
  title='Two sticks + arm up/down buttons (servo)',
  goals=['Use the driving code from lesson 6.4 with the two-stick controller without changing it', 'Add extra buttons U / D that make a servo lift the arm'],
  intro='The <b>two sticks</b> controller: the left stick drives forward and back, the right stick turns. The phone first mixes the two sticks into left and right wheel power, then sends one number as before. So the robot’s driving code is <b>the same as lesson 6.4, line for line</b>. What is new is two extra buttons: arm up sends <code>U</code>, arm down sends <code>D</code>, and the robot turns the servo on RC1 to 150° or 60°.',
  examples=[
    dict(title='Test the arm only', desc='Plug the servo into RC1, no driving yet. Tap the arm up/down buttons on the controller and check that the arm moves the right way.',
         notes=['An extra button sends the text set in the controller builder. The defaults are U and D.',
                'Arm up. If the arm moves the wrong way, swap 150 and 60.',
                'Arm down (Setup also sets 60, so the arm starts down).']),
    dict(title='Drive with two sticks + arm', desc='The hat block from lesson 6.4 with two more ifs in the else part (messages that are not stick numbers). loop stays the same.',
         notes=['Stick number → split into l, r as in lesson 6.4',
                'U, S and D are letters. <code>toFloat</code> gives 0, so they end up in the else part.',
                'setAngle moves on at once, so you can drive and lift the arm at the same time.']),
  ],
  arduino=['The two-stick controller sends the same kind of numbers as the one-stick controller. The lesson 6.4 controller can also drive this robot (but it has no arm buttons).',
           'An extra button can have both a text on press and a text on release. For example, press sends <code>G</code> and release sends <code>g</code>, for a gripper that only grips while you hold the button.',
           'With more servos, use ports RC2–RC4 with new texts, e.g. <code>O</code> / <code>C</code> to open and close a gripper.'],
  tries=[dict(task='Each tap of arm up lifts the arm by 15° (at most 150), and each tap of arm down lowers it by 15° (at least 60). Use a variable <code>arm</code> and the constrain block.',
              answer='<code>constrain</code> keeps the value within 60–150, so extra taps never turn it past the limits.'),
         dict(task='In the controller builder, add a 3rd button that sends <code>M</code> and moves the arm to the middle, 105°.', answer='')],
  quiz=[dict(q='You switch from the lesson 6.4 controller to two sticks. Must you change the part of the robot code that splits the stick number?', choices=['No, the phone mixes the two sticks into one number as before', 'Yes, it must receive two separate messages', 'Yes, it must change to a 12-digit number'],
             why='The phone turns the left and right sticks into wheel power before sending, so the robot gets the same data as before.'),
        dict(q='Why are the ifs for U and D in the else part?', choices=['U and D are letters: toFloat gives 0, which is less than 1000', 'Anywhere else, it does not compile', 'To make the arm move faster'],
             why='Every message that is not a stick number ends up in else.'),
        dict(q='You tap arm up while driving with the stick. What does the robot do?', choices=['It keeps driving, and the arm moves at the same time', 'It stops and waits until the arm has finished moving', 'The arm does not move until you let go of the stick'],
             why='<code>setAngle</code> does not wait, so loop keeps driving the wheels with l, r.')])

L['u6-builder'] = dict(
  title='Design your own controller: add buttons, copy the HTML, open it and test',
  goals=['Change a controller in the controller builder: pick a layout, add buttons, rename them, turn the arrow, drag them around and set the text each button sends',
         'Copy the HTML into your own file, read what each part does, change values yourself, then open it and test'],
  intro='This lesson has <b>no new blocks</b>. The robot can use the program from lesson 6.5 as it is. What changes is the phone side. Tap “Open this lesson’s controller” to get the controller builder. It has 3 settings parts: '
        '<b>1. Pick a layout</b> · <b>2. Settings</b> (robot name, connection, wheel power) · <b>3. Extra buttons</b> (add, rename, turn, drag). '
        'The controller preview changes straight away. Tap <b>Test with robot</b> to try driving. When you are happy, tap <b>Copy HTML</b> or <b>Download .html</b> to get one file with comments in English.',
  examples=[
    dict(title='The same robot from lesson 6.5', desc='The new controller still sends the same messages (stick numbers, S, U, D), so the robot program needs no changes. See which line each value in the controller builder goes with.',
         notes=['Set the controller’s <b>Robot name</b> to match this name. If you connect to a robot with another name, the controller warns you.',
                'The arm up button’s <b>Text on press</b> is <code>U</code>. It must match the if exactly, letter for letter.',
                'A button must not send a number of 1000 or more, or the robot will think it is the stick.',
                '<b>Top wheel power</b> 60 → l, r stay within ±60. You can change it in the controller without changing the robot.']),
    dict(title='A button that sends on press and on release: headlights', desc='Add a “Light” button with Text on press <code>W</code> and Text on release <code>w</code>. Hold it and the lights are on; let go and they turn off.',
         notes=['Text on press → both lights white',
                '<b>Text on release</b> (small w) → lights off. If the screen turns off or you switch apps while holding, the controller still sends w.']),
  ],
  arduinoTitle='Editing the controller file you copied',
  arduino=['Open the file in a text editor such as VS Code. The file is split into parts, with comments that explain them: <code>&lt;style&gt;</code> colours and sizes · <code>&lt;main id="pad"&gt;</code> sticks and buttons · <code>&lt;script&gt;</code> the controller’s program',
           '<b>Settings</b> are at the top of <code>&lt;script&gt;</code>: <code>const CONFIG = {</code> holds the robot name and <code>speed: 60</code>. For example, change it to 80 and the robot is stronger when you push the stick all the way.',
           'The <b>connection</b> is <code>const Link = {</code> (Bluetooth or MQTT). Every button sends its text through <code>function send(text)</code>.',
           '<b>Buttons</b>: one extra button is one <code>&lt;button&gt;</code> line. Change <code>data-press="U"</code> to send other text · <b>Sticks</b>: <code>holdRepeat(…, 100)</code> sends the value again every 100 milliseconds.',
           'Test your own file: ① in the controller builder, paste the code into <b>Test my file</b> and tap <b>Open pasted file</b> ② on a computer, double-click the file so it opens in Chrome',
           '③ put it on GitHub Pages: upload the file as <code>index.html</code> to a repository, then open Settings → Pages to get an https link · Bluetooth from a web page only works on https pages or on files on your computer'],
  tries=[dict(task='Add a horn button: tap <b>+ Add button</b>, set the Label to “Horn” and Text on press to <code>G</code>, turn the arrow to 90°, drag it to an empty spot, then make the robot beep when it gets <code>G</code>.',
              answer='1 new button = 1 new if in the else part. The text must match letter for letter.'),
         dict(task='Change <b>Main controls</b> to “4 direction buttons, hold down”. What must you add to this robot?',
              answer='F B L R are not stick numbers, so they go to the else part. Add the ifs for F B L R as in lesson 6.3, and the robot accepts both the stick controller and the button controller.')],
  quiz=[dict(q='You add an extra button that sends <code>G</code> in the controller builder, but you have not changed the robot program yet. What happens when you press it?', choices=['The robot receives G but does nothing, because no if compares with G', 'The robot freezes and needs a reset', 'The controller refuses to send G'],
             why='A message that matches no if is simply ignored. Every new button needs a matching if in the robot.'),
        dict(q='In the file you copied, you want the robot to be stronger when the stick is pushed all the way. What do you change?', choices=['speed in CONFIG', 'the button’s data-press', 'name in CONFIG'],
             why='<code>speed</code> is the top wheel power the stick sends, the same value as “Top wheel power” in the controller builder.'),
        dict(q='A button has an empty “Text on release” box. What does the controller send when you lift your finger off it?', choices=['Nothing', 'S', 'The press text again'],
             why='The controller only sends text that is not empty. If the robot should know you let go, set a Text on release, such as <code>w</code>.')])

L['u6-mqtt-hello'] = dict(
  title='WiFi + MQTT: send messages over the internet, the robot sends the battery voltage back',
  goals=['Connect the board to 2.4 GHz WiFi and an MQTT broker, then receive messages from your own robot’s topic', 'Send the battery voltage from the robot back to the phone with MQTT Publish'],
  intro='Bluetooth only works inside the room. Over the <b>internet</b>, you can be as far apart as you like. This lesson uses <b>MQTT</b>: a middleman computer called the <b>broker</b> (<code>broker.hivemq.com</code>) takes each message that someone sends (<b>Publish</b>) to a <b>topic</b> and passes it on to every device that has signed up (<b>Subscribe</b>) for that topic. '
        'The controller sends commands to <code>mr4/R4-T01/cmd</code> and the robot answers on <code>mr4/R4-T01/msg</code> · Setup: connect WiFi → connect MQTT → Subscribe · Loop: <b>MQTT Polling</b>',
  examples=[
    dict(title='Hello MQTT', desc='The light is orange while it connects to WiFi and the broker, and turns green when done. Send a message from the controller page: it appears on the OLED and the robot replies OK.',
         notes=['The MQTT library (you need to install it).',
                'The hat block. It must come before <code>connectMQTT</code>, which uses it, so it goes above R4 Begin.',
                'Joins the received bytes into a String = the MQTT Received Message block.',
                'Sends OK to the msg topic. It shows in the controller’s message window.',
                'Change these to your real WiFi name and password. This command waits until it is connected.',
                'Broker, port 1883, ID <code>R4-T01</code>',
                'Listens to your own robot’s command topic.',
                'Must run often for messages to come in. No long waits.']),
    dict(title='Send the battery voltage to the phone every 2 seconds', desc='The battery voltage appears in the controller’s message window every 2 seconds. millis does the timing as in lesson 6.1, so Loop still runs fast.',
         notes=['The hat block must always be there. Something simple inside is fine.',
                'More than 2000 ms since last time?',
                'Sends the battery voltage as text, e.g. 7.85']),
  ],
  arduino=['The board can only join <b>2.4 GHz</b> WiFi. A phone hotspot works (iPhone: turn on “Maximize Compatibility” · Android: choose the 2.4 GHz band). Some school WiFi blocks port 1883; if it will not connect, try a hotspot.',
           'Light stays orange? Open the Serial Monitor (9600): stuck at <code>WiFi Connection..</code> = wrong name/password, or the WiFi is 5 GHz · stuck at <code>MQTT Connection..</code> = port 1883 is blocked, or there is no internet',
           '<b>A public broker</b>: anyone who knows the topic name can send to your robot. So every team uses its own robot name in the topic and in the ID (if two IDs are the same, the broker disconnects the one that connected first), and never send personal information.',
           '<b>Watch out 1:</b> MQTT Connect without the When MQTT Message Received hat block → it does not compile: <code>\'mqttCallback\' was not declared</code>',
           '<b>Watch out 2:</b> the MQTT hat block must be <b>above</b> R4 Begin (the opposite of Bluetooth). If it is below, it also fails to compile with the same message.',
           'Arduino IDE: install the <b>PubSubClient</b> library (WiFiS3 comes with the board). If WiFi will not connect even though everything is right, try updating the wireless firmware: Tools → <b>Firmware Updater</b>'],
  tries=[dict(task='Type <code>bat</code> in the message window and the robot replies with the battery voltage at once. Other messages still go on the screen as before.',
              answer='You can Publish inside the hat block. The received message is already stored in <code>mqtt_rcvMessage</code>.'),
         dict(task='Change example 1 for team 7’s robot, named <code>R4-T07</code>. How many places in the blocks must you change, and what do you change in the controller builder?',
              answer='4 places: the name on the screen, the ID, the Subscribe topic and the Publish topic. In the controller builder you only change the robot name; the controller makes the <code>mr4/R4-T07/…</code> topics for you.')],
  quiz=[dict(q='The controller sends commands to the topic <code>mr4/R4-T01/cmd</code>. Which block does the robot need to receive them?', choices=['MQTT Subscribe mr4/R4-T01/cmd', 'MQTT Publish mr4/R4-T01/cmd', 'MQTT Connect with the ID set to mr4/R4-T01/cmd'],
             why='Subscribe = sign up to receive: the broker passes that topic’s messages on to you. Publish means sending out.'),
        dict(q='You put the When MQTT Message Received hat block below R4 Begin, as with Bluetooth. What happens?', choices=["It does not compile: 'mqttCallback' was not declared", 'It works normally', 'It uploads, but WiFi will not connect'],
             why='The code generator goes from top to bottom, and the <code>mqttCallback</code> function must come before <code>connectMQTT</code>.'),
        dict(q='After uploading, the light stays orange and never turns green. Which could be the cause?', choices=['The WiFi is 5 GHz, the password is wrong, or the network blocks port 1883', 'You forgot the hat block', 'You forgot MQTT Polling in Loop'],
             why='The light turns green only after WiFi and the broker connect. A missing hat block would not compile in the first place, and without Polling the light still turns green but no messages arrive.')])

L['u6-mqtt-drive'] = dict(
  title='Drive over MQTT with the same controller, and compare the delay with Bluetooth',
  goals=['Move the driving program from lesson 6.5 to MQTT by changing only the connection blocks', 'Set the fail-safe to 1000 ms to suit the internet, then compare the delay with Bluetooth'],
  intro='This lesson’s controller is the two sticks + arm from lesson 6.5 with <b>Connection</b> set to <b>Internet (MQTT)</b>. The messages are the same, so the robot uses the same logic. Only these change: BLE Polling → <b>MQTT Polling</b> · BLE Connected? → <b>MQTT Connected?</b> · '
        'Bluetooth hat → <b>When MQTT Message Received</b> · Received Data → <b>MQTT Received Message</b> · fail-safe 500 → <b>1000 ms</b>, because over the internet messages sometimes arrive late and sometimes early.',
  examples=[
    dict(title='Test the fail-safe over the internet with a light', desc='No wheels yet: hold the stick and the light is green; let go and after 1 second it turns red. Try switching off the hotspot while holding the stick: the light must turn red by itself.',
         notes=['For every message that comes in, remember the time in <code>last</code>, as in lesson 6.3.',
                'MQTT disconnected, or quiet for more than 1000 ms (while you hold the stick the controller sends every 100 ms) → treat the signal as lost']),
    dict(title='Two sticks + arm over the internet', desc='The blocks in the hat and in Loop are in the same order as in lesson 6.5. Only the connection blocks change to the MQTT ones, and 500 becomes 1000.',
         notes=['Splits the stick number as before, reading from <code>mqtt_rcvMessage</code> instead of <code>ble_rcvData</code>',
                'The same arm buttons',
                'Instead of <code>BLE.poll()</code>',
                'Instead of <code>!BLE.connected()</code> and 500',
                'Drives the wheels as before']),
  ],
  arduino=['The controller page connects to the same broker through <code>wss://broker.hivemq.com:8884/mqtt</code> (browsers use WebSocket on port 8884), while the robot uses port 1883, so the messages still reach each other.',
           'Why 1000 ms: messages travel phone → broker → robot over an internet shared with other people, so they do not arrive evenly. With 500 the robot may stop in jerks even while you are still holding the stick. The price: when the signal is really lost, the robot can keep going for up to 1 second.',
           'After you let go of the stick, the robot stops later than with Bluetooth. Keep the wheel power moderate, drive slowly in an open space, and leave room to brake.',
           'When the internet fades quietly (e.g. weak WiFi), <code>mqttClient.connected()</code> may take several seconds to notice, so timing 1000 ms of silence is still needed.',
           'This program connects to the broker only once, in Setup. If it disconnects, the robot stops and waits. Press reset on the board to connect again, or see Try it, task 2.'],
  tries=[dict(task='Compare the delay with Bluetooth: blue light while the wheels turn, off when stopped. Lift the robot so the wheels are in the air, push the stick and let go, and see how late the light goes off. Then do the same with the Bluetooth program from lesson 6.5. Which one stops later?',
              answer='MQTT usually stops noticeably later, because S has to pass through the broker before it reaches the robot. How much later depends on the internet at that moment.'),
         dict(task='Reconnect by itself: at the end of Loop, if MQTT is not connected, stop the wheels, make the light orange, then MQTT Connect and Subscribe again, and turn the light green when done.',
              answer='After reconnecting you must Subscribe again too (the broker forgets the topic when you disconnect), and stop the wheels first, because MQTT Connect waits until it is connected and Loop does not run meanwhile.')],
  quiz=[dict(q='Why does the MQTT fail-safe use 1000 ms while Bluetooth uses 500 ms?', choices=['Messages over the internet are slower and uneven; too short a time makes the robot stop in jerks while you still hold the stick', 'MQTT can only send one message per second', 'The board counts time more slowly when WiFi is on'],
             why='The controller still sends every 100 ms, but on the way through the broker some messages arrive with long gaps between them.'),
        dict(q='When you move the lesson 6.5 program to MQTT, must you change the part that splits the stick number?', choices=['No, just read from MQTT Received Message instead', 'Yes, the formula changes because MQTT sends numbers as bytes', 'Yes, it needs two topics, one for each wheel'],
             why='The controller sends the same messages whichever way it connects.'),
        dict(q='The robot is driving when the hotspot goes off. What makes it stop?', choices=['No message arrives for more than 1000 ms, so the fail-safe sets l and r to 0', 'mqttClient.loop() stops the wheels by itself', 'The board resets itself when WiFi is lost'],
             why='Moving at … never stops by itself, so you always need a fail-safe.')])

L['u6-wifi-server'] = dict(
  title='(Extra C++) The robot makes its own WiFi + a web page with 5 buttons',
  goals=['Make the robot create its own WiFi (AP mode) and act as a web server, with no internet needed', 'Read a request line such as GET /F and make the robot drive for 0.5 seconds'],
  intro='An extra lesson in <b>plain C++</b> (there are blocks to create WiFi, but no web server blocks). The robot sends out the WiFi <code>R4-T01</code> with the password <code>12345678</code>. The phone joins it and opens <code>192.168.4.1</code> to get a web page with the buttons ▲ ◀ ■ ▶ ▼. '
        'When you tap one, the page uses <code>fetch</code> to request an address such as <code>/F</code>. The robot reads the first line, <code>GET /F HTTP/1.1</code>, and drives for 0.5 seconds. No internet needed, and it works in every browser, including Safari on iPhone.',
  examples=[
    dict(title='The robot as a web server (whole file)',
         desc='Plain C++. You can copy the whole file into Arduino IDE with no extra libraries (WiFiS3 comes with the board). Change the WiFi name so it differs from the other teams’ before you upload.',
         notes=['The robot’s WiFi name, which must differ from every other team’s · <code>PASS</code> is the password, at least 8 characters',
                'A web server on port 80 = the normal port for http',
                'The web page in the variable <code>PAGE</code>: tap ▲ → <code>go(\'F\')</code> → asks the robot for <code>/F</code>',
                'The robot’s address = the WiFi Config IP block',
                'Turns on the robot’s WiFi (the WiFi Create AP block uses this command too). If it fails, the screen shows AP fail.',
                'Shows the address on the screen = the WiFi Device Local IP block',
                'A request has come in: read the first line',
                'Reads and throws away the other lines, up to the empty line',
                'Cuts out the second word: <code>a</code> = 4, cut up to the next space, giving <code>"/F"</code>',
                'Answers (the web page or OK) and closes first, then drives, so the web page does not have to wait',
                '■ brakes. If you press it while the robot is driving, it brakes after the 0.5-second move, because MoveSyncTime waits until the move is done.']),
  ],
  arduino=['Join the WiFi <code>R4-T01</code>, then type <code>192.168.4.1</code> (http, not https). Some phones warn that this WiFi has no internet: choose to stay connected. If the page does not load, try turning off mobile data for a while.',
           'If the screen shows <code>AP fail</code>, try another name or password (at least 8 characters), or update the wireless firmware: Tools → <b>Firmware Updater</b>',
           'While the phone is on the robot’s WiFi, it has no internet over WiFi. When you finish, switch back to your usual WiFi.',
           '<code>MoveSyncTime</code> waits until the move is finished, as in lesson 6.2, and the robot takes no new requests meanwhile. So it answers and calls <code>client.stop()</code> first, then drives.',
           'Comparing the three: <b>Bluetooth</b> needs no internet but needs Chrome/Bluefy · <b>MQTT</b> works at any distance but needs the internet and has more delay · <b>a web server in the robot</b> needs no internet and works in every browser, but you must stay within range of the robot’s WiFi'],
  tries=[dict(task='Add a horn button ♪ to the web page that calls <code>go(\'H\')</code>, and make the robot beep for 0.2 seconds when it gets <code>/H</code>.',
              answer='Change two places that go together: whatever the button asks for, the robot needs an if waiting for it, just like extra buttons in the controller builder.'),
         dict(task='Add a <code>V</code> button that asks for <code>/V</code>. The robot answers with the battery voltage, and the web page shows the robot’s answer under the buttons.',
              answer='The web page reads the answer with <code>r.text()</code> and writes it into <code>&lt;p id=\'o\'&gt;</code>. The other buttons show OK, so you know the robot got the request.')],
  quiz=[dict(q='You tap the ◀ button on the web page. What is the first line the robot reads?', choices=['GET /L HTTP/1.1', 'GET /F HTTP/1.1', 'L'],
             why='The ◀ button calls <code>go(\'L\')</code> → <code>fetch(\'/L\')</code>, and the browser sends a GET request to /L.'),
        dict(q='Why does the robot answer and call client.stop() before MoveSyncTime?', choices=['MoveSyncTime waits 0.5 seconds; answering after it would make the web page wait a long time', 'Driving first would not compile', 'client.stop() makes the robot drive faster'],
             why='Answer first, and the phone knows straight away that the robot got it.'),
        dict(q='Do you need the internet to use this lesson’s web page?', choices=['No, the phone joins the robot’s WiFi directly', 'Yes, because the messages go through the broker', 'Yes, because the web page loads from GitHub'],
             why='The robot is both the WiFi and the web server. The web page is inside the robot’s own code (<code>PAGE</code>).')])

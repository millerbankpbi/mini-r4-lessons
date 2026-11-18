# English text for the lessons (code snippets stay in lessons_src.py, only words are here)
UNITS = {
  1: dict(title='R4 Core · Movement · Looks', sub='Board, motors, driving, light, sound, screen'),
  2: dict(title='Sensing', sub='IMU · Grayscale · Potentiometer · Color V3 · Laser V2'),
  3: dict(title='Control', sub='Wait · If · Repeat · Timing'),
  4: dict(title='Operators · Variables', sub='Math · Compare · Variables · Text'),
  5: dict(title='My Blocks', sub='Make your own block = a function'),
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

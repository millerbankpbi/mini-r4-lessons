"""Tiny helpers to write MATRIXblock programs as Blockly XML (run later through the app's own generator)."""
from xml.sax.saxutils import escape


def N(v):
    return '<shadow type="math_number"><field name="NUM">%s</field></shadow>' % v


def T(s):
    return '<shadow type="text"><field name="TEXT">%s</field></shadow>' % escape(str(s))


def VAR(name):
    return '<block type="data_variable"><field name="VARIABLE" id="v_%s" variabletype="">%s</field></block>' % (name, name)


def chain(blocks):
    """Join statement blocks with <next>."""
    blocks = [b for b in blocks if b]
    if not blocks:
        return ''
    out = blocks[-1]
    for b in reversed(blocks[:-1]):
        assert b.endswith('</block>'), b[:60]
        out = b[:-len('</block>')] + '<next>' + out + '</next></block>'
    return out


def B(type_, f=None, v=None, s=None, var=None):
    """A block. f = fields, v = value inputs (shadow/block xml or plain number/text), s = statement lists."""
    parts = []
    if var:
        parts.append('<field name="VARIABLE" id="v_%s" variabletype="">%s</field>' % (var, var))
    for k, val in (f or {}).items():
        parts.append('<field name="%s">%s</field>' % (k, escape(str(val))))
    for k, val in (v or {}).items():
        if isinstance(val, (int, float)):
            val = N(val)
        elif isinstance(val, str) and not val.startswith('<'):
            val = T(val)
        parts.append('<value name="%s">%s</value>' % (k, val))
    for k, lst in (s or {}).items():
        parts.append('<statement name="%s">%s</statement>' % (k, chain(lst)))
    return '<block type="%s">%s</block>' % (type_, ''.join(parts))


def num_slot(inner):
    """Put a reporter into a number slot but keep a number shadow underneath (like dragging in the app)."""
    return inner


def P(setup=(), loop=(), aa='2', uart='1', baud='9600', extra=()):
    """A whole program: R4 Begin with Setup and Loop. extra = top-level hat blocks (full <block ...> xml), placed to the right.
    The generator emits top-level blocks in y order. BLE needs R4 Begin first (rxChar is declared by "UART enable"), but MQTT needs
    mqttCallback defined before connectMQTT, so an "on MQTT message" hat is placed above R4 Begin (R4 Begin goes below the hats)."""
    f = {'miniBegin_AA': aa, 'miniBegin_EnUART': uart, 'miniBegin_Baud': baud}
    main = B('mini_setup', f=f, s={'SUBSTACK': list(setup), 'SUBSTACK2': list(loop)}).replace('<block type="mini_setup">', '<block type="mini_setup" x="10" y="%d">' % (10 + len(extra) * 300 if any('mini_mqtt_on_message' in h for h in extra) else 10), 1)
    hats = ''.join(h.replace('<block ', '<block x="520" y="%d" ' % (10 + i * 300), 1) for i, h in enumerate(extra))
    return '<xml>' + main + hats + '</xml>'


# ---- frequently used blocks (all fields set explicitly: block defaults differ from the toolbox) ----
def wait(ms):
    return B('control_wait', v={'TIMES': ms})


def led(r, g, b, which=1):
    return B('mini_setRGB', f={'PIN': which}, v={'R': r, 'G': g, 'B': b})


def oled_print(text, x=0, y=0, show='Yes'):
    return B('mini_OLED_printEASY', f={'SHOW': show}, v={'TEXT': text, 'X': x, 'Y': y})


def oled_clear():
    return B('mini_OLED_clear')


def oled_size(n):
    return B('mini_OLED_setTextSize', v={'SIZE': n})


def drive_setup(l='M1', r='M2', lrev='false', rrev='true', settle='true'):
    return B('mini_ddc_setting', f={'PINL': l, 'PINR': r, 'PINL_REV': lrev, 'PINR_REV': rrev, 'BRAKE_SETTLE': settle})


def button(which='BTN_UP'):
    return B('mini_BTNget', f={'PIN': which})


def setvar(name, value):
    return B('data_setvariableto', var=name, v={'VALUE': value if isinstance(value, str) and value.startswith('<') else T(value)})


def changevar(name, by):
    return B('data_changevariableby', var=name, v={'VALUE': by if isinstance(by, str) and by.startswith('<') else N(by)})


def op(type_, a, b, names=('NUM1', 'NUM2')):
    return B(type_, v={names[0]: a, names[1]: b})


def cmp(type_, a, b):
    return B(type_, v={'OPERAND1': a, 'OPERAND2': b})


# ---- IoT: Bluetooth LE ----
def ble_setup(name='R4-T01'):
    """Blocks for Setup: BLE begin, set name, enable UART (needs ble_on_received as a hat in P(extra=...))."""
    return [B('mini_ble_begin'), B('mini_ble_set_name', v={'NAME': name}), B('mini_ble_uart_enable')]


def ble_poll():
    return B('mini_ble_poll')


def ble_connected():
    return B('mini_ble_connected')


def ble_send(v):
    return B('mini_ble_uart_send', v={'MESSAGE': v})


def ble_on_received(stmts):
    return B('mini_ble_on_received', s={'SUBSTACK': list(stmts)})


def ble_data():
    return B('mini_ble_received_data')


# ---- IoT: WiFi + MQTT ----
def wifi_connect(ssid, pw):
    return B('mini_wifi_connect', v={'SSID': ssid, 'PASSWORD': pw})


def mqtt_connect(client, broker='broker.hivemq.com', port=1883, user='', pw=''):
    return B('mini_mqtt_connect', v={'BROKER': broker, 'PORT': port, 'CLIENTID': client, 'USERNAME': user, 'PASSWORD': pw})


def mqtt_loop():
    return B('mini_mqtt_loop')


def mqtt_subscribe(topic, qos=0):
    return B('mini_mqtt_subscribe', f={'QOS': qos}, v={'TOPIC': topic})


def mqtt_publish(topic, v):
    return B('mini_mqtt_publish', v={'TOPIC': topic, 'MESSAGE': v})


def mqtt_on_message(stmts):
    return B('mini_mqtt_on_message', s={'SUBSTACK': list(stmts)})


def mqtt_msg():
    return B('mini_mqtt_received_message')


def mqtt_connected():
    return B('mini_mqtt_is_connected')


# ---- misc blocks used with remote control ----
def millis():
    return B('mini_millis')


def mathop(op_, v):
    return B('operator_mathop', f={'OPERATOR': op_}, v={'NUM': v})


def to_float(v):
    return B('operator_toFloat', v={'NUM': v})


def servo(port, angle):
    return B('mini_RCset', f={'PIN': port}, v={'Angle': angle})


def move_sync_time(l, r, secs, brake=True):
    return B('mini_ddc_runFor_sync', f={'UNIT': 'seconds', 'BrakeType': 'true' if brake else 'false'}, v={'NUM': secs, 'SPEEDL': l, 'SPEEDR': r})


def moving(l, r):
    return B('mini_ddc_on', v={'SPEEDL': l, 'SPEEDR': r})


def stop_moving(brake=True):
    return B('mini_ddc_off', f={'BrakeType': 'true' if brake else 'false'})

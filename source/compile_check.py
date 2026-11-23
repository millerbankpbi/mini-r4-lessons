"""Compile-only check of generated Arduino sketches (UNO R4 WiFi core + MatrixMiniR4, ArduinoBLE, PubSubClient)."""
import json
import os
import re
import shlex
import sys
from concurrent.futures import ProcessPoolExecutor
from subprocess import run

HERE = os.path.dirname(os.path.abspath(__file__))
CC = os.path.join(HERE, 'cc2')
EXTRA_INC = ['/home/claude/vendor/ArduinoBLE/src', '/home/claude/vendor/PubSubClient/src']


def _flags():
    toks = shlex.split(open('/home/claude/r4/build/cmd.txt').read())
    toks = toks[1:]  # drop compiler
    toks.remove('-c')
    # Arduino's bundled gcc 7 only warns on MatrixMiniR4.h's MiniR4I2C<-1,...>; gcc 13 errors, so relax it.
    return toks + ['-Wno-narrowing'] + ['-I' + p for p in EXTRA_INC]


def compile_code(name, code):
    """Compile one sketch (compile only, no link). Returns (ok, first error line or '')."""
    os.makedirs(CC, exist_ok=True)
    safe = re.sub(r'[^A-Za-z0-9_.-]', '_', name)
    src, obj = os.path.join(CC, safe + '.cpp'), os.path.join(CC, safe + '.o')
    with open(src, 'w') as f:
        f.write('#include <Arduino.h>\n' + code)
    r = run(['arm-none-eabi-g++', '-c'] + _flags() + [src, '-o', obj], capture_output=True, text=True)
    with open(os.path.join(CC, safe + '.log'), 'w') as f:
        f.write(r.stderr)
    if r.returncode == 0:
        return True, ''
    errs = [l for l in r.stderr.splitlines() if 'error' in l]
    return False, (errs[0] if errs else r.stderr.strip().splitlines()[0] if r.stderr.strip() else 'unknown error')


def _job(a):
    return a[0], compile_code(a[0], a[1])


def main(path):
    data = json.load(open(path))
    jobs = []
    for les in data['lessons']:
        for i, e in enumerate(les.get('examples', [])):
            jobs.append(('%s_ex%d' % (les['id'], i + 1), e['code']))
        for i, t in enumerate(les.get('tries', [])):
            jobs.append(('%s_try%d' % (les['id'], i + 1), t['code']))
    bad = 0
    with ProcessPoolExecutor(4) as ex:
        for name, (ok, err) in ex.map(_job, jobs):
            if not ok:
                bad += 1
                print('FAIL', name, err)
    print('%d/%d OK' % (len(jobs) - bad, len(jobs)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))

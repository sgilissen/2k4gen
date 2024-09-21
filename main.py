from flask import Flask, render_template, jsonify
import hashlib
import ctypes
import secrets


app = Flask(__name__)


def base_repr(number, base=2, padding=0):
    digits = '0123456789abcdefghijklmnopqrstuvwxyz'

    if base > len(digits):
        raise ValueError("Bases greater than 36 not handled in base_repr.")
    elif base < 2:
        raise ValueError("Bases less than 2 not handled in base_repr.")

    num = abs(number)
    res = []
    while num:
        res.append(digits[num % base])
        num //= base
    if padding:
        res.append('0' * padding)
    if number < 0:
        res.append('-')
    return ''.join(reversed(res or '0'))

def scramble(string):
    result = ''
    table = 'ABCDEFGHJLKMNPQRTUVWXYZ2346789'

    for ch in string:
        c = ord(ch)

        if 0x30 <= c <= 0x39:
            result += table[c - 0x30]
        elif 0x41 <= c <= 0x5A:
            result += table[c - 0x41 + 10]
        elif 0x61 <= c <= 0x7A:
            result += table[c - 0x61 + 10]
        else:
            result += '\0'

    return result

def generate_key():
    magic = 'appDebugfNoInit'
    seed = secrets.randbits(64)
    base = 30
    padch = 'A'

    seed30 = base_repr(ctypes.c_ulonglong(seed).value, base)
    key = scramble(seed30).rjust(14, padch)
    check_data = f'{ctypes.c_longlong(seed).value}{magic}'
    digest = hashlib.md5(check_data.encode('utf-8')).digest()

    # Convert to unsigned 64-bit integer
    qdigest = ctypes.c_ulonglong(int.from_bytes(digest[0:8], 'little')).value
    digest30 = base_repr(qdigest, base).rjust(6, padch)
    check = scramble(digest30)
    fullkey = f'{key}{check}'

    return f'{fullkey[10:15]}-{fullkey[5:10]}-{fullkey[0:5]}-{fullkey[15:20]}'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-uuid', methods=['GET'])
def get_uuid():
    key = generate_key()
    return jsonify({'uuid': key})



if __name__ == '__main__':
    app.run(debug=True)

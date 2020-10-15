import getpass
import sys
import random
import time
import keyboard
import bcrypt
import string
from cryptography.fernet import Fernet
import os.path
from os import path
from os import listdir
import subprocess
import tkinter as tk

#subprocess.check_call(['attrib','+H','key.key'])
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

#hiding key
'''ext = ['jpg', 'png', 'gif', 'bmp', 'raw', 'tiff', 'webp']
letters_digits = string.ascii_letters + string.digits

for i in range(1000):
    name = ''.join([random.choice(letters_digits) for i in range(random.randint(18,22))])
    #ext = ''.join([random.choice(letters_digits) for i in range(random.randint(2,4))])
    addrs = 'settings/' + name + '.' + random.choice(ext)
    f = open(addrs, 'wb')
    f.write(os.urandom(random.randint(500,800)))
    subprocess.check_call(['attrib', '+H', addrs])

    print('loading.. ' + str(i/10) + '%', end='\r')

f.close()


f = open('settings/' + listdir('settings')[f_index],'wb')
key = Fernet.generate_key()
f.write(key)
f.close()'''

f_index = str(time.time())[-4:-1]

print('done.           ')

#specifically chose not to use string lib for no particular reason
lower = 'abcdefghijklmnopqrstuvwxyz'
upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nums = '1234567890'
spcl = '`~!@#$%^&*()_-+={[}]|\<,>./?' #no quotes allowed
legal_chars = lower + upper + nums + spcl


password = 'hunter2'

key = Fernet.generate_key()
k = Fernet(key)
encrypted_pw = k.encrypt(password)

def encrypt_files():
    for i in listdir('files'):
        with open('files/' + i, 'rb') as f:
            data = f.read()
            e_data = k.encrypt(data)
        with open('files/' + i, 'wb') as f:
            f.write(e_data)

pw_location = 'SeCrypt.py:pw'

f = open(pw_location, 'wb')
f.write(encrypted_pw)
f.close()

key_location = 'SeCrypt.py:key'

f = open(key_location, 'wb')
f.write(key)
f.close()

print(encrypted_pw, key)

subprocess.check_call(['attrib', '+H', 'setup.py'])
subprocess.check_call(['attrib', '-H', 'SeCrypt.py'])

input('hit enter to exit. ')
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

def gen_key():
  key = Fernet.generate_key()
  hide_key(key)
  return key
  

def hide_key(key):
  for i in listdir('files'): #deletes all files in folder
    os.remove('files/' + i)

  ext = ['jpg', 'png', 'gif', 'bmp', 'raw', 'tiff', 'webp']
  letters_digits = string.ascii_letters + string.digits
  
  if len(listdir('files')) == 0:
    for i in range(1000):
      name = ''.join([random.choice(letters_digits) for i in range(random.randint(18,22))])
      addrs = 'settings/' + name + '.' + random.choice(ext)
      f = open(addrs, 'wb')
      f.write(os.urandom(random.randint(500,800)))
      subprocess.check_call(['attrib', '+H', addrs])

      print('loading.. ' + str(i/10) + '%', end='\r')

  f.close()

  def rand_char():
    return random.choice(string.ascii_letters + string.digits)

  r_string = rand_char().join(rand_char() for i in range(6))

  curr_time = time.time()
  f_index = (curr_time)[-4:-1]
  f = open(listdir('files')[f_index] + ':' + r_string, 'wb')
  f.write(key)
  f.close()

  f = open()

def encrypt(f_add: str, e: object):
  with open(f_add, 'rb') as f:
    data = f.read()
    e_data = e.encrypt(data)
  with open(f_add, 'wb') as f:
    f.write(e_data)

def decrypt(f_add: str, e: object):
  with open(f_add, 'rb') as f:
    data = f.read()
    e_data = e.decrypt(data)
  with open(f_add, 'wb') as f:
    f.write(e_data)

#decrypt(listdir('files'))
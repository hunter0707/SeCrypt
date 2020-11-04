import getpass
import sys
import random
import time
import keyboard
import bcrypt
import string
from cryptography.fernet import Fernet
from os import path
from os import listdir
import os
import subprocess

def gen_key():
  key = Fernet.generate_key()
  hide_key(key)
  return key

p = 0



def hide_key(key): #convoluted enough that i wouldn't know
  for i in listdir('settings'): #deletes all files in folder
    os.remove('settings/' + i)

  ext = ['jpg', 'png', 'gif', 'bmp', 'raw', 'tiff', 'webp']
  letters_digits = string.ascii_letters + string.digits
  
  ###
  if len(listdir('settings')) == 0:
    for i in range(1000):
      global p
      p = i
      name = ''.join([random.choice(letters_digits) for i in range(random.randint(18,22))])
      addrs = 'settings/' + name
      f = open(addrs, 'wb')
      f.write(os.urandom(random.randint(16,32)))
      subprocess.check_call(['attrib', '+H', addrs])

  f.close()
  ###

  ###
  def rand_char():
    return random.choice(string.ascii_letters + string.digits)

  r_list = [rand_char() for i in range(random.randint(20,28))]
  r_string = ''.join(r_list)

  curr_time = time.time()
  f_index = int((str(curr_time))[-4:-1])
  addrs = 'settings/' + listdir('settings')[f_index] + ':' + r_string
  f = open(addrs, 'wb')
  f.write(key)
  f.close()
  ###

  ###
  f = open('crypter.py:' + str(curr_time).split('.', -1)[1], 'wb')

  f.write((r_string * f_index + str(len(r_string))).encode())
  f.close()
  ###

  f = open('setup.py:info', 'wb')
  f.write((str(curr_time).split('.', -1)[1]).encode())
  f.close()

def fetch_key():
  f = open('setup.py:info', 'rb')
  time_str = f.read().decode()
  f.close()

  f = open('crypter.py:' + time_str, 'rb')
  long_str = f.read().decode()
  f.close()

  str_len = int(long_str[-2:])
  string_concat = len(long_str) - 2
  rptd_str = long_str[0:str_len]
  f_index = int(string_concat/str_len)

  f = open('settings/' + listdir('settings')[f_index] + ':' + rptd_str)
  key = f.read()
  f.close()

  return key

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
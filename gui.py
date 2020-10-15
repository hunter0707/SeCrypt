import string
import time
from tkinter import *
import keyboard
import random
import crypter as sec
from cryptography.fernet import Fernet
from os import listdir

class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.legal_chars = string.ascii_letters + string.digits + string.punctuation
        self.master = master
        self.match_status = ''
        self.setup()
        
        self.bars = [Button(text='         ', state='disabled', bg='white') for i in range(3)]
        self.bars[0].grid(sticky=W) #bar1 left
        self.bars[2].grid(sticky=E) #bar3 right, bar2 centered
        self.strength_meter()
        
    def setup(self):
        self.pw_confirmed = False
        self.master.title('Setup')

        Label(text='Password:').grid(row=0, columnspan=2)
        self.label_len = Label(text='- must be between 8 and 64 characters long')
        self.label_char = Label(text='- must contain at least 1 number and letter')
        self.label_spcl = Label(text='- can contain special characters')

        self.label_len.grid(row=1, columnspan=2)
        self.label_char.grid(row=2, columnspan=2)
        self.label_spcl.grid(row=3, columnspan=2)

        Label(text='Enter Password:').grid(column=0, row=4)
        Label(text='Confirm Password:').grid(column=0, row=5)
        
        self.pw_1 = Entry(show='*')
        self.pw_2 = Entry(show='*', state='disabled')

        self.pw_1.grid(column=1, row=4)
        self.pw_2.grid(column=1, row=5)

        self.confirm_pw_button = Button(text='Confirm Password', command=self.confirm_pw, state='disabled')
        self.confirm_pw_button.grid(column=1, row=6)

    def valid(self, pw):
        for i in pw:
            if i not in self.legal_chars:
                return False
        return True and len(pw) >= 8

    def secure(self, pw):
        letter = False
        digit = False

        for i in pw:
            if i in string.ascii_letters:
                letter = True
            if i.isdigit():
                digit = True

        return letter and digit and 8 <= len(pw) <= 64

    def strength_meter(self):
        def strength_check(pw):

            upper = 0
            lower = 0
            digit = 0
            special = 0

            if len(pw) >= 12:
                length = 1
            else:
                length = 0

            reqs = [upper, lower, digit, length, special]

            for i in pw:
                if i.isupper():
                    upper = 1
                elif i.islower():
                    lower = 1
                elif i.isdigit():
                    digit = 1
                else:
                    special = 1

            reqs = [upper, lower, digit, length, special]

            if sum(reqs) == 5:
                return '  strong  '
            elif 2 <= sum(reqs) <= 4 and len(pw) >= 10:
                return '  medium  '
            elif len(pw) != 0:
                return '   weak   '
            else:
                return '             '

        for i in self.bars:
            i.grid(column=0, row=6)

        pw = self.pw_1.get()
        strength = strength_check(pw)

        if 'weak' in strength: #first 1 red
            self.bars[0].configure(bg='red')
            self.bars[1].configure(bg='white')
            self.bars[2].configure(bg='white')
        elif 'medium' in strength: #first 2 yellow
            self.bars[0].configure(bg='yellow') 
            self.bars[1].configure(bg='yellow')
            self.bars[2].configure(bg='white')
        elif 'strong' in strength: #all green
            for i in self.bars:
                i.configure(bg='green')
        else: #nothing, all white
            for i in self.bars:
                i.configure(bg='white')

        Label(text=strength).grid(column=0, row=7)

        root.after(100, self.strength_meter)
        root.after(100, self.pw_status)

    def confirm_pw(self):
        self.pw_1.configure(state='disabled')
        self.pw_2.configure(state='disabled')
        self.confirm_pw_button.configure(text='Encrypt', command=self.encrypt)

    def pw_status(self):
        pw_1 = self.pw_1.get()
        pw_2 = self.pw_2.get()

        if self.secure(pw_1) and self.valid(pw_1):
            self.pw_2.configure(state='normal')
            if pw_1 == pw_2:
                self.confirm_pw_button.configure(state='normal')

        if 8 <= len(pw_1) <= 64:
            leng_c = 'green'
        else:
            leng_c = 'black'

        letter = False
        digit = False

        for i in pw_1:
            if i not in string.ascii_letters and i not in string.digits:
                spcl_c = 'green'
            elif i in string.ascii_letters:
                letter = True
            elif i in string.digits:
                digit = True

        try:
            if spcl_c != 'green':
                spcl_c = 'black'
        except:
            spcl_c = 'black'
        
        if letter and digit:
            char_c = 'green'
        else:
            char_c = 'black'

        self.label_char.configure(fg=char_c)
        self.label_len.configure(fg=leng_c)
        self.label_spcl.configure(fg=spcl_c)

    def encrypt(self):
        pw_key = sec.gen_key()
        fl_key = sec.gen_key()

        f_encrypt = Fernet(fl_key)

        for i in listdir('files'):
            sec.encrypt('files' + i, f_encrypt)

root = Tk()
app = Window(root)
root.minsize(250,160)

root.mainloop()
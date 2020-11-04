import string
import sys
import time
from tkinter import *
import random
import crypter as sec
from cryptography.fernet import Fernet
from os import listdir
import subprocess

class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.legal_chars = string.ascii_letters + string.digits + string.punctuation
        self.master = master
        self.match_status = ''
        self.setup()
        
        self.bars = [Button(text='         ', state='disabled', bg='white') for i in range(3)]
        self.bars[0].grid(sticky=W) #bar1 left, for password strength
        self.bars[2].grid(sticky=E) #bar3 right, bar2 centered
        self.strength_meter()
        self.v_time = 60
        
    def setup(self):
        self.pw_confirmed = False
        self.master.title('Setup')

        self.label_pw = Label(text='Password:')
        self.label_pw.grid(row=0, columnspan=2)

        self.label_len = Label(text='- must be between 6 and 64 characters long')
        self.label_char = Label(text='- must contain at least 1 number and letter')
        self.label_spcl = Label(text='- can contain special characters')

        self.label_len.grid(row=1, columnspan=2)
        self.label_char.grid(row=2, columnspan=2)
        self.label_spcl.grid(row=3, columnspan=2)

        Label(text='Enter Password:').grid(column=0, row=4)
        Label(text='Confirm Password:').grid(column=0, row=5)
        
        self.pw1 = Entry(show='*')
        self.pw2 = Entry(show='*', state='disabled')

        self.pw1.grid(column=1, row=4)
        self.pw2.grid(column=1, row=5)

        self.confirm_pw_button = Button(text=' Confirm ', command=self.confirm_pw, state='disabled')
        self.confirm_pw_button.grid(column=1, row=6, sticky='E')

        self.cancel_button = Button(text='    Reset    ', command=self.setup) #sticky='W' once confirmed
        self.view_button = Button(text='    View    ', command=self.view, state='disabled')
        self.randomize_button = Button(text='Randomize', command=self.randomize)

        self.cancel_button.grid(column=1, row=7, sticky='W')
        self.randomize_button.grid(column=1, row=6, sticky='W')
        self.view_button.grid(column=1, row=7, sticky='E')

    def randomize(self):
        pw = ''
        while True:
            for i in range(16):
                pw += random.choice(self.legal_chars)
            if self.secure(pw):
                #enables entry boxes and empties them before inserting
                self.pw1.configure(state='normal')
                self.pw1.delete(0, END)
                self.pw1.insert(END, pw)

                self.pw2.configure(state='normal')
                self.pw2.delete(0, END)
                self.pw2.insert(END, pw)

                self.view()
                self.randomize_button.configure(state='disabled')

                break #pw is secure
            else:
                pw = ''
            
    def view(self):
        v_time = self.v_time
        pw = self.pw1.get()

        pw_view = Toplevel(master=None) #opens new window that shows password and counts down
        pw_view.title('password')
        pw_view.geometry('180x60')
        pw_view.minsize(180,60)
        pw_view.maxsize(180,60)


        Label(pw_view, text='Your password is').pack()
        Label(pw_view, text=pw).pack()
        time_left = Label(pw_view, text=str(v_time))
        time_left.pack()

        def t_minus():
            elapsed = time.time() - start_time
            if elapsed > v_time: #time has elapsed
                pw_view.destroy()
            time_left.configure(text=str(round(v_time - elapsed, 1)) + ' seconds left to view.')
            root.after(100, t_minus)

        start_time = time.time()

        root.after(100, t_minus)
        
    def valid(self, pw): #check validity of password
        for i in pw:
            if i not in self.legal_chars:
                return False
        return True and len(pw) >= 6

    @staticmethod
    def secure(pw): #checks security of password
        letter = False
        digit = False

        for i in pw:
            if i in string.ascii_letters:
                letter = True
            if i.isdigit():
                digit = True

        return letter and digit and 6 <= len(pw) <= 64

    def strength_meter(self): #displays strength of password
        def strength_check(pw):

            upper = 0
            lower = 0
            digit = 0
            special = 0

            if len(pw) >= 10:
                length = 1
            else:
                length = 0

            for i in pw:
                if i.isupper():
                    upper = 1
                elif i.islower():
                    lower = 1
                elif i.isdigit():
                    digit = 1
                else:
                    special = 1

            reqs = [upper, lower, digit, length, special] #5 different requirements: 1 if met, 0 if not met

            if sum(reqs) == 5 or sum(reqs) == 4 and len(pw) > 12: #all met is strong
                return '  strong  '
            elif 2 <= sum(reqs) <= 4 and len(pw) > 8: #some met is medium
                return '  medium  '
            elif len(pw) != 0: #one met is weak
                return '   weak   '
            else: #nothingness
                return '             '

        for i in self.bars: #places the deactivated buttons
            i.grid(column=0, row=6)

        pw = self.pw1.get()
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

    def confirm_pw(self): #locks basically everything
        self.pw1.configure(state='disabled')
        self.pw2.configure(state='disabled')
        self.confirm_pw_button.configure(text='    Lock    ', command=self.lock, bg='red')
        self.randomize_button.configure(state='disabled')
        self.view_button.configure(state='disabled')

    def pw_status(self):
        pw1 = self.pw1.get()
        pw2 = self.pw2.get()

        if self.secure(pw1) and self.valid(pw1):
            if len(pw2) != 0: #disable 1 once 2nd starts filling
                self.pw1.configure(state='disabled')
            if pw1 == pw2: #disable both entries, places cancel button
                self.view_button.configure(state='normal')
                self.pw1.configure(state='disabled')
                self.pw2.configure(state='disabled')
                self.confirm_pw_button.configure(state='normal')
            else: #not equivalent, cannot use confirm, 2 is open
                self.pw2.configure(state='normal')
                self.view_button.configure(state='disabled')
                self.confirm_pw_button.configure(state='disabled')
        else:
            self.view_button.configure(state='disabled')
            self.confirm_pw_button.configure(state='disabled')
            self.pw1.configure(state='normal')
            self.pw2.configure(state='disabled')
            self.pw2.insert(END, '')

        if 6 <= len(pw1) <= 64: #len req met
            leng_c = 'green'
        elif len(pw1) > 64:
            leng_c = 'red'
        else:
            leng_c = 'black'

        letter = False
        digit = False

        for i in pw1:
            if i not in string.ascii_letters and i not in string.digits: #spcl char
                spcl_c = 'green'
            elif i in string.ascii_letters:
                letter = True
            elif i in string.digits:
                digit = True

        try:
            if spcl_c not in ('green', 'red'):
                spcl_c = 'black'
        except:
            spcl_c = 'black'
        
        if letter and digit:
            char_c = 'green'
        else:
            char_c = 'black'

        #color of label text
        self.label_char.configure(fg=char_c)
        self.label_len.configure(fg=leng_c)
        self.label_spcl.configure(fg=spcl_c)
        
    def lock(self):
        self.label_pw.configure(text='                                                                             ')
        self.label_len.configure(text='                                                                             ')
        self.label_char.configure(text='   Locking.. This may take a while...   ')
        self.label_spcl.configure(text='                                                                             ')

        buttons = [self.cancel_button, self.view_button, self.confirm_pw_button, self.randomize_button]
        
        for i in buttons: #disable buttons
            i.configure(state='disabled')

        def delayed():
            key = sec.gen_key()
            f_encrypt = Fernet(key)

            for i in listdir('files'): #encrypt all files w/ my function
                sec.encrypt('files/' + i, f_encrypt)

            pw = self.pw1.get().encode()
            pw = f_encrypt.encrypt(pw) #encyrpted pw

            f = open('unlock.py:eKey', 'wb')
            f.write(pw)
            f.close()

            #hides and unhides
            subprocess.check_call(['attrib', '+H', 'setup.py']) 
            subprocess.check_call(['attrib', '-H', 'unlock.py'])

            self.label_char.configure(text='                              Success!                              ')

            def Exit():
                sys.exit()

            root.after(3000, Exit) #bye

        root.after(50, delayed)

root = Tk()
app = Window(root)
root.minsize(250,180)
root.maxsize(250,180)
root.mainloop()
import string
import sys
import time
from tkinter import Frame, Entry, Button, Label, Tk
from tkinter.filedialog import askopenfilename
import random
import crypter as sec
from cryptography.fernet import Fernet
from os import listdir, remove
import subprocess

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('')
        self.u_entry = Entry(show='*')
        self.unlock_button = Button(text='unlock', command=self.unlock)
        self.enter = Label(text='Enter Password:')
        self.status = Label(text='')


        self.enter.pack()
        self.u_entry.pack()
        self.unlock_button.pack()
        self.status.pack()

    @staticmethod
    def reset():
        for i in listdir('settings'):
            remove('settings/' + i)
        subprocess.check_call(['attrib', '-H', 'setup.py'])
        subprocess.check_call(['attrib', '+H', 'unlock.py'])

    def unlock(self):
        hkey = sec.fetch_key()
        entered = self.u_entry.get().encode()
        with open('unlock.py:ekey', 'rb') as f:
            ekey = f.read()

        if entered == Fernet(hkey).decrypt(ekey):
            self.status.configure(text='Success! Unlocking..', fg='green')
            
            def de():
                for i in listdir('files'):  
                    sec.decrypt('files/' + i, Fernet(hkey))

            root.after(100, de)

            self.status.configure(text='Unlocked successfully!')
            self.reset()

            def Exit():
                sys.exit()

            root.after(3000, Exit) #bye
        else:
            self.status.configure(text='Password incorrect.', fg='red')

root = Tk()
app = Window(root)
root.minsize(180, 90)
root.maxsize(180, 90)
root.mainloop()
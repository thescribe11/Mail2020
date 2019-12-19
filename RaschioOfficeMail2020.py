import time
import tkinter as tk
import smtplib, imaplib
from email.message import EmailMessage
import justext as js
from tkinter import ttk
from imap_tools import MailBox
#import pygubu  # Here just in case I need it at some point. Remove if unnecessary when production stage is reached.

class MainWindow(tk.Tk):

    def __init__(self, title="BoaConstrictor", icon=None, management="default", *args, **kwargs):

        tk.Tk.__init__(self)
        
        try:
            self.title(title)
        except:
            raise ValueError(f"I am afraid that a {title.type()} can not be used as a title.")

        if icon != None:
            if icon[-4:] == ".gif":
                try:
                    with open(icon, r) as f:
                        content = f.read()
                    image = tk.PhotoImage(data=content)
                    self.tk.call('wm', 'iconphoto', self._w, image)
                except:
                    raise ValueError("Excuse me, but you have sent in the wrong type of photo for the window icon.")
            
            else:
                try:
                    image = tk.PhotoImage(data=content)
                    self.tk.call('wm', 'iconphoto', self._w, image)
                
                except:
                    raise ValueError("Excuse me, but this image simply doesn't make sense.")
        
        if management != "default":  # Take care of custom window management.
            self.overrideredirect(True)
        
        return None
        

    def run(self):
        self.mainloop()

    def kill(self, killcode = 0):
        if killcode != 0:
            print("*** ERROR! ERROR! EXTERMINATING WINDOW! ***")
            self.destroy()

########################
#### The MainUI.   #####
########################
class MainUI(MainWindow):
    '''The main user interface. Inherits from the MainWindow class of my upcoming BoaConstrictor module.'''
    def __init__(self):
        '''Basic setup.'''
        MainWindow.__init__(self, title="Raschio Office Mail 2020")

        new_image = tk.PhotoImage(file="C:\\Users\\Adam\\AppData\\Local\\Programs\\Python\\Python38\\new.png")

        self.new_button = tk.Button(self, text="", image=new_image, borderwidth="2px", command=self.NewMessage)
        self.new_button.grid(padx=30, pady=30)

        self.run()

    def NewMessage(self, *args):
        pass

if __name__ == "__main__":
    MainUI()

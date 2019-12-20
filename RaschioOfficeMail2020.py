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

    def kill(self, *args, killcode = 0):
        if killcode != 0:
            print("*** ERROR! ERROR! EXTERMINATING WINDOW! ***")
            self.destroy()


class Message(tk.Frame):
    def __init__(self, master, sender: str, subject: str, content: str):
        if len(subject) > 30:
            subject = subject[:30]
            subject = subject + "..."
        text = f"From: {sender}   Re: {subject}   " # Do not delete the whitespace; its necessary.

        tk.Frame.__init__(self, bg="#b7b3b0")

        self.checked = tk.IntVar()
        self.checker = tk.Checkbutton(self, var=self.checked, bg="#b7b3b0", relief="flat", borderwidth=0, offrelief="flat")
        self.checker.grid(padx=5)

        self.main = tk.Button(self, text=text, bg="#b7b3b0", font="Times 14", command = self.open_message(), relief="flat")
        self.main.grid(column=1, row=0)

    def grid_it(self, row, column):
        self.grid(row=row, column=column, pady=4, padx=5, sticky="we")
        return None

    def open_message(self, *args):
        pass
    

########################
#### The MainUI.   #####
########################
class MainUI(MainWindow):
    '''The main user interface. Inherits from the MainWindow class of my upcoming BoaConstrictor module.'''
    displayed_messages = dict()
    def __init__(self):
        '''Basic setup.'''
        MainWindow.__init__(self, title="Raschio Office Mail 2020")
        self.withdraw()

        # Image assets to be used by various widgets.
        new_image = tk.PhotoImage(file="new.png")
        delete_image = tk.PhotoImage(file="delete.png")
        move_image = tk.PhotoImage(file="move.png")

        # Button for drafting an e-mail.
        self.new_button = tk.Button(self, text="", image=new_image, borderwidth="2px", command=self.NewMessage)
        self.new_button.grid(row=1, column=0, padx=15)

        '''
        E-mail management buttons.
        '''    
        self.options_frame = tk.Frame(self)
        self.options_frame.grid(row=0, column=1, pady=(0, 20))

        self.delete_button = tk.Button(self.options_frame, image=delete_image, borderwidth="1px", command=self.delete_selected)
        self.delete_button.grid(row=0, column=0, padx=(50, 10))

        self.move_button = tk.Button(self.options_frame, image=move_image, borderwidth="1px", command=self.move_selected)
        self.move_button.grid(row=0, column=1, padx=(20, 10))

        '''
        Actual mail display.
        '''
        self.mail_frame = tk.Frame(self)  # Frame containing instances of Message().

        self.mail_frame.grid(row=2, column=1)

        '''# Get the messages.'''
        self.InitLogin()
        self.SetupMessages()
        self.deiconify()

        '''On your marks, get set, GO!!!'''
        self.run()

    '''
    #######################
    # Processing methods. #
    #######################
    '''

    def SetupMessages(self, *args, **kwargs):
        messages = self.mailbox.fetch(limit=50)
        self.root.destroy()

    def NewMessage(self, *args):
        print("I am making a new message.")

    def delete_selected(self, *args):
        print("EXTERMINATE! EXTERMINATE!")

    def move_selected(self, *args):
        print("Moving...")

    def killer(self, *args):
        self.root.destroy()
        self.destroy()

    def InitLogin(self):
        self.root = tk.Toplevel(self)
        self.root.protocol("WM_DELETE_WINDOW", self.killer)
        self.MainFrame = tk.Frame(self.root)
        self.MainFrame.grid(padx=30, pady=30)
        self.ver_label = tk.Label(self.MainFrame, font="Times 10")
        self.ver_label.grid(pady=5)
        user_label = tk.Label(self.MainFrame, text="Username", font="Times 15")
        user_label.grid()
        self.user_entry = tk.Entry(self.MainFrame, font="Times 12")
        self.user_entry.grid(pady=(10, 20))

        pass_label = tk.Label(self.MainFrame, text="Password", font="Times 15")
        pass_label.grid()
        self.pass_entry = tk.Entry(self.MainFrame, font="Times 12", show="*")
        self.pass_entry.grid(pady=(10,20))

        EntryImage = tk.PhotoImage(file="signin.png")
        submit = tk.Button(self.MainFrame, image=EntryImage, command=self.LogIn)
        self.root.bind("<Return>", self.LogIn)
        submit.grid(pady=20)
        
        self.root.mainloop()

    def LogIn(self, *args) -> int:
        username = self.user_entry.get()
        password = self.pass_entry.get()
        
        if "@" not in username:
            username += "@gmail.com"
        
        self.mailbox = MailBox('imap.gmail.com')
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        try:    
            self.mailbox.login(username, password, initial_folder='INBOX')
            self.server.login(username, password)
        except:
            self.ver_label['text'] = "*Wrong E-mail or Password."
            return
        
        self.root.destroy()
        del self.root
        self.root = tk.Toplevel()
        self.root.protocol("WM_DELETE_WINDOW", self.killer)
        self.frames = [tk.PhotoImage(file = 'DalekShootingMail.gif', format = 'gif -index %i' % (i)) for i in range(38)]
        self.imager = tk.Label(self.root)
        self.imager.grid()
        self.root.after(0, self.updater, 0)
        return 0

    def updater(self, index, *args):
        frame = self.frames[index]
        if index < 37:
            index += 1
        else:
            index = 0
        self.imager.configure(image=frame)
        self.imager.update()
        self.root.after(30, self.updater, index)


if __name__ == "__main__":
    MainUI()

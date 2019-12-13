import tkinter as tk
import pygubu
import time
import re

TASK_BUFFER = dict()

class MainWindow(tk.Tk):
    def __init__(self, typer = "default", title="BoaConstrictor", *args, **kwargs):
        tk.Tk.__init__(self)
        self.title(title)
        self.bind("<Unmap>", self.onRootIconify)
        self.bind("<Map>", self.onRootDeiconify)
        self.top = tk.Toplevel(self)
        self.attributes("-alpha", 0.0)
        self.top.geometry("+800+300")
        if typer == "custom":
            self.top.overrideredirect(True)
        else:
            self.overrideredirect(True)
        self.protocol('WM_DELETE_WINDOW', self.good_bye_1)
        self.top.protocol('WM_DELETE_WINDOW', self.good_bye_2)
    
    def good_bye_1(self, *args):
        self.top.destroy()

    def good_bye_2(self, *args):
        self.destroy()

    def onRootIconify(self, *args, **kwargs):
        self.top.withdraw()

    def onRootDeiconify(self, *args, **kwargs):
        self.top.deiconify()

def mainwindow(title, typer = "default"):
    MW = MainWindow(typer = typer, title=title)
    return MW.top

class Application:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('C:\\Users\\Adam\\AppData\\Local\\Programs\\Python\\Python38\\timer.ui')

        self.mainwindow = builder.get_object('MainFrame', master)
        callbacks = {
            'start_cmd': self.start
        }
        
        builder.connect_callbacks(callbacks)

    def start(self, *args):
        '''Start the timer. '''
        what = str(self.builder.tkvariables.__getitem__('CurrentTask').get())
        seconds = int(self.builder.tkvariables.__getitem__('Seconds').get())
        minutes = int(self.builder.tkvariables.__getitem__('Minutes').get())
        hours = int(self.builder.tkvariables.__getitem__('Hours').get())
        
        #################################################
        ## TODO: Make logic to insert 0 if ''.
        #################################################
        buffer = 0



        print(buffer)

if __name__ == "__main__":
    root = mainwindow("Raschio Timer")
    app = Application(root)
    
    root.mainloop()
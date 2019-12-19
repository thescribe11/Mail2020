import tkinter as tk
import pygubu
import time
import re
from gtts import gTTS as gtts
import sched
import threading
import tempfile
from pygame import mixer

ID = 0

class Timer(threading.Thread):
    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.name, self.how_long = name, counter

    def run(self):
        global root
        print("Starting " + self.name)
        time.sleep(self.how_long)
        print("Timer is done.")
        top = tk.Toplevel(root)
        top.title("Jarvis")

    def speak(self, audioString):
        print(audioString)
        tts = gtts(text=audioString, lang='en')
        temp = tempfile.TemporaryFile(mode="w+r")
        tts.save(temp)
        mixer.init()
        mixer.music.load(temp)
        mixer.music.play()


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

    def start(self, *args) -> None:
        '''Start the timer. '''
        global ID
        what = str(self.builder.tkvariables.__getitem__('CurrentTask').get())
        seconds = str(self.builder.tkvariables.__getitem__('Seconds').get())
        minutes = str(self.builder.tkvariables.__getitem__('Minutes').get())
        hours = str(self.builder.tkvariables.__getitem__('Hours').get())
        buffer = 0

        if seconds == '':
            seconds = 0

        if minutes == '':
            minutes = 0
        else:
            minutes = minutes * 60
        
        if hours == '':
            hours = 0
        else:
            hours = hours * 3600

        exec(f'self.thread{ID} = Timer(what, buffer); self.thread{ID}.start()')
        

if __name__ == "__main__":
    root = mainwindow("Raschio Timer")
    app = Application(root)
    
    root.mainloop()
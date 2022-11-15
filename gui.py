from tkinter import *


class GUI(object):

    def __init__(self):
        self._mainFont = ('Arial', 20)
        self._smallerFont = ('Arial', 15)


        self._root = Tk()
        self._root.title("Electric Vehicle")
        
        self._socLabel = Label(self._root, text='Charge: 100%', width=30, height=4, bg='grey', fg='green', font=self._mainFont)
        self._socLabel.grid(row=0, column=0)

        self._rangeLabel = Label(self._root, text='Distance on current charge:\n 100km', width=30, height=4, bg='white', fg='orange', font=self._mainFont)
        self._rangeLabel.grid(row=0, column=1)

        self._powerMode = Label(self._root, text='Normal Mode', width=44, height=3, bg='white', fg='orange', font=self._smallerFont)
        self._powerMode.grid(row=1, column=0)

        self._modeBG = Label(self._root, text='', width=44, height=3, bg='white', fg='orange', font=self._smallerFont)
        self._modeBG.grid(row=2, column=0)

        self._switchMode = Button(self._root, command=self.switchLowPowerMode, text="Switch Mode", width=10, height=3, bd='02', bg='white', fg='orange')
        self._switchMode.grid(row=2, column=0)

        self._warningsLabel = Label(self._root, text='Warnings', width=44, height=3, bg='grey', fg='green', font=self._smallerFont)
        self._warningsLabel.grid(row=1, column=1)
        
        self._warnings = Label(self._root, text='No Warnings', width=44, height=3, bg='grey', fg='green', font=self._smallerFont)
        self._warnings.grid(row=2, column=1)

        self._root.mainloop()

    def switchLowPowerMode(self):
        print("Switching Power Mode...")
        if self._powerMode.cget("text") == 'Low Power Mode':
            self._powerMode.config(text='Normal Mode')
        else: self._powerMode.config(text='Low Power Mode')

    def reportWarning(self, warning):
        self._warningsList.append(warning)
        if self._warnings.cget("text") == "No Warnings":
            self._warnings.config(text=warning)
        else:
            self._warnings.config(text="You have %s urgent warnings" % len(self._warningsList))

    def clearWarning(self, warning):
        self._warningsList.remove(warning)
        if len(self._warningsList) == 0:
            self._warnings.config(text="No Warnings")
        elif len(self._warningsList) == 1:
            self._warnings.config(text=self._warningsList[0])
        else:
            self._warnings.config(text="You have %s urgent warnings" % len(self._warningsList))

if __name__ == "__main__":
    gui = Gui()
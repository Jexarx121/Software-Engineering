from tkinter import *

class Gui(object):

    def __init__(self):
        self._root = Tk()
        self._root.title("Electric Vehicle")

        self._canvas = Canvas(self._root, bg="black", height=400, width=600)
        self._canvas.grid(row=3, column=5)
        
        self._leftSide = Frame(self._root)
        self._socLabel = Label(self._leftSide, text='Charge: 100%').grid(row=0, column=0)
        self._ecoMode = Button(self._root, text="Eco Mode", width=10, height=3,
         bd='02', bg='black', fg='green').grid(row=1, column=0)

        self._root.mainloop()

if __name__ == "__main__":
    gui = Gui()

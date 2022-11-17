from tkinter import *
from tkinter import ttk

class UI():

    def __init__(self):

        self._background = "#2e2e2e"
        self._percentLabel = ""

        self._root = Tk()
        self._root.title("Eco Mode")
        self._root.geometry("500x500")
        self._root.configure(bg=self._background)
        self._root.resizable(False, False)

        # Create the left and right frames
        self._leftFrame = Frame(self._root, bg=self._background, highlightbackground="white", highlightthickness=1, width=100, height=500)
        self._leftFrame.grid(row=0, column=0, sticky="nsew")
        self._rightFrame = Frame(self._root, bg=self._background, width=400, height=500)
        self._rightFrame.grid(row=0, column=1, sticky="nsew")

        # Create the left frame widgets
        self._onOffButton = Button(self._leftFrame, text="Turn On/Off", bg=self._background, fg="white", width=10, height=2)
        self._onOffButton.grid(row=0, column=0, padx=10, pady=10)
        self._ecoModeButton = Button(self._leftFrame, text="Eco Mode", bg=self._background, fg="white", width=10, height=2)
        self._ecoModeButton.grid(row=1, column=0, padx=10, pady=10)
        self._settingsButton = Button(self._leftFrame, text="Settings", bg=self._background, fg="white", width=10, height=2)
        self._settingsButton.grid(row=2, column=0, padx=10, pady=10)

        # Create the right frame widgets
        self._batteryPercentLabel = Label(self._rightFrame, text=self._percentLabel, bg=self._background, fg="white")
        self._batteryPercentLabel.grid(row=0, column=0, padx=10, pady=10)
        self._batteryPercentProgress = ttk.Progressbar(self._rightFrame, orient=HORIZONTAL, length=200, mode="determinate")
        self._batteryPercentProgress.grid(row=0, column=0, padx=10, pady=10)
        self._distanceRemainingLabel = Label(self._rightFrame, text="Distance Remaining", bg=self._background, fg="white")
        self._distanceRemainingLabel.grid(row=1, column=0, padx=10, pady=10) 

        self.getData()


    def progressBar(self, stateOfCharge):
        self._batteryPercentProgress['value'] = stateOfCharge
        self._percentLabel = f"Current Percentage: {self._batteryPercentProgress['value']}"

    def getData(self):
        self._root.mainloop()


if __name__ == "__main__":
    ui = UI()

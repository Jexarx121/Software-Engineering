from tkinter import *
from tkinter import ttk
from bms import BatteryManagementSystem

class UI():
    def __init__(self, bms):

        self._background = "#2e2e2e"
        self._font = ('Times New Roman', 20)
        self._warningFont = ('Times New Roman', 16)

        self._root = Tk()
        self._root.title("Eco Mode")
        self._root.geometry("700x400")
        self._root.configure(bg=self._background)
        self._root.resizable(False, False)

        # Create the left and right frames
        self._leftFrame = Frame(self._root, bg=self._background, width=100, height=400)
        self._leftFrame.grid(row=0, column=0, sticky="nsew")
        self._rightFrame = Frame(self._root, bg=self._background, width=600, height=400)
        self._rightFrame.grid(row=0, column=1, sticky="nsew")

        # Create the left frame widgets
        self._settingsButton = Button(self._leftFrame, text="Settings", bg=self._background, fg="white", width=10, height=2)
        self._settingsButton.grid(row=0, rowspan=2, column=0, padx=10, pady=10)

        # Create the right frame widgets
        self._batteryPercentProgress = ttk.Progressbar(self._rightFrame, orient=HORIZONTAL, length=200, mode="determinate")
        self._batteryPercentProgress.grid(row=0, column=1, padx=10, pady=10)
        self._batteryPercentLabel = Label(self._rightFrame, text=self.progressSocBar(bms.stateOfCharge), bg=self._background, fg="white", font=self._font)
        self._batteryPercentLabel.grid(row=0, column=0, padx=10, pady=10)
        self._distanceRemainingLabel = Label(self._rightFrame, text="Distance Remaining (est):", bg=self._background, fg="white", font=self._font)
        self._distanceRemainingLabel.grid(row=1, column=0, padx=10, pady=10) 
        self._distanceRemaining = Label(self._rightFrame, text=self.updateDistanceRemaining(bms.distanceRemaining), bg=self._background, fg="white", font=self._font)
        self._distanceRemaining.grid(row=1, column=1, padx=10, pady=10)

        # Warnings that appear below the buttons and labels
        self._socWarning = Label(self._root, text=self.displaySocWarnings(bms), bg=self._background, fg="yellow", font=self._warningFont)
        self._socWarning.grid(row=1, column=0, columnspan=2, sticky="sw", padx=20, pady=10)
        self._sohWarning = Label(self._root, text=self.displaySohWarnings(bms), bg=self._background, fg="red", font=self._warningFont)
        self._sohWarning.grid(row=2, column=0, columnspan=2, sticky="sw", padx=20, pady=10)

        self._root.mainloop()


    def displaySohWarnings(self, bms):
        return bms.stateOfHealthWarning()

    def displaySocWarnings(self, bms):
        return bms.stateOfChargeWarning()

    def updateDistanceRemaining(self, distanceRemaining):
        return f"{distanceRemaining}km"

    def progressSocBar(self, stateOfCharge):
        self._batteryPercentProgress['value'] = stateOfCharge
        return f"Current Percentage: {self._batteryPercentProgress['value']}%"
        

if __name__ == "__main__":
    pass

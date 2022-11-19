from tkinter import *
from tkinter import ttk
from bms import BatteryManagementSystem

class UI():
    def __init__(self, bms):

        self._background = "#2e2e2e"
        self._font = ('Times New Roman', 20)
        self._warningFont = ('Times New Roman', 16)
        self._toggle = True

        self._root = Tk()
        self._root.title("Infobtainment Screen")
        self._root.geometry("700x400")
        self._root.configure(bg=self._background)
        self._root.resizable(False, False)

        # Create the left and right frames
        self._leftFrame = Frame(self._root, bg=self._background, width=100, height=400)
        self._leftFrame.grid(row=0, column=0, sticky="nsew")
        self._rightFrame = Frame(self._root, bg=self._background, width=600, height=400)
        self._rightFrame.grid(row=0, column=1, sticky="nsew")

        # Create the right frame widgets
        # SOC text and progress bar
        self._batteryPercentProgress = ttk.Progressbar(self._rightFrame, orient=HORIZONTAL, length=200, mode="determinate")
        self._batteryPercentProgress.grid(row=0, column=1, padx=10, pady=10)
        self._batteryPercentLabel = Label(self._rightFrame, text=self.progressSocBar(bms.stateOfCharge)[0], bg=self._background, fg=self.progressSocBar(bms.stateOfCharge)[1], font=self._font)
        self._batteryPercentLabel.grid(row=0, column=0, padx=10, pady=10)

        # SOH text and progress bar
        self._healthPercentProgress = ttk.Progressbar(self._rightFrame, orient=HORIZONTAL, length=200, mode="determinate")
        self._healthPercentProgress.grid(row=1, column=1, padx=10, pady=10)
        self._healthPercentLabel = Label(self._rightFrame, text=self.progressSohBar(bms.stateOfHealth)[0], bg=self._background, fg=self.progressSohBar(bms.stateOfHealth)[1], font=self._font)
        self._healthPercentLabel.grid(row=1, column=0, padx=10, pady=10)

        # distance remaining text
        self._distanceRemainingLabel = Label(self._rightFrame, text="Distance Remaining (est):", bg=self._background, fg="white", font=self._font)
        self._distanceRemainingLabel.grid(row=2, column=0, padx=10, pady=10) 
        self._distanceRemaining = Label(self._rightFrame, text=self.updateDistanceRemaining(bms.distanceRemaining), bg=self._background, fg="white", font=self._font)
        self._distanceRemaining.grid(row=2, column=1, padx=10, pady=10)

        # total mileage of vehicle text
        self._totalMileageLabel = Label(self._rightFrame, text="Total Mileage (km): ", bg=self._background, fg="white", font=self._font)
        self._totalMileageLabel.grid(row=3, column=0, padx=10, pady=10)
        self._totalMileage = Label(self._rightFrame, text=self.displayMileage(bms), bg=self._background, fg="white", font=self._font)
        self._totalMileage.grid(row=3, column=1, padx=10, pady=10)

        # Create the left frame widgets
        self._mileageButton = Button(self._leftFrame, text="Show Mileage", bg=self._background, fg="white", width=10, height=2, command=self.showMileage)
        self._mileageButton.grid(row=0, rowspan=2, column=0, padx=10, pady=10)

        # Warnings that appear below the buttons and labels
        self._lowPowerModeLabel = Label(self._root, text="", bg=self._background, fg="limegreen", font=self._warningFont)
        self._lowPowerModeLabel.grid(row=1, column=0, columnspan=2, sticky="sw", padx=20, pady=10)
        self._socWarning = Label(self._root, text=self.displaySocWarnings(bms), bg=self._background, fg="yellow", font=self._warningFont)
        self._socWarning.grid(row=2, column=0, columnspan=2, sticky="sw", padx=20, pady=10)
        self._sohWarning = Label(self._root, text=self.displaySohWarnings(bms), bg=self._background, fg="red", font=self._warningFont)
        self._sohWarning.grid(row=3, column=0, columnspan=2, sticky="sw", padx=20, pady=10)

        self._root.mainloop()

    
    def exit(self):
        self._root.destroy()


    def showMileage(self):
        self._toggle = not self._toggle

        if self._toggle == True:
            self._totalMileageLabel.grid_forget()
            self._totalMileage.grid_forget()
        else:
            self._totalMileageLabel.grid()
            self._totalMileage.grid(row=3, column=1, padx=10, pady=10) 

    def displayMileage(self, bms):
        return bms.odometer.mileage

    def displaySohWarnings(self, bms):
        return bms.stateOfHealthWarning()
        
    def displaySocWarnings(self, bms):
        return bms.stateOfChargeWarning()

    def updateDistanceRemaining(self, distanceRemaining):
        return f"{distanceRemaining}km"

    def progressSocBar(self, stateOfCharge):
        self._batteryPercentProgress['value'] = stateOfCharge
        color = self.textColorBasedOnPercentage(stateOfCharge)
        return f"Charge Remaining: {self._batteryPercentProgress['value']}%", color


    def progressSohBar(self, stateOfHealth):
        self._healthPercentProgress['value'] = stateOfHealth
        color = self.textColorBasedOnPercentage(stateOfHealth)
        return f"Health Status: {self._healthPercentProgress['value']}%", color

    def textColorBasedOnPercentage(self, value):
        if value >= 70:
            color = "limegreen"
        elif value >= 25:
            color = "yellow"
        else:
            color = "red"

        return color

    def getLowPowerModeLabel(self):
        return self._lowPowerModeLabel

    lowPowerModeLabel = property(getLowPowerModeLabel)
        

if __name__ == "__main__":
    pass

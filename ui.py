from tkinter import *
from tkinter import ttk
from time import sleep

class UI():
    def __init__(self):
        
        height = 500
        width = 700
        self._background = "#2e2e2e"
        self._font = ('Times New Roman', 20)
        self._warningFont = ('Times New Roman', 16)
        self._toggle = False

        self._root = Tk()
        self._root.title("Infobtainment Screen")
        self._root.geometry(f"{width}x{height}")
        self._root.configure(bg=self._background)
        self._root.resizable(False, False)

        self._bigFrame = Frame(self._root, bg=self._background, width=width, height=height)
        self._bigFrame.grid(row=0, column=0, sticky="nsew")

        # Create the left and right frames
        self._leftFrame = Frame(self._bigFrame, bg=self._background, width=width/7, height=height)
        self._leftFrame.grid(row=0, column=0, sticky="nsew")
        self._rightFrame = Frame(self._bigFrame, bg=self._background, width=(width/7)*6, height=height)
        self._rightFrame.grid(row=0, column=1, sticky="nsew")

        # Create the right frame widgets
        # SOC text and progress bar
        self._batteryPercentProgress = ttk.Progressbar(self._rightFrame, orient=HORIZONTAL, length=200, mode="determinate")
        self._batteryPercentProgress.grid(row=0, column=1, padx=10, pady=10)
        self._batteryPercentLabel = Label(self._rightFrame, text=75, bg=self._background, fg="yellow", font=self._font)
        self._batteryPercentLabel.grid(row=0, column=0, padx=10, pady=10)

        # SOH text and progress bar
        self._healthPercentProgress = ttk.Progressbar(self._rightFrame, orient=HORIZONTAL, length=200, mode="determinate")
        self._healthPercentProgress.grid(row=1, column=1, padx=10, pady=10)
        self._healthPercentLabel = Label(self._rightFrame, text=0, bg=self._background, fg="white", font=self._font)
        self._healthPercentLabel.grid(row=1, column=0, padx=10, pady=10)

        # distance remaining text
        self._distanceRemainingLabel = Label(self._rightFrame, text="Distance Remaining (est):", bg=self._background, fg="white", font=self._font)
        self._distanceRemainingLabel.grid(row=2, column=0, padx=10, pady=10) 
        self._distanceRemaining = Label(self._rightFrame, text=0, bg=self._background, fg="white", font=self._font)
        self._distanceRemaining.grid(row=2, column=1, padx=10, pady=10)

        # total mileage of vehicle text
        self._totalMileageLabel = Label(self._rightFrame, text="Total Mileage (km): ", bg=self._background, fg="white", font=self._font)
        self._totalMileageLabel.grid(row=3, column=0, padx=10, pady=10)
        self._totalMileage = Label(self._rightFrame, text=0, bg=self._background, fg="white", font=self._font)
        self._totalMileage.grid(row=3, column=1, padx=10, pady=10)

        # Create the left frame widgets
        self._mileageButton = Button(self._leftFrame, text="Show Mileage", bg=self._background, fg="white", width=10, height=2, command=self.showList)
        self._mileageButton.grid(row=0, rowspan=2, column=0, padx=10, pady=10)

        # Warnings that appear below the buttons and labels
        self._lowPowerModeLabel = Label(self._root, text="", bg=self._background, fg="limegreen", font=self._warningFont)
        self._lowPowerModeLabel.grid(row=1, column=0, columnspan=2, sticky="sw", padx=20, pady=10)
        self._socWarning = Label(self._root, text="Test", bg=self._background, fg="yellow", font=self._warningFont)
        self._socWarning.grid(row=2, column=0, columnspan=2, sticky="sw", padx=20, pady=10)
        self._sohWarning = Label(self._root, text="Test", bg=self._background, fg="red", font=self._warningFont)
        self._sohWarning.grid(row=3, column=0, columnspan=2, sticky="sw", padx=20, pady=10)

        self._vehicleOffLabel = Label(self._root, text="", fg="white", bg=self._background, font=self._warningFont)
        self._vehicleOffLabel.grid(row=4, column=0, columnspan=2, sticky="sw", padx=20, pady=10)

        self._chargeLabel = Label(self._root, text="", fg="yellow", bg=self._background, font=self._warningFont)
        self._chargeLabel.grid(row=5, column=0, columnspan=2, sticky="sw", padx=20, pady=10)

        self._root.update()


    def exit(self):
        self._vehicleOffLabel['text'] = "Vehicle is shutting down."
        sleep(1)
        self._root.destroy()


    def showList(self):
        self._toggle = not self._toggle

        if self._toggle:
            self._totalMileageLabel.grid_forget()
            self._totalMileage.grid_forget()
        else:
            self._totalMileageLabel.grid()
            self._totalMileage.grid(row=3, column=1, padx=10, pady=10) 



if __name__ == "__main__":
    pass
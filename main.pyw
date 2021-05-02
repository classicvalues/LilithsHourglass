import time
import os
from playsound import playsound
import tkinter
import tkinter.ttk
import threading

#Constant variables
height = 400
width = 400

#Pomodoro factory
class Pomodoro:
	'''
	Pomodoro class that takes settings used for pomodoros (pomodoro time, break time, long break time)
	'''
	def __init__(self, name, minutes, minutes_break, minutes_break_long):
		self.name = name
		self.minutes = minutes
		self.minutes_break = minutes_break
		self.minutes_break_long = minutes_break_long
		self.__overSixtyCheck()

	def showSettings(self):
		return f"your current settings are:\nminutes: {self.minutes}\nbreak: {self.minutes_break}\nlong break: {self.minutes_break_long}"
	
	def __overSixtyCheck(self):
		if self.minutes > 60:
			self.overSixty = True
		else:
			self.overSixty = False


#Pomodoro settings
pomodoroDefault = Pomodoro("Default", 25, 5, 30) # pomodoro minutes = 25 / pomodoro break = 5 / pomodoro break long = 30
pomodoroDouble = Pomodoro("Double", 50, 10, 60)
pomodoroUltradian = Pomodoro("Ultradian", 90, 20, 110)
pomodoroTest = Pomodoro("Test", 0.01, 0.01, 0.01)

#Quality of life variables
pomodoro_count = 0
isBreak = False
stop = False

#System functions
def play(sound):
	'''
	Function that makes the sound when pomodoros and breaks are started or finished
	'''
	soundFilePath=''
	
	if sound == "pomodoro":
		soundFilePath ="sounds/finish.wav" #pomodoro sound
	elif sound == "break":
		soundFilePath = "sounds/bfinish.wav" #break sound
	elif sound == "pStart":
		soundFilePath = "sounds/start.wav" #pomodoro start sound
	elif sound == "bStart":
		soundFilePath = "sounds/bstart.wav" #break start sound
	
	playsound(soundFilePath, False)

#Pomodoro functions
def clock(pomo):
	'''
	Clock function that takes settings and makes a pomodoro according to the given settings
	'''
	global isBreak
	global pomodoro_count
	minutes = 0
	
	if isBreak:
		if pomodoro_count == 4:
			minutes = pomo.minutes_break_long
		else:
			minutes = pomo.minutes_break
		play("bStart")
	else:
		minutes = pomo.minutes
		play("pStart")

	time_start = time.perf_counter()
	
	while True:
		time_diff = int(round(time.perf_counter()-time_start))
		time_left = minutes*60-time_diff
		if time_left <= 0:
			break

		if stop:
			resetClock()
			break

		showTime(time_left)
		time.sleep(1)
	
	if stop:
		pass
	else:
		if isBreak:
			play("break")
			if pomodoro_count == 4:
				pomodoro_count = 0
				updateNotifications("You've finished your long break!")
			else:
				pomodoro_count+=1
				lblPomodorosLeft.config(text=f"Pomodoros left for long break: {4-pomodoro_count}")
				updateNotifications("You've finished your break!")
			isBreak = False
		else:
			play("pomodoro")
			updateNotifications("You've finished your pomodoro!")
			isBreak = True
	
	global btnStart
	global lblCurrentState
	btnStart["state"] = "active"
	btnPomodoroChange["state"] = "active"
	lblCurrentState.config(text=f"Currently on a break? {isBreak}")

def showTime(time_left):
	global selectedPomodoro
	'''
	Function that updates a label to show time left
	'''
	time_left-=1
	if selectedPomodoro.overSixty:
		time_converted=time.strftime("%H:%M:%S", time.gmtime(time_left))
	else:
		time_converted=time.strftime("%M:%S", time.gmtime(time_left))
	updateTime(time_converted)

def startClock():
	'''
	Function that starts the clock function on a different thread
	'''
	global stop
	if stop != False:
		stop = False

	threading.Thread(target=clock, args=(selectedPomodoro,)).start()
	global btnStart
	btnStart["state"] = "disabled"
	btnPomodoroChange["state"] = "disabled"

def stopClock():
	'''
	Function that changes variable stop and so makes the clock function stop and close its thread
	'''
	global stop
	stop = True

def resetClock():
	'''
	Function that resets time in lblTimeLeft
	'''
	if selectedPomodoro.overSixty:
		updateTime(time.strftime('%H:%M:%S', time.gmtime(selectedPomodoro.minutes*60)))
	else:
		updateTime(time.strftime('%M:%S', time.gmtime(selectedPomodoro.minutes*60)))

def updateNotifications(notification):
	'''
	Function that updates notifications label
	'''
	lblNotifications.config(text=f"{notification}")

def updateTime(time):
	'''
	Function that updates lblTimeLeft with the data that has been given to it
	'''
	lblTimeLeft.config(text=f"{time}")

def pomoSwitch():
	'''
	Function that cycles through pomodoro settings
	'''
	global selectedPomodoro
	if selectedPomodoro == pomodoroDefault:
		selectedPomodoro = pomodoroDouble
	elif selectedPomodoro == pomodoroDouble:
		selectedPomodoro = pomodoroUltradian
	elif selectedPomodoro == pomodoroUltradian:
		selectedPomodoro = pomodoroDefault
	btnPomodoroChange.config(text=f"{selectedPomodoro.name}")

	resetClock()

#Program start functions
selectedPomodoro = pomodoroTest

#GUI
window = tkinter.Tk()

#Window Settings
window.title("Lilith's Hourglass")
window.geometry(f"{width}x{height}")
window.maxsize(width, height)
window.minsize(width, height)

#Icon Settings
icon = tkinter.PhotoImage(file = "Icon/sandclock.png")
window.iconphoto(False, icon)

#GUI Widgets
#Widget Creation
#Label
lblCurrentState = tkinter.Label(window, text=f"Currently on a break? {isBreak}")
lblTimeLeft = tkinter.Label(window, text=f"{time.strftime('%M:%S', time.gmtime(selectedPomodoro.minutes*60))}", font=("Calibri", 30))
lblPomodorosLeft = tkinter.Label(window, text=f"Time left for long break: {4-pomodoro_count}")
lblNotifications = tkinter.Label(window, text="")

#Button
btnStart = tkinter.ttk.Button(window, text="Start", command=startClock)
btnStop = tkinter.ttk.Button(window, text="Stop", command=stopClock)
btnPomodoroChange = tkinter.ttk.Button(window, text=f"{selectedPomodoro.name}", command=pomoSwitch)

#Widget Placement
#Label
lblTimeLeft.grid(row=0, column=0, columnspan=2)
lblCurrentState.grid(row=3, column=0, columnspan=2)
lblPomodorosLeft.grid(row=4, column=0, columnspan=2)
lblNotifications.grid(row=5, column=0, columnspan=2)

#Button
btnStart.grid(row=1, column=0, padx=31, ipadx=31)
btnStop.grid(row=1, column=1, padx=31, ipadx=31)
btnPomodoroChange.grid(row=2, column=0, columnspan=2, ipadx=131)


window.mainloop()
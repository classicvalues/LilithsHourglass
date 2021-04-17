import time
import os
from playsound import playsound
import tkinter

#Constant variables
height = 400
width = 400

#Pomodoro settings
pomodoro_minutes=25
pomodoro_break=5
pomodoro_break_long=30
pomodoro_count=0
isBreak=False
pomo_or_break="pomodoro"

#System functions
def play(sound):
	soundFilePath=''
	
	if sound=="pomodoro":
		soundFilePath="sounds/finish.wav" #pomodoro sound
	elif sound=="break":
		soundFilePath="sounds/bfinish.wav" #break sound
	elif sound=="pStart":
		soundFilePath="sounds/start.wav" #pomodoro start sound
	elif sound=="bStart":
		soundFilePath="sounds/bstart.wav" #break start sound
	
	playsound(soundFilePath, False)

clear=lambda: os.system('cls')
#if UNIX use clear instead of cls

#Pomodoro functions
def clock():
	global isBreak
	global pomodoro_count
	minutes = 0
	
	if isBreak:
		if pomodoro_count == 4:
			minutes=pomodoro_break_long
		else:
			minutes=pomodoro_break	
		play("bStart")
	else:
		minutes=pomodoro_minutes
		play("pStart")

	time_start=time.perf_counter()
	
	while True:
		time_diff=int(round(time.perf_counter()-time_start))
		time_left=minutes*60-time_diff
		if time_left <= 0:
			print('')
			break

		showTime(time_left)
		time.sleep(1)
	
	if isBreak:
		play("break")
		if pomodoro_count==4:
			pomodoro_count=0
			print("You've finished your long break!")
		else:
			pomodoro_count+=1
			print("You've finished your break!")
		isBreak=False
	else:
		play("pomodoro")
		print("You've finished your pomodoro!")
		isBreak=True

def showTime(time_left):
	time_left-=1
	time_converted=time.strftime("%M:%S", time.gmtime(time_left))
	print(f"Time left: {time_converted}\r", end="\r")

#Program start functions
clear() #To have a clean console at the start

#GUI
window = tkinter.Tk()

#Window Settings
window.geometry(f"{width}x{height}")
window.maxsize(width, height)
window.minsize(width, height)

#GUI Widgets
#Widget Creation
lblCurrentState = tkinter.Label(window, text=f"Currently on a break? {isBreak}")

#Widget Placement
lblCurrentState.grid(row=0, column=0)

window.mainloop()
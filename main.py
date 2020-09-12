import time
import os
from playsound import playsound

#Constant variables


#Pomodoro settings
pomodoro_minutes=25
pomodoro_break=5
pomodoro_break_long=30
pomodoro_count=0
isBreak=False
pomo_or_break="pomodoro"

#System functions
def play(sound):
	if sound=="pomodoro":
		playsound("sounds/finish.wav")
	elif sound=="break":
		playsound("sounds/bfinish.wav")
	elif sound=="pStart":
		playsound("sounds/start.wav")
	elif sound=="bStart":
		playsound("sounds/bstart.wav")

clear=lambda: os.system('cls')
#if UNIX use clear instead of cls

#Database functions


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

#UI
clear()
while True:
	print(f"Pomodoros left for long break: {4-pomodoro_count}")
	if isBreak:
		pomo_or_break="break"
	else:
		pomo_or_break="pomodoro"
	option=input(f"1. Start {pomo_or_break}\n\nPress 0 to exit program\n")
	clear()

	if option=='0':
		break

	elif option=="1":
		clock()

	else:
		print(f'"{option}" is not an option')
		print("Press Enter to exit.")
		input()

print("Press enter to exit")
input()
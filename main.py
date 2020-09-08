import time

def clock(minutes):
	time_start=time.perf_counter()
	
	while True:
		time_diff=int(round(time.perf_counter()-time_start))
		time_left=minutes*60-time_diff
		if time_left <= 0:
			print('Pomodoro Finished')
			break

		showTime(time_left)
		time.sleep(1)

def showTime(time_left):
	time_converted=time.strftime("%M:%S", time.gmtime(time_left))
	print(f"Time left: {time_converted}\r", end="\r")
import time

def clock(minutes):
	time_start=time.perf_counter()
	
	while True:
		time_diff=int(round(time.perf_counter()-time_start))
		time_left=minutes*60-time_diff
		if time_left <= 0:
			print('Pomodoro Finished')
			break

		time.sleep(1)
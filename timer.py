import Brisk
import time

times = []
SAMPLE_SIZE = 1
POLL_TIME = 1 # seconds
for i in xrange(SAMPLE_SIZE):
	b = Brisk.Brisk()
	start = time.time()
	while not b.get_game_state()['winner']:
		time.sleep(POLL_TIME)
	end = time.time()
	times.append(end - start)
print times

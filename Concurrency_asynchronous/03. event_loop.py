import time


class Timer:
    def __init__(self, timeout):
        self.timeout = timeout
        self.start = time.time()
        self.callback = None

    def done(self):
        return time.time() - self.start > self.timeout

    def on_timer_done(self, callback):
        self.callback = callback


# timer = Timer(2.0)
# while True:  # busy-waiting
#     if timer.done():
#         print('Timer is done!')
#         break

# timer = Timer(2.0)
# timer.on_timer_done(lambda: print("Timer is done!"))
# while True:  # busy-waiting
#     if timer.done():
#         timer.callback()
#         break

timers = []
timer1 = Timer(1.0)
timer1.on_timer_done(lambda: print('First timer is done!'))
timer2 = Timer(2.0)
timer2.on_timer_done(lambda: print('Second timer is done!'))

timers.append(timer1)
timers.append(timer2)

while True:
    for timer in timers:
        if timer.done():
            timer.callback()
            timers.remove(timer)
    if len(timers) == 0:
        break

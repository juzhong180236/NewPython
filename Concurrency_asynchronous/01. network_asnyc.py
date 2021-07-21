import time
import threading


def network_request(number):
    time.sleep(1.0)
    return {'success': True, 'result': number * 2}


def fetch_square(number):
    response = network_request(number)
    if response['success']:
        print('Result is: {}'.format(response['result']))


def network_request_async(number, _on_done):
    def timer_done():
        _on_done({'success': True,
                  'result': number * 2})

    timer = threading.Timer(1.0, timer_done)
    timer.start()


def on_done(result):
    print(result)


def fetch_square_async(number):
    def _on_done(response):
        if response['success']:
            print('Result is: {}'.format(response['result']))

    network_request_async(number, _on_done)


network_request_async(2, on_done)
network_request_async(3, on_done)
network_request_async(4, on_done)
print('After Submission 1')
fetch_square_async(2)
fetch_square_async(3)
fetch_square_async(4)
print('After Submission 2')

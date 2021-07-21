import time
import threading
from concurrent.futures import Future


# fut = Future()
# fut.add_done_callback(lambda f: print(f.result()))
# print(fut)
# fut.set_result("hello")
# print(fut)


# print(fut.result())


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


def network_request_async_future(number):
    future = Future()
    result = {'success': True, 'result': number * 2}
    timer = threading.Timer(1.0, lambda: future.set_result(result))
    timer.start()
    return future


def fetch_square_async_future(number):
    _fut = network_request_async_future(number)

    def _on_done_future(_future):
        _response = _future.result()
        if _response['success']:
            print('Result is: {}'.format(_response['result']))

    _fut.add_done_callback(_on_done_future)


fetch_square_async_future(2)
# network_request_async(2, on_done)
# network_request_async(3, on_done)
# network_request_async(4, on_done)
# print('After Submission 1')
# fetch_square_async(2)
# fetch_square_async(3)
# fetch_square_async(4)
# print('After Submission 2')

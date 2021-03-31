from eventpy.callbacklist import CallbackList
from eventpy.eventdispatcher import EventDispatcher

# create a CallbackList
callbackList = CallbackList()
# Add a callback.
# Lambda is not required, any function or callable object is fine
callbackList.append(lambda: print("Got callback 1."))


def anotherCallback():
    print("Got callback 2.")


callbackList.append(anotherCallback)
# Invoke the callback list
callbackList()

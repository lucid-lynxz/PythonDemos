import threading

name = threading.current_thread().getName()
print("thread name ", name)

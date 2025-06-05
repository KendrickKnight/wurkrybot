from threading import Thread 
from reporter import main as reporter
from discbot import main as discbot

thread_a = Thread(target=reporter)
thread_b = Thread(target=discbot)

thread_a.start()
thread_b.start()

thread_a.join()
thread_b.join()

from functools import wraps
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal


class Worker(QtCore.QThread):
    started = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, target, *args, **kwargs):
        super().__init__()
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self.started.connect(self.before)
        self.finished.connect(self.after)

    def run(self):
        self.started.emit()
        self._target(*self._args, **self._kwargs)
        self.finished.emit()

    def before(self):
        print("Starting")

    def after(self):
        print("Finished")
        self.quit()


def multi_thread_runner(func):
    @wraps(func)
    def async_func(*args, **kwargs):
        worker = Worker(func, *args, **kwargs)
        func.__worker = worker
        worker.start()
    return async_func

from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot, QThread


# class Worker(QThread):
#
#     def __init__(self, task, args):
#         super(Worker, self).__init__()
#         self.task = task
#         self.args = args
#
#     def run(self):
#         self.task(self.args)
#
#

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Worker(QObject):

    resultReady = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @pyqtSlot(str)
    def doWork(self, param):
        result = "hello world"
        print("foo bar")
        # ...here is the expensive or blocking operation... #
        self.resultReady.emit(result)


class Controller(QObject):

    operate = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. Create 'workerThread' and 'worker' objects
        # ----------------------------------------------
        self.workerThread = QThread()
        self.worker = Worker()          # <- SEE NOTE(1)
        self.worker.moveToThread(self.workerThread)

        # 2. Connect all relevant signals
        # --------------------------------
        self.workerThread.finished.connect(self.worker.deleteLater)
        self.workerThread.finished.connect(lambda: print("workerThread finished."))  # <- SEE NOTE(2)
        self.operate.connect(self.worker.doWork)
        self.worker.resultReady.connect(self.handleResults)

        # 3. Start the thread
        # --------------------
        self.workerThread.start()

    def __del__(self):
        self.workerThread.quit()
        self.workerThread.wait()

    @pyqtSlot(str)
    def handleResults(self, param):
        print(param)
        # One way to end application
        # ---------------------------
        # global app      # <- SEE
        # app.exit()      #     NOTE(3)

        # Another way to end application
        # -------------------------------
        self.workerThread.quit()   # <- SEE NOTE(4)
        self.thread().quit()

#
# if __name__ == '__main__':
#     app = QCoreApplication([])
#     controller = Controller()
#     controller.operate.emit("foo")      # <- SEE NOTE(5)
#     sys.exit(app.exec_())

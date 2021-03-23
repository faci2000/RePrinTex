import sys

from PyQt5.QtWidgets import QApplication

from views.main_window import MainWindow

# TODO:
#  - save, save all, save as (tak sobie napisałam, żeby zobaczyć jak to wyjdzie, trzeba ogarnąć co nam jest potrzebne)
#  - jakie pola na menubar i ich rozwinięcia
#  - teraz zrobiłam tak, że jak się kliknie jeszcze raz open, to usuwa to co było poprzednio, nwm czy chcemy tak, czy
#  chcemy dopisywać te nowe czy rozdzielić na dwie opcje np. Open files i Add files


if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    sys.exit(app.exec_())

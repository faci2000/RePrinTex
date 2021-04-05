from views.main_window import MainWindow
import sys
from PyQt5.QtWidgets import QApplication

# Main dla całej aplikacji, poza startem aplikacji w sumie raczej nic nie powinien robić, tak mi się wydaje

# TODO:
#  - przeniesienie tego dock1 do guielements
#  - dodanie klas obrazu i kolekcji obrazów -> zastosowanie ich do tej listy(później )
#  - resize obrazów przy resize okna, nwm czy do tego nie trzeba będzie z centralWidget zrobić kontenera a potem dopiero Qlabel
#  - resize obrazka na wejscie
#  - zoom
#  - save, save all, save as (tak sobie napisałam, żeby zobaczyć jak to wyjdzie, trzeba ogarnąć co nam jest potrzebne)
#  - jakie pola na menubar i ich rozwinięcia
#  - jeśli chcemy obrazki jako podgląd plików
#  - ogólnie nie wiem narazie co my tu chcemy jeszcze mieć oprócz menubar i podglądu wszystkich plików
#  - teraz zrobiłam tak, że jak się kliknie jeszcze raz open, to usuwa to co było poprzednio, nwm czy chcemy tak, czy
#  chcemy dopisywać te nowe czy rozdzielić na dwie opcje np. Open files i Add files


if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    sys.exit(app.exec_())


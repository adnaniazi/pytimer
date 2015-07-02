__authors___ = 'Nisar Ahmad, Jahenzeb Khan, and Adnan Niazi'

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import winsound
from my_gui import Ui_MainWindow

class MyMainGui(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainGui, self).__init__(parent)
        self.setupUi(self)
        app.setStyle(QStyleFactory.create('Plastique'))

        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.display('00:00:00')
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.do_countdown)

        self.toolButton_start.setDisabled(True)
        self.toolButton_pause.setDisabled(True)
        self.toolButton_reset.setDisabled(True)

        self.spinBox_hours.valueChanged.connect(self.update_lcd)
        self.spinBox_minutes.valueChanged.connect(self.update_lcd)
        self.spinBox_seconds.valueChanged.connect(self.update_lcd)

        self.toolButton_start.clicked.connect(self.start_timer)
        self.toolButton_pause.clicked.connect(self.pause_timer)
        self.toolButton_reset.clicked.connect(self.reset_timer)

        self.paused = False

    def reset_timer(self):
        """Stop the timer and initializes the display to values in spinboxes"""

        self.toolButton_reset.setDisabled(True)
        self.toolButton_pause.setDisabled(True)
        self.toolButton_start.setEnabled(True)
        self.update_lcd()
        self.timer.stop()
        self.paused = False

    def pause_timer(self):
        """Stops the timer which is equivalent to pause"""

        self.toolButton_pause.setDisabled(True)
        self.toolButton_start.setEnabled(True)
        self.timer.stop()
        self.paused = True

    def start_timer(self):
        """Start the timer if user has specified some time in the spin boxes"""
        if not self.paused:
            # Only get values from spinboxes if paused button hasn't been pressed
            self.hours = self.spinBox_hours.value()
            self.minutes = self.spinBox_minutes.value()
            self.seconds = self.spinBox_seconds.value()

        if not (self.hours == 0 and self.minutes == 0 and self.seconds == 0):
            self.timer.start(1000)
            self.toolButton_pause.setDisabled(False)
            self.toolButton_start.setDisabled(True)
            self.toolButton_reset.setDisabled(False)

    def do_countdown(self):
        """Logic for decrementing hours, minutes, and seconds every tick"""

        self.toolButton_pause.setEnabled(True)
        self.toolButton_reset.setEnabled(True)

        self.hours = int(self.hours)
        self.minutes = int(self.minutes)
        self.seconds = int(self.seconds)

        if self.minutes > 0 and self.seconds == 0:
            self.minutes = self.minutes - 1
            self.seconds = 60

        if self.hours > 0 and self.minutes == 0:
            self.hours = self.hours - 1
            self.minutes = 60
            self.seconds = 60

        self.seconds = self.seconds - 1
        #print(self.hours, self.minutes, self.seconds)

        if self.hours == 0 and self.minutes == 0 and self.seconds == 0:
            self.timer.stop()
            self.toolButton_start.setEnabled(True)
            self.toolButton_pause.setDisabled(True)
            winsound.Beep(2000, 1000)

        self.update_display()

    def update_lcd(self):
        """Intializes LCD whenever values in spinboxes are changed by the user"""

        self.hours = self.spinBox_hours.value()
        self.minutes = self.spinBox_minutes.value()
        self.seconds = self.spinBox_seconds.value()
        self.update_display()

        # if the user choose 00:00:00 then disable the start button
        if self.hours == 0 and self.minutes == 0 and self.seconds == 0:
            self.toolButton_start.setDisabled(True)
        else:
            self.toolButton_start.setEnabled(True)

    def update_display(self):
        """Updates LCD at every tick of the clock"""

        if self.hours < 10:
            self.hours = '0' + str(self.hours)
        if self.minutes < 10:
            self.minutes = '0' + str(self.minutes)
        if self.seconds < 10:
            self.seconds = '0' + str(self.seconds)

        self.string_to_be_displayed = str(self.hours) + ':' + str(self.minutes) + ':' + str(self.seconds)
        self.lcdNumber.display(self.string_to_be_displayed)


if __name__ == "__main__":
    app = QApplication([])
    my_gui = MyMainGui()
    my_gui.show()
    app.exit(app.exec_())
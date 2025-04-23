from tkinter import *
from tkinter import ttk
from time import sleep
from ttkwidgets.autocomplete import AutocompleteCombobox
import pickle

class Calling():
    def __init__(self, org1, org2, callingClass, callingName):
        self.org1 = org1
        self.org2 = org2
        self.callingClass = callingClass
        self.callingName = callingName
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        # return "Calling("  + ", ".join(reversed([self.org1, self.org2, self.callingClass, self.callingName])) + ")"
        return ", ".join([self.callingName, self.org1, self.org2, self.callingClass])
    
class NoOverAutocompleteCombobox(AutocompleteCombobox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.last_eval = None
        self.min_delta = 50
        self.bind('<KeyPress>', self.handle_keypress)
        self.previousKeyStillPressed = False
        self.keysPressed = 0

    def handle_keyrelease(self, event):
        self.keysPressed -= 1
        if self.keysPressed == 0:
            return super().handle_keyrelease(event)
        
    def handle_keypress(self, event):
        self.keysPressed += 1

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return("break")


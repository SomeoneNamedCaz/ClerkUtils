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
    
class MyAutocompleteCombobox(AutocompleteCombobox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.last_eval = None
        self.min_delta = 50
        self.bind('<KeyPress>', self.handle_keypress)
        self.previousKeyStillPressed = False
        self.keysPressed = 0

    def handle_keyrelease(self, event):
        print("released", event.time, event.keysym)
        self.keysPressed -= 1
        if self.keysPressed == 0:
            return super().handle_keyrelease(event)
        
    def handle_keypress(self, event):
        self.keysPressed += 1
        print("pressed",event.time, event.keysym)

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return("break")


def loadDropDowns(people,callingDict):
    root = Tk()
    root.geometry("300x400")
    root.configure(background="black")
    

    peopleLabel = Label(root, text="person")
    peopleLabel.pack(anchor=W, padx=10)
    peopleDropDown = MyAutocompleteCombobox(root,completevalues=people)
    peopleDropDown.pack(anchor=W, padx=10)

    callingLabel = Label(root,text="calling")
    callingLabel.pack(anchor=W, padx=10)
    callingDropDown = MyAutocompleteCombobox(root,completevalues=list(callingDict.keys()))
    callingDropDown.pack(anchor=W, padx=10)

"""
def submit(enterCallingFunc, *args, keyBindArg=None):
    print("saved")
    person = peopleDropDown.get()
    calling: Calling = callingDict[callingDropDown.get()]
    peopleDropDown.set("")
    callingDropDown.set("")
    enterCallingFunc(*args)

if __name__ == "__main__":
    
    people = getPeople(wait, driver)
    loadCallingsFirst = True
    if loadCallingsFirst:
        with open("callingPickle","rb") as out:
            callings = pickle.load(out)
    else:
        callings = getCallings(wait, driver, people[0])
        with open("callingPickle","wb") as out:
            pickle.dump(callings,out)
    callingStrs = [str(calling) for calling in callings]
    callingDict = {str(calling) : calling for calling in callings}
    root = Tk()
    root.geometry("300x400")
    root.configure(background="black")
    

    peopleLabel = Label(root, text="person")
    peopleLabel.pack(anchor=W, padx=10)
    peopleDropDown = AutocompleteCombobox(root,completevalues=people)
    peopleDropDown.pack(anchor=W, padx=10)

    callingLabel = Label(root,text="calling")
    callingLabel.pack(anchor=W, padx=10)
    callingDropDown = AutocompleteCombobox(root,completevalues=list(callingDict.keys()))
    callingDropDown.pack(anchor=W, padx=10)


    submitButton = Button(root,text="submit",command=submit,)
    submitButton.pack(anchor=W, padx=10)
    submitButton.bind("<Return>", submit)

    print("started")
    
    sleep(10)

    root.mainloop()"""
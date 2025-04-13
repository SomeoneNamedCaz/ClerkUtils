from tkinter import *
from tkinter import ttk
from time import sleep
from ttkwidgets.autocomplete import AutocompleteCombobox
# import tkin
# root = Tk()
# root.geometry("400x400")
# canvas = Canvas(tk)
# canvas.mainloop()

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return("break")



root = Tk()
root.geometry("300x400")
root.configure(background="black")
# Label (root, text="Type Your Message:\n", bg="Black", fg="white", font="none 25 bold").pack(anchor=N)

# e = Text(root, width=75, height=10)
# e.bind("<Tab>", focus_next_widget)
def getPeople():
    pass

people = ["me", "someone else", "random person"]
callings = ["exec sec", "clerk", "teacher"]

peopleLabel = Label(root,text="person")
peopleLabel.pack(anchor=W, padx=10)
peopleDropDown = AutocompleteCombobox(root,completevalues=people)
peopleDropDown.pack(anchor=W, padx=10)

callingLabel = Label(root,text="calling")
callingLabel.pack(anchor=W, padx=10)
callingDropDown = AutocompleteCombobox(root,completevalues=callings)
callingDropDown.pack(anchor=W, padx=10)


def submit(keyBindArg=None):
    # if root.focus_get() == submitButton:
    print("saved")
    peopleDropDown.set("")
    callingDropDown.set("")


submitButton = Button(root,text="submit",command=submit,)
submitButton.pack(anchor=W, padx=10)
submitButton.bind("<Return>", submit)

# def makeSuggestion():
#     print("ino func",root.focus_get())
#     # if focused on button check enter
    
#     currentText = peopleDropDown.get()
#     print(currentText)
#     # suggestions = [people]
#     root.after(100, makeSuggestion)

# root.after(10, makeSuggestion)
root.mainloop()


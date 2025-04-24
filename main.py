import re
from playwright.sync_api import Playwright, sync_playwright, expect, TimeoutError
import re
import pickle
from time import sleep
from dropDownFuncs import *
from tkinter import filedialog
import pandas as pd
from moveFuncs import *
from callingFuncs import *
import dateutil

USERNAME = ""
PASSWORD = ""

# column names for movin df
FULL_NAME_COL = "Full Name"
BIRTHDATE_COL = "Birthdate"
BUILDING_ADDR_COL = "Building Address"
APART_NUM_COL = "Apartment Number (if up or down house, enter anything)"

# city constant
CITY = "provo"
PICKLE_FILENAME = "memberData.pkl"


with open("loginInfo.config") as file:
    usernameFlag = "username:"
    passwordFlag = "password:"
    for line in file:
        if usernameFlag in line:
            USERNAME = line.replace(usernameFlag, "").strip()
        elif passwordFlag in line:  
            PASSWORD = line.replace(passwordFlag, "").strip()
    
class UnrecognizedFileTypeError(Exception):
    pass


def login(page):
    page.goto("https://lcr.churchofjesuschrist.org/")
    page.get_by_role("textbox", name="Username").fill(USERNAME)
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Password").fill(PASSWORD)
    page.get_by_role("button", name="Verify").click()


def moveInButtonClicked(page, filename=None):
    if not filename:
        filename = filedialog.askopenfilename()
    print('Selected:', filename)
    if ".xlsx" in filename:
        df = pd.read_excel(filename)
    elif ".csv" in filename:
        df = pd.read_csv(filename)
    else:
        raise UnrecognizedFileTypeError()
    
    with open("failedMoveIns.txt","w") as file:
        for _, row in df.iterrows():
            print(row)
            name = row.loc[FULL_NAME_COL]
            birthdate = pd.to_datetime(row.loc[BIRTHDATE_COL]).strftime("%d %b %Y")
            addressLine1 = re.findall(r"\((.+)\)",row.loc[BUILDING_ADDR_COL])
            addressLine2 = str(row.loc[APART_NUM_COL])
            print( name, birthdate, addressLine1, addressLine2, CITY,)
            try:
                moveIn(page, name, birthdate, addressLine1, addressLine2, CITY, "NotUsed")
            except TimeoutError:
                print(name, birthdate, addressLine1, addressLine2, CITY, file=file)
            
def updatePickleFile(page):
    people = getMembers(page)
    sleep(1)
    callings = getCallings(page, people[0])
    with open(PICKLE_FILENAME,"wb") as out:
        pickle.dump((callings, people),out)
    return callings, people

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    login(page)

    try:
        with open(PICKLE_FILENAME,"rb") as out:
            callings, people = pickle.load(out)
    except FileNotFoundError:
        callings, people = updatePickleFile(page)
    
    for i,name in enumerate(people):
        family, given = name.split(", ")
        people[i] = " ".join((given,family))
    
    callingDict = {str(calling) : calling for calling in callings}
    root = Tk()
    root.geometry("300x400")
    root.configure(background="black")
    

    peopleLabel = Label(root, text="person")
    peopleLabel.pack(anchor=W, padx=10)
    peopleDropDown = NoOverAutocompleteCombobox(root,completevalues=people)
    peopleDropDown.pack(anchor=W, padx=10)

    callingLabel = Label(root,text="calling")
    callingLabel.pack(anchor=W, padx=10)
    callingDropDown = NoOverAutocompleteCombobox(root,completevalues=list(callingDict.keys()))
    callingDropDown.pack(anchor=W, padx=10)


    def submit(keyBindArg=None):
        print("saved")
        memberName = peopleDropDown.get()
        calling: Calling = callingDict[callingDropDown.get()]
        peopleDropDown.set("")
        callingDropDown.set("")
        addCalling(page, memberName, calling)
        # enterCalling(wait, driver, person, calling.org1, calling.org2, calling.callingClass, calling.callingName)


    submitButton = Button(root,text="submit",command=submit,)
    submitButton.pack(anchor=W, padx=10)
    submitButton.bind("<Return>", submit)
    


    importButton = Button(root, text='Import Move-in Data', command=lambda:moveInButtonClicked(page))
    importButton.pack()



    print("started")
    
    updatePickleFile(page)

    root.mainloop()

    context.close()
    browser.close()



if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
    

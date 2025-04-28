import re
from playwright.sync_api import Playwright, sync_playwright, expect, TimeoutError
import playwright
import re
import pickle
from time import sleep
from dropDownClasses import *
from tkinter import filedialog
import pandas as pd
from moveFuncs import *
from callingFuncs import *
import dateutil
from concurrent.futures import *
from queue import Queue
import os
import sys

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
class InvalidMemberDataException(Exception):
    pass


def login(page):
    page.goto("https://lcr.churchofjesuschrist.org/")
    page.get_by_role("textbox", name="Username").fill(USERNAME)
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Password").fill(PASSWORD)
    page.get_by_role("button", name="Verify").click()


def loadMoveInDF(queue: Queue,filename=None):
    if not filename:
        filename = filedialog.askopenfilename()
    print('Selected:', filename)
    if ".xlsx" in filename:
        df = pd.read_excel(filename)
    elif ".csv" in filename:
        df = pd.read_csv(filename)
    else:
        raise UnrecognizedFileTypeError()
    df.dropna(inplace=True)
    queue.put(df)

    return df
    
def processMoveInDF(page: Page, df: pd.DataFrame):
    with open("failedMoveIns.txt","a") as file:
        for _, row in df.iterrows():
            name = row.loc[FULL_NAME_COL]
            birthdate = pd.to_datetime(row.loc[BIRTHDATE_COL]).strftime("%d %b %Y")
            addressLine1 = re.findall(r"\((.+)\)",row.loc[BUILDING_ADDR_COL])[0]
            addressLine2 = str(int(row.loc[APART_NUM_COL]))

            try:
                moveIn(page, name, birthdate, addressLine1, addressLine2, CITY)
            except playwright._impl._errors.TimeoutError as e:
                if page.get_by_text("we were unable to find any records that match the criteria provided").is_visible():
                    print("BAD INFO",name, birthdate, addressLine1, addressLine2, CITY, file=file)
                elif page.get_by_text("The requested household is already in the ward").is_visible():
                    print("ALREADY MOVED IN",name, birthdate, addressLine1, addressLine2, CITY, file=file)
                else:
                    print("UNKNOWN ERROR",name, birthdate, addressLine1, addressLine2, CITY, file=file)
                
            
def updatePickleFile(page):
    people = getMembers(page)
    sleep(1)
    callings = getCallings(page, people[0])
    with open(PICKLE_FILENAME,"wb") as out:
        pickle.dump((callings, people),out)
    return callings, people

def addCallingLoop(queue: Queue, page: Page):
    while True:
        if queue.empty():
            sleep(10)
        else:
            nextItem = queue.get(block=False)
            if type(nextItem) == pd.DataFrame:
                print("started processing move ins")
                processMoveInDF(page,nextItem)
                print("finished move ins")
            else:
                addCalling(page,*nextItem)
            print("calling added")

def loadTkinter(people, callingDict, callingQueue):
        root = Tk()
        root.geometry("1000x400")
        # root.configure(background="black")
        

        peopleLabel = Label(root, text="person")
        peopleLabel.pack(anchor=W, padx=10)
        peopleDropDown = NoOverAutocompleteCombobox(root, 
                                                    completevalues=people,
                                                    width=max(len(name) for name in people))
        peopleDropDown.pack(anchor=W, padx=10)

        callingLabel = Label(root,text="calling")
        callingLabel.pack(anchor=W, padx=10)
        callingDropDown = NoOverAutocompleteCombobox(root,
                                                     completevalues=list(callingDict.keys()),
                                                     width=max(len(callingName) for callingName in callingDict.keys()))
        callingDropDown.pack(anchor=W, padx=10)

        def submitCalling(keyBindArg=None):
            print("saved")
            memberName = peopleDropDown.get()
            calling: Calling = callingDict[callingDropDown.get()]
                
            peopleDropDown.set("")
            callingDropDown.set("")
            callingQueue.put((memberName, calling))


        submitButton = Button(root,text="submit",command=submitCalling)
        submitButton.pack(anchor=W, padx=10)
        submitButton.bind("<Return>", submitCalling)

        importButton = Button(root, text='Import Move-in Data', command=lambda: loadMoveInDF(callingQueue))
        importButton.pack()

        def updateMemberData():
            with open(PICKLE_FILENAME,"rb") as out:
                callings, people = pickle.load(out)
                callingDropDown.set_completion_list([str(calling) for calling in callings])
                peopleDropDown.set_completion_list(people)

        updateMemberDataButton = Button(root, text='update member data', command=updateMemberData)
        updateMemberDataButton.pack()


        root.attributes('-topmost',True)
        root.mainloop()

def runPlaywright(callingQueue) -> None:
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            login(page)
            updatePickleFile(page)

            addCallingLoop(callingQueue, page)

            context.close()
            browser.close()
    except Exception:
        sys.excepthook(*sys.exc_info())
        exit(1)



if __name__ == "__main__":
    exec = ThreadPoolExecutor(1)
    callingQueue = Queue()
    future = exec.submit(runPlaywright, callingQueue)

    # if the data hasn't been saved wait until playwright gets it
    while not os.path.exists(PICKLE_FILENAME):
        sleep(1)
    
    with open(PICKLE_FILENAME,"rb") as out:
        callings, people = pickle.load(out)
    callingDict = {str(calling) : calling for calling in callings}
    loadTkinter(people, callingDict,callingQueue)
    

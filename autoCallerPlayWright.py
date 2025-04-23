import re
from playwright.sync_api import Playwright, sync_playwright, expect
import re
import pickle
from time import sleep
from dropDownFuncs import *

USERNAME = ""
PASSWORD = ""

with open("loginInfo.config") as file:
    usernameFlag = "username:"
    passwordFlag = "password:"
    for line in file:
        if usernameFlag in line:
            USERNAME = line.replace(usernameFlag, "").strip()
        elif passwordFlag in line:  
            PASSWORD = line.replace(passwordFlag, "").strip()
    

def login(page):
    page.goto("https://lcr.churchofjesuschrist.org/")
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill(USERNAME)
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Password").fill(PASSWORD)
    page.get_by_role("button", name="Verify").click()

def getMembers(page):
    page.locator("#menu-list").get_by_text("Membership").click()
    page.get_by_role("link", name="Member Directory").click()

    dirLocator = page.get_by_text("Member Directory Print Individuals Households Show Gender Age Birth Date")
    
    # dirLocator.scroll_into_view_if_needed()
    sleep(1)
    for i in range(2):
        page.mouse.wheel(0, 15000)
        sleep(1)

    directoryText = dirLocator.evaluate("el => el.outerHTML")
    names = re.findall("<span.+?>\s+([\w ,\.]+)\s+</span>", directoryText)

    return names 

def release(page):
    try:
        page.get_by_text("Member Callings Organization").locator("a").nth(1).click(timeout=5000)
        page.get_by_role("button", name="Release").click()
        page.get_by_role("button", name="Save").click()
        sleep(1)
    except Exception as e:
        print("didn't release",e)

def goToMemberCallingPage(page,name):
    page.locator("#menu-list").get_by_text("Membership").click()
    page.get_by_role("link", name="Member Directory").click()
    page.get_by_role("link", name=name).click()
    page.get_by_role("link", name="View Member Profile").click()
    page.get_by_role("link", name="Callings/Classes").click()

def addCalling(page, name, callingClass, callingName):
    goToMemberCallingPage(page,name)

    # release old calling if applicable
    release(page)
    
    page.get_by_role("link", name="Add calling").click()
    print("clicked add")
    page.get_by_role("combobox").select_option(label=callingClass)
    page.get_by_role("cell", name="Select a calling . .").get_by_role("combobox").select_option(label=callingName)
    page.get_by_role("button", name="Save").click()
    # sleep(1)
    # page.get_by_role("cell", name="Select a calling . .").get_by_role("combobox").select_option("object:561")
    # page.get_by_role("button", name="Save").click()


def getCallings(page, randomMemberName):
    goToMemberCallingPage(page, randomMemberName)
    page.get_by_role("link", name="Add calling").click()
    orgTableHTML = page.get_by_role("combobox").evaluate("el => el.outerHTML")

    allOrgs = re.findall("\<opt\w+? label=\"([\w\s.]+?)\".*?\>", orgTableHTML)
    allOrgs.remove("Select an organization . . .")
    org1s = re.findall("<optgroup label=\"([\w\s.]+?)\">", orgTableHTML)

    callings = []
    currentOrg1 = "None"
    lastOrg = None
    for org in allOrgs:
        if len(org1s) > 0 and org == org1s[0]: 
            currentOrg1 = org
            org1s = org1s[1:]
            continue
        try:
            # page.get_by
            if not lastOrg:
                organizationCombo = page.get_by_role("combobox").select_option(label=org)
            else:
                organizationCombo = page.get_by_role("cell",name=lastOrg).get_by_role("combobox").select_option(label=org)
            # sleep(1)

            callingComboHTML = page.get_by_role("cell", name="Select a calling . .").get_by_role("combobox").evaluate("el => el.outerHTML")
        
            allCallings = re.findall("\<opt\w+? label=\"(.+?)\".*?\>", callingComboHTML)
            callingClasses = re.findall("<optgroup label=\"(.+?)\">", callingComboHTML)

            currentClass = "None"
            for calling in allCallings:
                if len(callingClasses) > 0 and calling == callingClasses[0]:
                    currentClass = calling
                    callingClasses = callingClasses[1:]
                    continue
                callings.append(Calling(currentOrg1, org, currentClass, calling))
            lastOrg = org
        except Exception as e:
            raise #print("failed", e)
            pass
        
    # for calling in callings:
    #     print("callings",calling)
    return callings

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    login(page)
    people = getMembers(page)
    loadCallingsFirst = True
    if loadCallingsFirst:
        with open("callingPickle","rb") as out:
            callings = pickle.load(out)
    else:
        callings = getCallings(page, people[0])
        with open("callingPickle","wb") as out:
            pickle.dump(callings,out)
    callingStrs = [str(calling) for calling in callings]
    callingDict = {str(calling) : calling for calling in callings}
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


    def submit(keyBindArg=None):
        print("saved")
        memberName = peopleDropDown.get()
        calling: Calling = callingDict[callingDropDown.get()]
        peopleDropDown.set("")
        callingDropDown.set("")
        addCalling(page, memberName, calling.org1,calling.callingName)
        # enterCalling(wait, driver, person, calling.org1, calling.org2, calling.callingClass, calling.callingName)


    submitButton = Button(root,text="submit",command=submit,)
    submitButton.pack(anchor=W, padx=10)
    submitButton.bind("<Return>", submit)

    print("started")
    

    root.mainloop()

    context.close()
    browser.close()



if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
    

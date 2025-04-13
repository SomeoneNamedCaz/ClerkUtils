import selenium
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pickle
from dropDownFuncs import *

def login(waiter):
    waiter.until(EC.element_to_be_clickable((By.ID, "input28"))).send_keys("cazmire")
                                                    # "//input[@type='submit']"
    waiter.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))).click()
    
    waiter.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys("RampagingRhino!3@4")
    waiter.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))).click()
def search(waiter,query):
    sleep(5)
    waiter.until(EC.element_to_be_clickable((By.ID, "uber-search-input"))).send_keys(query)
    sleep(5)
    waiter.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='dropdown-item']"))).click()
    sleep(2)
def goToMemberCallings(waiter,name):
    sleep(5)
    search(waiter,name)
    waiter.until(EC.element_to_be_clickable((By.XPATH, "//li[@ng-class=\"{active: tab == 'callings'}\"]"))).click()
    sleep(2)
    
def clickCallingSaveButton(waiter):
    saveButton = waiter.until(EC.element_to_be_clickable((By.XPATH,"//button[@class=\"btn btn-small btn-primary ng-binding\"]")))
    saveButton.click()
def setApart(waiter,name):
    
    goToMemberCallings(waiter,name)
    
    try:
        editButton = waiter.until(EC.element_to_be_clickable((By.XPATH, "//a[@ng-show=\"!c.editMode && c.userCanEdit && (c.editable || c.contactInfoEditable)\"]")))
        editButton.click()
        # if <span ng-show="c.setApart" class="callings-mobile ng-binding">Yes</span>
        setApartButton = waiter.until(EC.element_to_be_clickable((By.XPATH, "//input[@ng-show=\"c.editMode && c.editable && !c.releaseDate && !c.requiresSetApartDateAndPerson\"]")))
        if not setApartButton.is_selected():
            # setApartButton = waiter.until(EC.element_to_be_clickable((By.XPATH, "//input[@ng-show=\"c.editMode && c.editable && !c.releaseDate && !c.requiresSetApartDateAndPerson\"]")))
            setApartButton.click()
            #<button ng-click="save()" class="btn btn-small btn-primary ng-binding" cr-btn-loading="c.saving" data-loading-text="Saving . . .">Save</button>
            clickCallingSaveButton(waiter)
    except Exception as e:
        print("failed on " + name +  "with",e)
    sleep(4)

def printAtts(driver, elt):
    ats = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', elt)
    print(ats)

def enterCalling(waiter,driver, name, org1,org2,callingClass,calling):
    goToMemberCallings(waiter,name)
    # <a ng-if="authorizedToEditCallings &amp;&amp; anySubOrgsForPotentialNewCallings" ng-click="addCalling()" href="" class="pull-right ng-binding ng-scope"> <i class="lds icon-add"></i> Add calling </a>
    addCallingButton = waiter.until(EC.element_to_be_clickable((By.XPATH, "//a[@ng-click=\"addCalling()\"]")))
    addCallingButton.click()
    sleep(0.1)
    # organizationCombo = waiter.until(EC.visibility_of_element_located((By.XPATH, '//select[@ng-model="selectedSubOrg"]')))
    # printAtts(driver, organizationCombo)
    # options = organizationCombo.get_attribute("ng-options")
    
    # print(help(options))

    # print("combo attrs help", organizationCombo.attrs)
    organizationCombo = driver.find_element(By.XPATH,'//select[@ng-model="selectedSubOrg"]/optgroup[@label="' + org1 +'"]/*[contains(text(), "' + org2 +'")]')
    organizationCombo.click()
    sleep(4)

    callingCombo = driver.find_element(By.XPATH, '//select[@ng-options="p as p.name group by p.typeGroup for p in selectedSubOrg.positions"]/optgroup[@label="' + callingClass + '"]/*[contains(text(), "' + calling + '")]')
    callingCombo.click()
    sleep(1.9)#class="btn btn-small ng-binding btn-warning"
    button = driver.find_element(By.XPATH, '//button[@ng-click="save()"]')
    button.click()
    sleep(2)

def getCallings(waiter, driver, randomMember):
    goToMemberCallings(waiter, randomMember)
    addCallingButton = waiter.until(EC.element_to_be_clickable((By.XPATH, "//a[@ng-click=\"addCalling()\"]")))
    addCallingButton.click()
    sleep(0.1)
    orgTable = driver.find_element(By.XPATH,'//select[@ng-model="selectedSubOrg"]')
    print(orgTable.get_attribute("outerHTML"))
    allOrgs = re.findall("\<opt\w+? label=\"([\w\s.]+?)\".*?\>", orgTable.get_attribute("outerHTML"))
    org1s = re.findall("<optgroup label=\"([\w\s.]+?)\">", orgTable.get_attribute("outerHTML"))
    print(allOrgs)
    print(org1s)
    callings = []
    currentOrg1 = "None"
    for org in allOrgs:
        if len(org1s) > 0 and org == org1s[0]:
            currentOrg1 = org
            org1s = org1s[1:]
            continue
        try:
            organizationCombo = driver.find_element(By.XPATH,'//select[@ng-model="selectedSubOrg"]/optgroup[@label="' + currentOrg1 +'"]/*[contains(text(), "' + org +'")]')
            organizationCombo.click()
            sleep(5)
            callingCombo = driver.find_element(By.XPATH, '//select[@ng-options="p as p.name group by p.typeGroup for p in selectedSubOrg.positions"]')
        
            allCallings = re.findall("\<opt\w+? label=\"(.+?)\".*?\>", callingCombo.get_attribute("outerHTML"))
            callingClasses = re.findall("<optgroup label=\"(.+?)\">", callingCombo.get_attribute("outerHTML"))
            print(callingCombo.get_attribute("outerHTML"))
            print(allCallings)
            print(callingClasses)
            print("______________")
            currentClass = "None"
            for calling in allCallings:
                if len(callingClasses) > 0 and calling == callingClasses[0]:
                    currentClass = calling
                    callingClasses = callingClasses[1:]
                    continue
                callings.append(Calling(currentOrg1, org, currentClass, calling))
        except:
            pass
        
    for calling in callings:
        print(calling)
    return callings

def getPeople(waiter, driver):

    search(waiter, "member Directory")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(0.5)
    personTable = waiter.until(EC.visibility_of_element_located((By.XPATH, '(//table)[1]')))

    names = re.findall("<span.+?>\s+([\w ,\.]+)\s+</span>", personTable.get_attribute("outerHTML"))

    return names


def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return("break")


if __name__ == "__main__":
    driver = selenium.webdriver.Chrome()
    wait = WebDriverWait(driver, 30)

    driver.get("https://lcr.churchofjesuschrist.org/?lang=eng")

    login(wait)
    # enterCalling(wait,driver, "Erin Pickett","Relief Society", "Activities","Standard Callings","Relief Society Activity Coordinator")
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


    def submit(keyBindArg=None):
        print("saved")
        person = peopleDropDown.get()
        calling: Calling = callingDict[callingDropDown.get()]
        peopleDropDown.set("")
        callingDropDown.set("")
        enterCalling(wait, driver, person, calling.org1, calling.org2, calling.callingClass, calling.callingName)


    submitButton = Button(root,text="submit",command=submit,)
    submitButton.pack(anchor=W, padx=10)
    submitButton.bind("<Return>", submit)

    print("started")
    
    sleep(10)

    root.mainloop()


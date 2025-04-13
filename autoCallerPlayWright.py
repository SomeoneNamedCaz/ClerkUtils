import re
from playwright.sync_api import Playwright, sync_playwright, expect
import re
import pickle
from time import sleep


def login(page):
    page.goto("https://id.churchofjesuschrist.org/oauth2/default/v1/authorize?client_id=0oajwqqtpz7f8r1OD357&scope=openid%20profile%20email%20offline_access%20cmisid%20group&response_type=code&redirect_uri=https%3A%2F%2Flcr.churchofjesuschrist.org%2Fapi%2Fauth%2Fcallback&nonce=yHPNHDCO56iJk6aOPjnRw_qjI8XPAN0EUW_gea8qrYI&state=eyJyZXR1cm5UbyI6Imh0dHBzOi8vbGNyLmNodXJjaG9mamVzdXNjaHJpc3Qub3JnLz9sYW5nPWVuZyJ9&code_challenge=sJGmzVysKwEADZgcNY59SLhCgM4SMeO5cjpkmV7dERM&code_challenge_method=S256")
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill(USERNAME)
    page.get_by_role("button", name="Next").click()
    page.get_by_role("textbox", name="Password").fill(PASSWORD)
    page.get_by_role("button", name="Verify").click()

def getMemberDirectory(page):
    page.locator("#menu-list").get_by_text("Membership").click()
    page.get_by_role("link", name="Member Directory").click()

    dirLocator = page.get_by_text("Member Directory Print Individuals Households Show Gender Age Birth Date")
    
    # dirLocator.scroll_into_view_if_needed()
    sleep(2)
    for i in range(2):
        page.mouse.wheel(0, 15000)
        sleep(2)
    return dirLocator

def getMembers(page):
   
    dirLocator = getMemberDirectory(page)
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
        print("exp",e)

# def goToMemberCallingPage(page,name):


def addCalling(page, name, callingClass, callingName):
    page.get_by_role("link", name=name).click()
    page.get_by_role("link", name="View Member Profile").click()
    page.get_by_role("link", name="Callings/Classes").click()

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

def getCallings(page, randomName):

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    login(page)
    people = getMembers(page)
    for person in people: 
        if "Clark" in person and "Kaden" in person:
            break
    memberName = person
    callingClass = "Teachers"
    callingName = "Elders Quorum Teacher"
    addCalling(page, memberName, callingClass,callingName)
    sleep(10)
    # page.get_by_role("row", name="Relief Society Presidency").locator("a").nth(1).click()
    # page.get_by_role("checkbox").check()
    # page.get_by_role("button", name="Save").click()
    # page.get_by_role("row", name="Relief Society Presidency").locator("a").nth(1).click()
    # page.get_by_role("checkbox").uncheck()
    # page.get_by_role("button", name="Save").click()

    # ---------------------
    context.close()
    browser.close()



if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
    

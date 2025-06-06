import re
from playwright.sync_api import Playwright, sync_playwright, expect, TimeoutError
import re
import pickle
from time import sleep
from dropDownClasses import *
from tkinter import filedialog
import pandas as pd
import dateutil

def getMembers(page): 
    page.locator("#menu-list").get_by_text("Membership").click()
    page.get_by_role("link", name="Member Directory").click()

    dirLocator = page.get_by_text("Member Directory Print Individuals Households Show Gender Age Birth Date")
    

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
    except TimeoutError as e:
        print("didn't release",e)

def goToMemberCallingPage(page,name):

    page.locator("#menu-list").get_by_text("Membership").click()
    page.get_by_role("link", name="Member Directory").click()

    sleep(1)
    for i in range(2):
        page.mouse.wheel(0, 15000)
        sleep(1)

    page.get_by_role("link", name=name).click()
    page.get_by_role("link", name="View Member Profile").click()
    page.get_by_role("link", name="Callings/Classes").click()
    sleep(0.5)

def addCalling(page, name, calling):
    goToMemberCallingPage(page,name)

    # release old calling if applicable
    release(page)
    
    page.get_by_role("link", name="Add calling").click()
    print("clicked add")
    page.get_by_role("combobox").select_option(label=calling.org2)
    page.get_by_role("cell", name="Select a calling . .").get_by_role("combobox").select_option(label=calling.callingName)
    page.get_by_role("button", name="Save").click()
    sleep(0.5)


def getCallings(page, members):

    callings = []
    foundEQ = False
    foundRS = False

    for member in members:
        goToMemberCallingPage(page, member)
        page.get_by_role("link", name="Add calling").click()
        orgTableHTML = page.get_by_role("combobox").evaluate("el => el.outerHTML")

        allOrgs = re.findall("\<opt\w+? label=\"(.+?)\".*?\>", orgTableHTML)
        allOrgs.remove("Select an organization . . .")
        org1s = re.findall("<optgroup label=\"(.+?)\">", orgTableHTML)
        print("org table",orgTableHTML)
        
        currentOrg1 = "None"
        lastOrg = None
        for org in allOrgs:
            print(org)
            if "Elders Quorum" in org:
                foundEQ = True
            if "Relief Society" in org:
                foundRS = True
            if len(org1s) > 0 and org == org1s[0]: 
                currentOrg1 = org
                org1s = org1s[1:]
                continue
            print("outer",page.get_by_role("combobox").all_text_contents())
            if not lastOrg:
                organizationCombo = page.get_by_role("combobox").select_option(label=org)
            else:
                organizationCombo = page.get_by_role("cell",name=lastOrg).get_by_role("combobox").select_option(label=org)
            sleep(1)
            
            callingComboHTML = page.get_by_role("cell", name="Select a calling . .").get_by_role("combobox").evaluate("el => el.outerHTML")
            print("calling table",callingComboHTML)
            allCallings = re.findall("\<opt\w+? label=\"(.+?)\".*?\>", callingComboHTML)
            callingClasses = re.findall("<optgroup label=\"(.+?)\">", callingComboHTML)
            print("callings",allCallings)
            currentClass = "None"
            for calling in allCallings:
                if len(callingClasses) > 0 and calling == callingClasses[0]:
                    currentClass = calling
                    callingClasses = callingClasses[1:]
                    continue
                if "Select a calling" in calling:
                    continue
                
                callingObj = Calling(currentOrg1, org, currentClass, calling)
                if callingObj not in callings:
                    callings.append(callingObj)

            lastOrg = org
        if foundEQ and foundRS:
            break

    return callings
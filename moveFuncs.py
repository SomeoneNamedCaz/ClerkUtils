import re
from playwright.sync_api import Playwright, sync_playwright, expect, TimeoutError, Page
import re
import pickle
from time import sleep
from dropDownFuncs import *

def moveIn(page: Page, name, birthdate, addressLine1, addressLine2, city, state):
    page.locator("#menu-list").get_by_text("Membership").click()
    page.get_by_role("link", name="Move Records In").click()
    page.get_by_role("textbox", name="Member Lookup").fill(name)
    page.get_by_role("textbox", name="Birth Date").fill(birthdate)
    page.get_by_role("button", name="Lookup").click()
    sleep(1)
    page.get_by_text(name).click()
    sleep(1)
    page.locator("#select-001004216582A").check()
    sleep(1)
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("textbox", name="Street 1").fill(addressLine1)
    page.get_by_role("textbox", name="Street 2").fill(addressLine2)
    page.get_by_role("textbox", name="City").fill(city)
    sleep(1)
    page.get_by_role("button", name="Move into Ward").click()
    sleep(1)
    try:
        page.get_by_role("button", name="Move into Ward").click(timeout=5000) # sometimes there is a pop-up 
    except TimeoutError:
        pass
    sleep(10)

def moveOut(page: Page, name,  addressLine1, addressLine2, city, state):
    page.locator("#menu-list").get_by_text("Membership").click()
    page.get_by_role("link", name="Move Records Out").click()
    page.get_by_role("textbox", name="Member Name or MRN").fill(name)
    page.locator("#select-001004216582A").check()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("textbox", name="Street 1").fill(addressLine1)
    page.get_by_role("textbox", name="Street 2").fill(addressLine2)
    page.get_by_role("textbox", name="City").fill(city)
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("combobox").select_option("object:210")
    page.get_by_role("button", name="Continue").click()
    sleep(10)
    page.get_by_role("button", name="Move Out of Ward").click()
    




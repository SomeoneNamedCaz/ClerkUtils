import unittest
from main import *
import re
from playwright.sync_api import Playwright, sync_playwright, expect, TimeoutError



class FailedToLocateError(Exception):
    pass

class Tests(unittest.TestCase):
    
    def testLogin(self):
        sleep(10)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            try:
                login(page)
            except TimeoutError:
                raise FailedToLocateError("failed to locate login item")
            sleep(1)
            expect(page).to_have_url("https://lcr.churchofjesuschrist.org/")
    def testGetMembers(self):
        pass
    def testGetCallings(self):
        sleep(10)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            login(page)
            people = getMembers(page)
            callings: list[Calling] = getCallings(page, people[0])

        standardCallings = {calling for calling in callings if calling.callingClass == "Standard Callings"}
        self.assertEqual(len(standardCallings), 83)

    def testAddCallingFromMembDir(self):
        sleep(10)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            login(page)
            people = getMembers(page)
            callings: list[Calling] = getCallings(page, people[0])
            people = getMembers(page)
            addCalling(page, people[1], callings[0])

    def testAddCallingFromOtherPage(self):
        sleep(10)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            login(page)
            people = getMembers(page)
            callings: list[Calling] = getCallings(page, people[0])
            addCalling(page, people[1], callings[0])

    def testAddCallingFromOtherPage(self):
        sleep(10)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            login(page)
            people = getMembers(page)
            callings: list[Calling] = getCallings(page, people[0])
            for calling in callings:
                if calling.callingName == "Activities Council Member":
                    break
            addCalling(page, people[1], calling)
    def moveOutHelper(self,page):
        df = pd.read_csv("/Users/cazcullimore/Downloads/Move out.csv")
        for _, row in df.iterrows():
            name = row.loc[FULL_NAME_COL]
            addressLine1 = row.loc[BUILDING_ADDR_COL]
            addressLine2 = str(row.loc[APART_NUM_COL])
            try:
                moveOut(page, name,  addressLine1, addressLine2, CITY)
            except TimeoutError:
                pass
    def testMoveInButtonClickedCSV(self):
        sleep(10)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            login(page)
            self.moveOutHelper(page)
            sleep(10)
            queue = Queue()
            loadMoveInDF(queue,filename="/Users/cazcullimore/Downloads/Move ins (Responses) - Form Responses 1.csv")
            processMoveInDF(page, queue.get())
            self.moveOutHelper(page)
            
    def testMoveInButtonClickedXLSX(self):
        sleep(10)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            login(page)
            self.moveOutHelper(page)
            sleep(10)
            queue = Queue()
            loadMoveInDF(queue,filename="/Users/cazcullimore/Downloads/Move ins (Responses)-1.xlsx")
            processMoveInDF(page, queue.get())
            self.moveOutHelper(page)


if __name__ == '__main__':
    unittest.main(failfast=False)
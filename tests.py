import unittest
from autoCallerPlayWright import *
import re
from playwright.sync_api import Playwright, sync_playwright, expect, TimeoutError

callingSet = {"Ward Missionary, None, Ward Missionaries, Standard Callings", "Ward Temple and Family History Consultant, None, Temple and Family History, Standard Callings", "Indexing Worker, None, Temple and Family History, Standard Callings", "Relief Society President  (will fail because includes name), Relief Society, Relief Society Presidency, Standard Callings", "Relief Society First Counselor  (will fail because includes name), Relief Society, Relief Society Presidency, Standard Callings", "Relief Society Second Counselor  (will fail because includes name), Relief Society, Relief Society Presidency, Standard Callings", "Relief Society Secretary  (will fail because includes name), Relief Society, Relief Society Presidency, Standard Callings", "Relief Society Assistant Secretary, Relief Society, Relief Society Presidency, Standard Callings", "Relief Society Teacher, Relief Society, Teachers, Standard Callings", "Relief Society Ministering Secretary, Relief Society, Ministering, Standard Callings", "Relief Society Activity Coordinator, Relief Society, Activities, Standard Callings", "Relief Society Assistant Activity Coordinator, Relief Society, Activities, Standard Callings", "Relief Society Activity Committee Member, Relief Society, Activities, Standard Callings", "Relief Society Music Leader, Relief Society, Music, Standard Callings", "Relief Society Pianist, Relief Society, Music, Standard Callings", "Relief Society Service Coordinator, Relief Society, Service, Standard Callings", "Relief Society Assistant Service Coordinator, Relief Society, Service, Standard Callings", "Relief Society Service Committee Member, Relief Society, Service, Standard Callings", "Young Women President, Young Women, Young Women Presidency, Standard Callings", "Young Women First Counselor, Young Women, Young Women Presidency, Standard Callings", "Young Women Second Counselor, Young Women, Young Women Presidency, Standard Callings", "Young Women Secretary, Young Women, Young Women Presidency, Standard Callings", "Young Women Specialist, Young Women, Young Women Presidency, Standard Callings", "Young Women Specialist, Young Women, Additional Young Women Callings, Standard Callings", "Young Women Specialist - Activities, Young Women, Additional Young Women Callings, Standard Callings", "Young Women Specialist - Camp Director, Young Women, Additional Young Women Callings, Standard Callings", "Young Women Specialist - Assistant Camp Director, Young Women, Additional Young Women Callings, Standard Callings", "Young Women Stake Youth Committee, Young Women, Additional Young Women Callings, Standard Callings", "Young Women Specialist - Sports, Young Women, Additional Young Women Callings, Standard Callings", "Young Women Specialist - Sports Assistant, Young Women, Additional Young Women Callings, Standard Callings", "Sunday School Teacher, Sunday School, Gospel Doctrine, Standard Callings", "Sunday School Teacher, Sunday School, Course 17, Standard Callings", "Sunday School Teacher, Sunday School, Course 16, Standard Callings", "Sunday School Teacher, Sunday School, Course 15, Standard Callings", "Sunday School Teacher, Sunday School, Course 14, Standard Callings", "Sunday School Teacher, Sunday School, Course 13, Standard Callings", "Sunday School Teacher, Sunday School, Course 12, Standard Callings", "Sunday School Teacher, Sunday School, Course 11, Standard Callings", "Sunday School Teacher, Sunday School, Unassigned Teachers, Standard Callings", "Resource Center Specialist, Sunday School, Resource Center, Standard Callings", "Primary President, Primary, Primary Presidency, Standard Callings", "Primary First Counselor, Primary, Primary Presidency, Standard Callings", "Primary Second Counselor, Primary, Primary Presidency, Standard Callings", "Primary Secretary, Primary, Primary Presidency, Standard Callings", "Relief Society Music Leader, Primary, Music, Standard Callings", "Relief Society Pianist, Primary, Music, Standard Callings", "Primary Teacher, Primary, Valiant 10, Standard Callings", "Primary Teacher, Primary, Valiant 9, Standard Callings", "Primary Teacher, Primary, Valiant 8, Standard Callings", "Primary Teacher, Primary, Valiant 7, Standard Callings", "Primary Teacher, Primary, CTR 6, Standard Callings", "Primary Teacher, Primary, CTR 5, Standard Callings", "Primary Teacher, Primary, CTR 4, Standard Callings", "Primary Teacher, Primary, Sunbeam, Standard Callings", "Nursery Leader, Primary, Nursery, Standard Callings", "Sunday School Teacher, Primary, Unassigned Teachers, Standard Callings", "Relief Society Adviser to Young Single Adult Sisters, Other Callings, Young Single Adult, Standard Callings", "Young Single Adult Adviser, Other Callings, Young Single Adult, Standard Callings", "Young Single Adult Leader, Other Callings, Young Single Adult, Standard Callings", "Young Single Adult Committee Chair, Other Callings, Young Single Adult, Standard Callings", "Young Single Adult Committee Member, Other Callings, Young Single Adult, Standard Callings", "Magazine Representative, Other Callings, Church Magazines, Standard Callings", "Building Representative, Other Callings, Facilities, Standard Callings", "Scheduler--Building 1, Other Callings, Facilities, Standard Callings", "Scheduler--Building 2, Other Callings, Facilities, Standard Callings", "Scheduler--Building 3, Other Callings, Facilities, Standard Callings", "Scheduler--Building 4, Other Callings, Facilities, Standard Callings", "Scheduler--Building 5, Other Callings, Facilities, Standard Callings", "FSY Conferences Representative, Other Callings, For the Strength of Youth, Standard Callings", "History Specialist, Other Callings, History, Standard Callings", "Relief Society Music Leader, Other Callings, Music, Standard Callings", "Relief Society Pianist, Other Callings, Music, Standard Callings", "Email Communication Specialist, Other Callings, Technology, Standard Callings", "Technology Specialist, Other Callings, Technology, Standard Callings", "Ward/Branch Interpreter, Other Callings, Technology, Standard Callings"}


class FailedToLocateError(Exception):
    pass

class TestAddCalling(unittest.TestCase):
    
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
        self.assertEqual(len(callingSet),len(standardCallings))

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
    def testMoveInButtonClickedCSV(self):
        # sleep(10)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            login(page)
            moveInButtonClicked(page, filename="/Users/cazcullimore/Downloads/Move ins (Responses) - Form Responses 1.csv")
            moveOut()
    def testMoveInButtonClickedXLSX(self):
        # sleep(10)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            login(page)
            moveInButtonClicked(page, filename="/Users/cazcullimore/Downloads/Move ins (Responses).xlsx")

    def testMoveOut(self):
         with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            login(page)



if __name__ == '__main__':
    unittest.main()
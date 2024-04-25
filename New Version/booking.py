import openpyxl.workbook
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import date
from time import sleep
import func
import openpyxl
import json
import re
import os



def submit(accounts:list):
    #  Today's month
    current_time = date.today()
    current_year = current_time.year
    current_month = current_time.month
    current_date = current_time.day
    # current_date = 29
    print(current_month, current_date, current_year)

    password = "Book123456"
    for account in accounts:        
    
        remote_debugging_address = "127.0.0.1:9024"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", remote_debugging_address)
        driver = webdriver.Chrome(options=chrome_options)

        driver.get("https://account.booking.com/register")
        func.wait_url(driver, "https://account.booking.com/register")
        try:
            driver.find_element(By.CSS_SELECTOR, "#onetrust-accept-btn-handler").click()
        except Exception as e:
            # Add your desired action if the element is not found
            print("Accept button not found. Performing alternative action...")
            pass
        sleep(2)

        if account["registered"] == False:
            sleep(2)
            func.find_element(driver, By.ID, "username").send_keys(account["email"])
            sleep(0.3)
            func.find_element(driver, By.CSS_SELECTOR, "#root > div > div > div.app > div.access-container.bui_font_body > div > div > div > div > div > div > div > form > div.Vw55_aACpYkyD1luIfis.cQj98l8L_Fc_IXYCWd4I.kBoHgdoepdx0bTMKriS3 > div:nth-child(2) > button").click()
            sleep(0.3)
            func.find_element(driver, By.ID, "new_password").send_keys(password)
            sleep(0.5)
            func.find_element(driver, By.ID, "confirmed_password").send_keys(password)
            sleep(0.5)
            func.find_element(driver, By.CSS_SELECTOR, "#root > div > div > div.app > div.access-container.bui_font_body > div > div > div > div > div > div > div > form > div > button").click()
            sleep(10)
            print("Successfully Registered! and Logined!")
            account["registered"] = True
            with open('accounts.json', 'w') as file:
                json.dump(accounts, file)
            sleep(8)
            func.find_element(driver, By.CSS_SELECTOR, "#b2indexPage > div.b9720ed41e.cdf0a9297c > div > div > div > div.c1af8b38aa > div > button").click()
            print("Got it!")
            sleep(1)
            func.find_element(driver, By.CSS_SELECTOR, "#\:rg\:").send_keys("Tirana")
            sleep(1)
            func.find_element(driver, By.CSS_SELECTOR, "#indexsearch > div.hero-banner-searchbox > div > form > div.ffb9c3d6a3.c9a7790c31.e691439f9a > div:nth-child(2) > div > div").click()
            sleep(2)
            calenders = func.find_elements(driver, By.CLASS_NAME, 'd358556c65')
            print(calenders)

            if current_date + 4 <= 31:
                # elem_table = func.find_element(driver, By.XPATH, '//*[@id="calendar-searchboxdatepicker"]/div/div[1]/div/div[1]')
                # print("calendar 1: ", current_date, elem_table)
                start_date_found = False
                end_date = current_date + 4
                # Loop through the rows and cells to find and click the cells for the date range
                for row in calenders[0].find_elements(By.XPATH, './/tr'):
                    for cell in row.find_elements(By.XPATH, ".//td"):
                        if cell.text == str(current_date):
                            start_date_found = True
                            cell.click()
                            sleep(2)
                            print("Start Date Clicked:", cell.text)

                        if start_date_found and cell.text == str(end_date):
                            cell.click()
                            print("End Date Clicked:", cell.text)
                            sleep(2)
                        break
                func.find_element(driver, By.XPATH, '//*[@id="indexsearch"]/div[2]/div/form/div[1]/div[4]/button').click()
                sleep(15)
                hotels = driver.find_elements(By.CSS_SELECTOR, "#bodyconstraint-inner > div:nth-child(10) > div > div.af5895d4b2 > div.df7e6ba27d > div.bcbf33c5c3 > div.dcf496a7b9.bb2746aad9 > div.d4924c9e74 > div:nth-child(5) > div.c066246e13 > div.c1edfbabcb > div > div.b1037148f8.c730b02848 > div.a4b53081e1 > div > div.da8b337763 > a")
                print(hotels)
                for hotel in hotels:
                    link = hotel.get_attribute("href")
                    driver.get(link)
                    apart_select = func.find_element(driver, By.CLASS_NAME, "hprt-nos-select")
                    apart = Select(apart_select)
                    apart.select_by_index(1)
                    driver.find_element(By.CLASS_NAME, "js-reservation-button").click()
                    sleep(1)
                    func.find_element(driver, By.ID, "firstname").send_keys(account["first_name"])
                    sleep(0.5)
                    func.find_element(driver, By.ID, "lastname").send_keys(account["last_name"])
                    sleep(1)
                    func.find_element(driver, By.ID, "cc1").send_keys("Albania")
                    sleep(0.3)
                    func.find_element(driver, By.ID, "phone").send_keys("437481753")
                    sleep(1)
                    time = func.find_element(driver, By.CLASS_NAME, "bui-list__description").text
                    match_time = re.search(r'\d+:\d+', time)
                    if match_time:
                        # Extract the matched numbers
                        booking_time = match_time.group()
                        print(booking_time)  # Output: 14:00
                    else:
                        print("No numbers found")
                    sleep(0.5)
                    func.find_element(driver, By.ID, "checkin_eta_hour").send_keys(booking_time)
                    sleep(0.5)
                    func.find_element(driver, By.CLASS_NAME, "e2e-bp-submit-button--next-step").click()
                    sleep(2)
                    # try:
                    #     func.find_element(driver, By.CSS_SELECTOR, "#cc_type").click()
                    #     sleep(1)
                    #     # func.find_element(driver, By.CSS_SELECTOR, "#cc_number").send_keys("5425233430109903")
                    #     # sleep(1)
                    #     # card_element = func.find_element(driver, By.CSS_SELECTOR, "#cc_type")
                    #     # card = Select(card_element)
                    #     # card.select_by_index(1) 
                    #     # sleep(1)
                    #     # month_element = func.find_element(driver, By.CSS_SELECTOR, "#cc_month")
                    #     # expire = Select(month_element)
                    #     # expire.select_by_index(current_month-1)
                    #     # func.find_element(driver, By.CLASS_NAME,"js-bp-submit-button--complete-booking").click()
                    #     # sleep(5)
                    # except:
                    func.find_element(driver, By.CLASS_NAME,"js-bp-submit-button--complete-booking").click()
                    sleep(5)
            else:
                # elem_table = func.find_element(driver, By.XPATH, '//*[@id="calendar-searchboxdatepicker"]/div/div[1]/div/div[1]')
                # print("calendar 1: ", current_date, elem_table)
                for row in calenders[0].find_elements(By.XPATH, './/tr'):
                    for cell in row.find_elements(By.XPATH, ".//td"):
                        if (cell.text == str(current_date)):
                            cell.click()
                            sleep(2)
                            print("Date Clicked!")
                            break
                # elem_table1 = func.find_element(driver, By.XPATH, '//*[@id="calendar-searchboxdatepicker"]/div/div[1]/div/div[2]')
                # print("calendar 2: ", current_date, elem_table1)
                for row in calenders[1].find_elements(By.XPATH, './/tr'):
                    for cell in row.find_elements(By.XPATH, ".//td"):
                        if (cell.text == str(current_date + 5 - 28)):
                            cell.click()
                            sleep(2)
                            print("Date Clicked!")
                            break
                func.find_element(driver, By.XPATH, '//*[@id="indexsearch"]/div[2]/div/form/div[1]/div[4]/button').click()
        if account["registered"] == True:
            sleep(2)
            func.find_element(driver, By.ID, "username").send_keys(account["email"])
            sleep(0.3)
            func.find_element(driver, By.CSS_SELECTOR, "#root > div > div > div.app > div.access-container.bui_font_body > div > div > div > div > div > div > div > form > div.Vw55_aACpYkyD1luIfis.cQj98l8L_Fc_IXYCWd4I.kBoHgdoepdx0bTMKriS3 > div:nth-child(2) > button").click()
            sleep(0.5)
            func.find_element(driver, By.CSS_SELECTOR, "#password").send_keys(password)
            sleep(0.3)
            func.find_element(driver, By.CSS_SELECTOR, "#root > div > div > div.app > div.access-container.bui_font_body > div > div > div > div > div > div > div > form > div > div:nth-child(3) > div > button").click()
            print("Successfully Logined!")
            sleep(10)
            func.find_element(driver, By.CSS_SELECTOR, "#\:rg\:").send_keys("Tirana")
            sleep(1)
            func.find_element(driver, By.CSS_SELECTOR, "#indexsearch > div.hero-banner-searchbox > div > form > div.ffb9c3d6a3.c9a7790c31.e691439f9a > div:nth-child(2) > div > div").click()
            sleep(2)
            calenders = func.find_elements(driver, By.CLASS_NAME, 'd358556c65')
            print(calenders)

            if current_date + 4 <= 31:
                # elem_table = func.find_element(driver, By.XPATH, '//*[@id="calendar-searchboxdatepicker"]/div/div[1]/div/div[1]')
                # print("calendar 1: ", current_date, elem_table)
                start_date_found = False
                end_date = current_date + 4
                # Loop through the rows and cells to find and click the cells for the date range
                for row in calenders[0].find_elements(By.XPATH, './/tr'):
                    for cell in row.find_elements(By.XPATH, ".//td"):
                        if cell.text == str(current_date):
                            start_date_found = True
                            cell.click()
                            sleep(2)
                            print("Start Date Clicked:", cell.text)

                        if start_date_found and cell.text == str(end_date):
                            cell.click()
                            print("End Date Clicked:", cell.text)
                            sleep(2)
                        break
                func.find_element(driver, By.XPATH, '//*[@id="indexsearch"]/div[2]/div/form/div[1]/div[4]/button').click()
                sleep(15)
                hotels = driver.find_elements(By.CSS_SELECTOR, "#bodyconstraint-inner > div:nth-child(10) > div > div.af5895d4b2 > div.df7e6ba27d > div.bcbf33c5c3 > div.dcf496a7b9.bb2746aad9 > div.d4924c9e74 > div:nth-child(5) > div.c066246e13 > div.c1edfbabcb > div > div.b1037148f8.c730b02848 > div.a4b53081e1 > div > div.da8b337763 > a")
                print(hotels)
                for hotel in hotels:
                    link = hotel.get_attribute("href")
                    driver.get(link)
                    apart_select = func.find_element(driver, By.CLASS_NAME, "hprt-nos-select")
                    apart = Select(apart_select)
                    apart.select_by_index(1)
                    driver.find_element(By.CLASS_NAME, "js-reservation-button").click()
                    sleep(1)
                    func.find_element(driver, By.ID, "firstname").send_keys(account["first_name"])
                    sleep(0.5)
                    func.find_element(driver, By.ID, "lastname").send_keys(account["last_name"])
                    sleep(1)
                    func.find_element(driver, By.ID, "cc1").send_keys("Albania")
                    sleep(0.3)
                    func.find_element(driver, By.ID, "phone").send_keys("437481753")
                    sleep(1)
                    time = func.find_element(driver, By.CLASS_NAME, "bui-list__description").text
                    match_time = re.search(r'\d+:\d+', time)
                    if match_time:
                        # Extract the matched numbers
                        booking_time = match_time.group()
                        print(booking_time)  # Output: 14:00
                    else:
                        print("No numbers found")
                    sleep(0.5)
                    func.find_element(driver, By.ID, "checkin_eta_hour").send_keys(booking_time)
                    sleep(0.5)
                    func.find_element(driver, By.CLASS_NAME, "e2e-bp-submit-button--next-step").click()
                    sleep(2)
                    # try:
                    #     func.find_element(driver, By.CSS_SELECTOR, "#cc_type").click()
                    #     sleep(1)
                    #     # func.find_element(driver, By.CSS_SELECTOR, "#cc_number").send_keys("5425233430109903")
                    #     # sleep(1)
                    #     # card_element = func.find_element(driver, By.CSS_SELECTOR, "#cc_type")
                    #     # card = Select(card_element)
                    #     # card.select_by_index(1) 
                    #     # sleep(1)
                    #     # month_element = func.find_element(driver, By.CSS_SELECTOR, "#cc_month")
                    #     # expire = Select(month_element)
                    #     # expire.select_by_index(current_month-1)
                    #     # func.find_element(driver, By.CLASS_NAME,"js-bp-submit-button--complete-booking").click()
                    #     # sleep(5)
                    # except:
                    func.find_element(driver, By.CLASS_NAME,"js-bp-submit-button--complete-booking").click()
                    sleep(5)
            else:
                # elem_table = func.find_element(driver, By.XPATH, '//*[@id="calendar-searchboxdatepicker"]/div/div[1]/div/div[1]')
                # print("calendar 1: ", current_date, elem_table)
                for row in calenders[0].find_elements(By.XPATH, './/tr'):
                    for cell in row.find_elements(By.XPATH, ".//td"):
                        if (cell.text == str(current_date)):
                            cell.click()
                            sleep(2)
                            print("Date Clicked!")
                            break
                # elem_table1 = func.find_element(driver, By.XPATH, '//*[@id="calendar-searchboxdatepicker"]/div/div[1]/div/div[2]')
                # print("calendar 2: ", current_date, elem_table1)
                for row in calenders[1].find_elements(By.XPATH, './/tr'):
                    for cell in row.find_elements(By.XPATH, ".//td"):
                        if (cell.text == str(current_date + 5 - 28)):
                            cell.click()
                            sleep(2)
                            print("Date Clicked!")
                            break
                func.find_element(driver, By.XPATH, '//*[@id="indexsearch"]/div[2]/div/form/div[1]/div[4]/button').click()
        # func.wait_url(driver, "https://account.booking.com/mysettings")         

if __name__ == "__main__":
    # import accounts
    accounts = []
    with open("accounts.json", "r") as file:
        accounts = json.load(file)
        print(accounts)
    
    submit(accounts)

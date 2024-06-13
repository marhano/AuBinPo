from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("http://binpo.paybps.ovpn/login?&page=%2Fmain%2F")
driver.maximize_window() 
time.sleep(2)

username = driver.find_element(By.ID, "frmuser")
username.clear()
username.send_keys("binpo.edgaffud")

password = driver.find_element(By.ID, "frmpass")
password.clear()
password.send_keys("56Z3aSc9zg")

submit = driver.find_element(By.ID, "submit")
submit.click()

driver.get("http://binpo.paybps.ovpn/intranet/panels/helpdesk_edit_workflow.php?id=110")


#Select Field
driver.find_element(By.ID, "new_field_symname").click()
option_id = "//option[@value='actions_7']"
driver.find_element(By.XPATH, option_id).click()

original_window = driver.current_window_handle
#Add Rule For This Field
driver.find_element(By.XPATH, "//input[@type='submit']").click()

names = ["A", "E", "X"]
max_values = {"A": 3, "B": 5, "C": 6}

for window_handle in driver.window_handles:
    if window_handle != original_window:
        new_window = window_handle
        break

driver.switch_to.window(new_window)
time.sleep(2)

#Start Loop
for x in names:
    if x == 'A' or x == 'B' or x == 'C':
        max_value = max_values[x]
        for a in range(1, max_value + 1):
            #Field Condition Name
            condition_select = "//select[@name='rule_id']"
            driver.find_element(By.XPATH, condition_select).click()
            time.sleep(2)
            condition_element = f"//select[@name='rule_id']/option[text()='Actions#7__{x}{a}']"
            driver.find_element(By.XPATH, condition_element).click()
            time.sleep(2)
            
            for a in range(1, 3):
                #Role Name
                driver.find_element(By.ID, "roleList").click()
                role_option = f"//select[@id='roleList']/option[{a}]"
                driver.find_element(By.XPATH, role_option).click()
                time.sleep(2)
                if(a == 1):
                    #checkbox
                    driver.find_element(By.NAME, "not_used_checkbox397").click()
                    #select
                    fields_value1 = "//select[@id='options_select397']/option[1]"
                    fields_value2 = "//select[@id='options_select397']/option[2]"
                    option1 = driver.find_element(By.XPATH, fields_value1)
                    option2 = driver.find_element(By.XPATH, fields_value2)
                else:
                    #checkbox
                    driver.find_element(By.NAME, "not_used_checkbox398").click() 
                    #select
                    fields_value1 = "//select[@id='options_select398']/option[1]"
                    fields_value2 = "//select[@id='options_select398']/option[2]"
                    option1 = driver.find_element(By.XPATH, fields_value1)
                    option2 = driver.find_element(By.XPATH, fields_value2)

                time.sleep(2)
                #Click ctrl key
                action = ActionChains(driver)
                action.key_down(Keys.CONTROL).click(option1).click(option2).key_up(Keys.CONTROL).perform()
                time.sleep(2)

            #Add/Change Rule
            submit_button = "//input[@type='submit']"
            driver.find_element(By.XPATH, submit_button).click()
            time.sleep(5)
            #Add New Rule
            new_rule = "//td/span[text()='actions_7']/ancestor::tr/following-sibling::tr//div[@id='new_link']/a[1]"
            driver.find_element(By.XPATH, new_rule).click()
            #End Loop
input()
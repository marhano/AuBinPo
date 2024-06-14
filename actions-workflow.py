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

for window_handle in driver.window_handles:
    if window_handle != original_window:
        new_window = window_handle
        break

driver.switch_to.window(new_window)
time.sleep(2)

names = ["A", "E", "X"]
iterations = [1, 2, 3]
max_values = {"A": 2, "B": 2, "C": 2}
#Start Loop
for name in names:
    if name == 'A' or name == 'B' or name == 'C':
        max_value = max_values[name]
        for iterations in range(1, max_value + 1):
            #Field Condition Name
            condition_select = "//select[@name='rule_id']"
            driver.find_element(By.XPATH, condition_select).click()
            time.sleep(2)
            condition_element = f"//select[@name='rule_id']/option[text()='Actions#7__{name}{iterations}']"
            driver.find_element(By.XPATH, condition_element).click()
            time.sleep(2)

            number_of_role = 2
            for role in range(1, number_of_role + 1):
                #Role Name
                driver.find_element(By.ID, "roleList").click()
                role_option = f"//select[@id='roleList']/option[{role}]"
                driver.find_element(By.XPATH, role_option).click()
                time.sleep(2)

                option1_user = driver.find_element(By.XPATH, "//select[@id='options_select397']/option[1]") #Used inappropriately
                option2_user = driver.find_element(By.XPATH, "//select[@id='options_select397']/option[2]") #Observed
                option3_user = driver.find_element(By.XPATH, "//select[@id='options_select397']/option[3]") #Altered
                option4_user = driver.find_element(By.XPATH, "//select[@id='options_select397']/option[4]") #Lost
                option5_user = driver.find_element(By.XPATH, "//select[@id='options_select397']/option[5]") #Manipulated
                option6_user = driver.find_element(By.XPATH, "//select[@id='options_select397']/option[6]") #Overloaded
                option7_user = driver.find_element(By.XPATH, "//select[@id='options_select397']/option[7]") #Damaged

                option1_tm = driver.find_element(By.XPATH, "//select[@id='options_select398']/option[1]") #Used inappropriately
                option2_tm = driver.find_element(By.XPATH, "//select[@id='options_select398']/option[2]") #Observed
                option3_tm = driver.find_element(By.XPATH, "//select[@id='options_select398']/option[3]") #Altered
                option4_tm = driver.find_element(By.XPATH, "//select[@id='options_select398']/option[4]") #Lost
                option5_tm = driver.find_element(By.XPATH, "//select[@id='options_select398']/option[5]") #Manipulated
                option6_tm = driver.find_element(By.XPATH, "//select[@id='options_select398']/option[6]") #Overloaded
                option7_tm = driver.find_element(By.XPATH, "//select[@id='options_select398']/option[7]") #Damaged
                if(name == "A" and iterations == 1 or role == 1):
                    driver.find_element(By.NAME, "not_used_checkbox397").click()
                    action = ActionChains(driver)
                    action.key_down(Keys.CONTROL).click(option1_user).click(option2_user).click(option3_user).click(option4_user).key_up(Keys.CONTROL).perform()
                else:
                    driver.find_element(By.NAME, "not_used_checkbox398").click()
                    action = ActionChains(driver)
                    action.key_down(Keys.CONTROL).click(option1_tm).click(option2_tm).click(option3_tm).click(option4_tm).key_up(Keys.CONTROL).perform()
                    time.sleep(2)
            #Add/Change Rule
            submit_button = "//input[@type='submit']"
            driver.find_element(By.XPATH, submit_button).click()
            time.sleep(5)
            driver.switch_to.window(original_window)
            original_window = driver.current_window_handle
            #Add New Rule
            new_rule = "//td/span[text()='actions_7']/ancestor::tr/following-sibling::tr//div[@id='new_link']/a[1]"
            driver.find_element(By.XPATH, new_rule).click()

            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    new_window = window_handle
                    break
            driver.switch_to.window(new_window)
            #End Loop
input()
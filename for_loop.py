from selenium import webdriver
from selenium.webdriver.common.by import By
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

driver.get("http://binpo.paybps.ovpn/intranet/panels/helpdesk_edit_rules.php?id=110")

names = ["A", "B", "C"]
max_values = {"A": 5, "B": 5, "C": 6}
value_opt = [1, 2, 3]

for x, y in zip(names, value_opt):
    if x == "A" and y == 1 or x == "B" and y == 2 or x == "C" and y == 3:
        max_value = max_values[x]
        for a in range(1, max_value + 1):
            #Add New Condition Set Button
            driver.find_element(By.NAME, "add_rule_link").click()
            #Condition Name
            condition_name = driver.find_element(By.ID, "rule_name")
            condition_name.send_keys(f"Actions#7__{x}{a}") 
            #Three Checkbox
            driver.find_element(By.ID, "for_fields_rights").click()
            driver.find_element(By.ID, "for_workflow").click()
            driver.find_element(By.ID, "for_sla").click()
            time.sleep(2)
            
            #Content
            threats_xpath = "//input[@value='threats_that_can_lead_to__7']"
            threats_value = f"{threats_xpath}//ancestor::tr//select[@class='form-control']/option[{y}]"
            supporting_xpath = "//input[@value='supporting_assets_7']"
            supporting_value = f"{supporting_xpath}//ancestor::tr//select[@class='form-control']/option[{a}]"
            submit_button = "//input[@value='Save']"

            #Threats that leads to
            driver.find_element(By.XPATH, threats_xpath).click()
            driver.find_element(By.XPATH, threats_value).click()
            time.sleep(2)
            #Supporting Assets
            driver.find_element(By.XPATH, supporting_xpath).click()
            driver.find_element(By.XPATH, 
            supporting_value).click()
            time.sleep(2)
            #Sumbit
            driver.find_element(By.XPATH, submit_button).click()
            time.sleep(2)
input()
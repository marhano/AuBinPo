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
driver.find_element(By.NAME, "add_rule_link").click()

#Condition Name
conditionname = driver.find_element(By.NAME, "add_rule_link")
conditionname.send_keys("Actions#1__A1")

#Three Checkbox
driver.find_element(By.ID, "for_fields_rights").click()
driver.find_element(By.ID, "for_workflow").click()
driver.find_element(By.ID, "for_sla").click()

threats_xpath = "//input[@value='threats_that_can_lead_to_2']"
threats_value = f"{threats_xpath}//ancestor::tr//select[@class='form-control']/option[1]"
supporting_xpath = "//input[@value='supporting_assets2']"
supporting_value = f"{supporting_xpath}//ancestor::tr//select[@class='form-control']/option[1]"
action_xpath = "//input[@value='actions2']"
action_value = f"{action_xpath}//ancestor::tr//select[@class='form-control']/option[1]"
submit_button = "//input[@value='Save']"

#Threats that leads to
driver.find_element(By.XPATH, threats_xpath).click()
driver.find_element(By.XPATH, threats_value).click()
time.sleep(5)
#Supporting Assets
driver.find_element(By.XPATH, supporting_xpath).click()
driver.find_element(By.XPATH, supporting_value).click()
time.sleep(5)
#Actions
driver.find_element(By.XPATH, action_xpath).click()
driver.find_element(By.XPATH, action_value).click()
#Submit
driver.find_element(By.XPATH, submit_button).click()

input()
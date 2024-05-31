import constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
import curses
from cursesmenu import CursesMenu
from cursesmenu.items import FunctionItem, SubmenuItem
from ui.forms import AddNewFieldConditionForm
import subprocess

class Infographics(webdriver.Chrome):
    def __init__(self, teardown=False):
        self.teardown = teardown
        super(Infographics, self).__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def login_user(self, username, password):
        self.get(const.BASE_URL)
        el_username = self.find_element(By.ID, "frmuser")
        el_username.send_keys(username)
        el_password = self.find_element(By.ID, "frmpass")
        el_password.send_keys(password)
        self.find_element(By.ID, "submit").click()

    def add_new_condition(self):
        self.find_element(By.NAME, "add_rule_link").click()

        rule_name, field_condition = add_new_field_condition()

        el_rule_name = self.find_element(By.ID, "rule_name")
        el_rule_name.send_keys(rule_name)

        # CHECKBOXES
        self.find_element(By.ID, "for_fields_rights").click()
        self.find_element(By.ID, "for_workflow").click()
        self.find_element(By.ID, "for_sla").click()

        for fc in field_condition:
            parent = self.find_element(By.XPATH, f"//input[contains(@value, '{fc[0]}')]")
            parent.click()
            if fc[1] == "text==":
                checkbox = parent.find_element(By.XPATH, f"ancestor::tr//input[contains(@id, 'equal_checkbox')]")
                checkbox.click()
                textbox = checkbox.find_element(By.XPATH, f"ancestor::div[@class='form-group row']//input[contains(@id, 'input_equal')]")
                textbox.send_keys(fc[2])
            else:
                checkbox = parent.find_element(By.XPATH, f"ancestor::tr//input[contains(@id, 'not_equal')]")
                checkbox.click()
                textbox = checkbox.find_element(By.XPATH, f"ancestor::div[@class='form-group row']//input[contains(@id, 'input_not_equal')]")
                textbox.send_keys(fc[2])

    def edit_condition(self):
        pass

def add_new_field_condition():
    def wrapper(stdscr):
        new_field_condition = AddNewFieldConditionForm(stdscr)
        return new_field_condition.run()
    
    return curses.wrapper(wrapper)

    
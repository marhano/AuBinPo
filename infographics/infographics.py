import constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
#from ui.forms import AddNewFieldConditionForm
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import winsound

class Infographics(webdriver.Chrome):
    def __init__(self, teardown=False):
        self.teardown = teardown
        self.LAST_FIELD_POS = const.INIT_POS
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

    def ob_class_b_pas(self):
        self.get(const.OB_CLASS_B)
        cont_btn = self.find_element(By.NAME, 'continue_edit_fields_link')
        cont_btn.click()

        data = read_json(const.JSON_PATH_OBPAS)

        terminalIDs = ['A', 'B', 'C', 'D', 'E', 'F']
        paymentTerminalIDs = ['1', '2', '3', '4', '5', '6']
        BRANCH = 2
        TERMINAL = 2
        PAYMENT_TERMINAL = 2

        checkbox_data = {
            "name": "Terminal",
            "alt_name": False,
            "input_type": "checkbox",
            "required": False,
            "disabled": False,
            "reload": True,
            "separate_cells": True,
            "label_above_input_field": False,
            "group_with_next": False,
            "label_size": 1,
            "input_size": 1,
            "field_label_css": "checkbox_label",
            "field_value_css": "checkbox_box",
            "optional_hint": False
        }

        create_field(self, {"input_type": "label", "name": "Branch 3", "optional_hint": False, "field_label_css": False, "label_size": 1, "group_with_next": False })
        for i in range(1, BRANCH + 1):

            create_section(self, {"name": "Branch", "visible_header": False, "field_label_css": "main_branch" }, i)
            for branch in data:

                if isinstance(branch, list):

                    for j, terminalID in enumerate(terminalIDs[:TERMINAL]):
                        create_section(self, {"name": "Terminal", "visible_header": False, "field_label_css": "terminal_section" }, f"{i}{terminalID}")
                        checkbox_data['name'] = "Terminal"
                        create_field(self, checkbox_data, f"{i}{terminalID}")

                        for terminal in branch:

                            if isinstance(terminal, list):
                                create_section(self, {"name": "Payment Terminal", "visible_header": False, "field_label_css": "payment_terminal_section" }, f"{i}{terminalID}")

                                for k, paymentTerminalID in enumerate(paymentTerminalIDs[:PAYMENT_TERMINAL]):
                                    checkbox_data['name'] = "Payment Terminal"
                                    create_field(self, checkbox_data, f"{i}{terminalID}{paymentTerminalID}")

                                    for paymentTerminal in terminal:
                                        create_field(self, paymentTerminal, f"{i}{terminalID}{paymentTerminalID}")
                                        if paymentTerminal['name'] != "Payment Partner":
                                            edit_field(self, paymentTerminal, f"{i}{terminalID}{paymentTerminalID}")
                                if (j + 1) == TERMINAL & i != BRANCH:
                                    checkbox_data['name'] = "Branch"
                                    create_field(self, checkbox_data, f"{str(i + 1)}")
                            else:
                                create_field(self, terminal, f"{i}{terminalID}")
                else:
                    create_field(self, branch, i)

    def ob_class_b_asi(self):
        self.get(const.OB_CLASS_B)
        cont_btn = self.find_element(By.NAME, 'continue_edit_fields_link')
        cont_btn.click()

        data = read_json(const.JSON_PATH_OBASI)
        # print(data)
        ASI = 10

        for i in range(1, ASI + 1):
            for asi in data:
                create_field(self, asi, i)
                    
    def ob_class_b_account_user(self):
        self.get(const.OB_CLASS_B)
        # edit_btn = self.find_element(By.NAME, 'edit_fields_link')
        # edit_btn.click()
        cont_btn = self.find_element(By.NAME, 'continue_edit_fields_link')
        cont_btn.click()

        data = read_json(const.JSON_PATH_OBAU)
        
        accounts = 10

        for i in range(1, accounts + 1):
            for account in data:
                create_field(self, account, i)
                if account['name'] == "Full Name User":
                    edit_field(self, account, i, "list")

# tested on(textfield, select, label, checkbox, multiple_checkbox)
def create_field(self, options, _index=None):
    if const.SWITCH == False:
        return
    
    def send_keys(id, option, index=None):
        form_field = self.find_element(By.ID, id)
        if option:
            form_field.clear()
            if index:
                form_field.send_keys(f"{option} {index}")
                return
            
            form_field.send_keys(option)

        else:
            form_field.clear()
    
    def click_element(id, option):
        form_field = self.find_element(By.ID, id)
    
        if form_field.is_selected() != option:
            form_field.click()
    
    attempts = False

    while attempts == False:
        try:
            if options['input_type'] == "multiple_checkboxes":
                form_field = self.find_element(By.XPATH, "//div[@class='btn-group']/a[@title='Checkbox']")
                form_field.click()

                field_type_select = self.find_element(By.XPATH, "//select[@id='field_type_select']")
                field_type_select.click()
                field_type_option = self.find_element(By.XPATH, "//select[@id='field_type_select']/option[@value='22']")
                field_type_option.click()
            else:
                form_field = self.find_element(By.XPATH, f"//div[@class='btn-group']/a[@title='{format_text(options['input_type'])}']")
                form_field.click()

            self.implicitly_wait(5)

            # properties
            name = options['alt_name'] if options.get('alt_name') else options['name']
            if _index:
                send_keys("field_label", name, _index)
            else:
                send_keys("field_label", name)
            send_keys("field_description", options['optional_hint'])

            if options['input_type'] != "label":
                click_element("field_required", options['required'])
                click_element("field_disabled", options['disabled'])
                click_element("field_dynamic", options['reload'])

            if options['input_type'] == "select" or options['input_type'] == "multiple_checkboxes":
                actions = ActionChains(self)
                field_values = self.find_element(By.ID, 'field_values')
                actions.click(field_values)
                for value in options['values']:
                    actions.send_keys(value)
                    actions.send_keys(Keys.ENTER)
                actions.perform()

                click_element("no_default", options['show_please_select_no_default'])

            # style
            change_tab(self, "Style")
            change_field_position(self)

            send_keys("field_style", options['field_label_css'])
            send_keys("field_title_size", options['label_size'])
            click_element("field_group_cells", options['group_with_next'])

            if options['input_type'] != "label":
                send_keys("field_style2", options['field_value_css'])
                send_keys("field_field_size", options['input_size'])
                click_element("field_two_cells", options['separate_cells'])
                click_element("field_on_top", options['label_above_input_field'])
            
            if options['input_type'] == "multiple_checkboxes":
                click_element("field_inline_layout", options['horizontal_layout'])

            # save
            save_btn = self.find_element(By.ID, "save_field_button")
            save_btn.click()
            if options['input_type'] == "select":
                self.implicitly_wait(5)
                save_btn = self.find_element(By.ID, "save_field_button")
                save_btn.click()

            print(f'\033[92m{options["name"]} {_index}\033[0m')
            attempts = True

            break

        except Exception as e:
            print(f'\033[91mAn error occurred: Create field, {options["name"]} {e}. Retrying...\033[0m')
            play_alert_sound()
            close_edit_field_modal(self)
            time.sleep(5)
    
def create_section(self, options, _index=None):
    if const.SWITCH == False:
        return
    
    def send_keys(id, option, index=None):
        form_field = self.find_element(By.ID, id)
        if option:
            form_field.clear()
            if index:
                form_field.send_keys(f"{option} {index}")
                return
            
            form_field.send_keys(option)

        else:
            form_field.clear()
    
    def click_element(id, option):
        form_field = self.find_element(By.ID, id)
    
        if form_field.is_selected() != option:
            form_field.click()
    
    attempts = False
    
    while attempts == False:
        try:
            self.implicitly_wait(5)
            form_field = self.find_element(By.XPATH, "//div[@class='btn-group']/a[@title='Add a new section']")
            form_field.click()

            self.implicitly_wait(5)

            send_keys("section_label", options['name'], _index) if _index else send_keys("section_label", options['name'])
            click_element("visible_checkbox", options['visible_header'])

            change_field_position(self)

            send_keys("section_style", options['field_label_css'])

            section_form = self.find_element(By.ID, 'edit_section_form')
            save_btn = section_form.find_element(By.XPATH, "//div[@class='modal-footer']/input[@class='btn btn-primary']")
            save_btn.click()

            break

        except Exception as e:
            print(f'\033[91mAn error occurred: Create section, {options["name"]} {e}. Retrying...\033[0m')
            play_alert_sound()
            close_edit_field_modal(self)
            time.sleep(5)

# deprecated
def edit_field(self, option, _index=None, custom=None):
    if const.SWITCH == False:
        return
    
    attempts = False

    while attempts == False:
        try:
            self.implicitly_wait(5)

            if option["alt_name"]:
                element_id = f'_100__field_{convert_to_id(option["alt_name"])}'
            else:
                element_id = f'_100__field_{convert_to_id(option["name"])}'

            if _index:
                element_id += f'_{convert_to_id(str(_index))}'
            edit_btn = self.find_element(By.XPATH, f"//label[@for='{element_id}']/a")
            self.execute_script("arguments[0].scrollIntoView({ block: 'center' });", edit_btn)
            edit_btn.click()

            self.implicitly_wait(5)

            if custom == "list":
                field_input = self.find_element(By.ID, "field_label")
                field_input.clear()
                field_input.send_keys(f'{_index}')
            else:
                field_input = self.find_element(By.ID, "field_label")
                field_input.clear()
                field_input.send_keys(f'{option["name"]} {_index}')

            save_btn = self.find_element(By.ID, "save_field_button")
            save_btn.click()

            attempts = True

            break

        except Exception as e:
            print(f'\033[93mAn error occurred: Edit field, {convert_to_id(option["name"])} {e}. Retrying...\033[0m')
            play_alert_sound()
            time.sleep(5)

# HELPER METHODS
def play_alert_sound():
    if const.ERROR_ALERT:
        winsound.Beep(1000, 500)

def read_json(json_path):
    with open(json_path, 'r') as ob_obj:
        data = json.load(ob_obj)
    
    return data

def convert_to_id(string):
    return string.lower().replace(' ', '_')

def format_text(label):
    label = label.replace('_', ' ')
    label = label.title()
    
    return label

def change_tab(self, tab_name):
    style_tab = self.find_element(By.XPATH, f"//a[text()='{tab_name}']")
    style_tab.click()

def change_field_position(self):
    if self.LAST_FIELD_POS:
        try:
            field_position = self.find_element(By.ID, "field_number_select")
            field_position.click()
            field_position_option = self.find_element(By.XPATH, f"//select[@id='field_number_select']/option[@value='{self.LAST_FIELD_POS}']")
            field_position_option.click()
        except:
            field_position = self.find_element(By.ID, "section_position")
            field_position.click()
            field_position_option = self.find_element(By.XPATH, f"//select[@id='section_position']/option[@value='{self.LAST_FIELD_POS}']")
            field_position_option.click()
        finally:
            self.LAST_FIELD_POS += 1

def close_edit_field_modal(self):
    try:
        close_button = self.find_element(By.XPATH, "//form[@name='edit_field_form']//button[@class='close']")
        close_button.click()
    except Exception as e:
        print(f"Error closing modal: {e}")
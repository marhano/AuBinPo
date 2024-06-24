import constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from ui.forms import AddNewFieldConditionForm
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

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

    def checkout_form(self):
        self.get(const.OB_CLASS_B)
        cont_btn = self.find_element(By.NAME, 'continue_edit_fields_link')
        cont_btn.click()

        data = read_json()

        terminalIDs = ['A', 'B', 'C', 'D', 'E', 'F']
        paymentTerminalIDs = ['a', 'b', 'c', 'd', 'e', 'f']

        BRANCH = 1
        TERMINAL = 3
        PAYMENT_TERMINAL = 3

        create_label(self, 'Branch 1')
        for i in range(1, BRANCH + 1):
            create_section(self, 'Branch ' + str(i), 'main_branch')
            for key, value in data['branch'].items():
                
                if key == 'terminal':
                    for j, terminalId in enumerate(terminalIDs[:TERMINAL]):
                        terminal_section_name = f'Terminal {i}{terminalId}'
                        print(terminal_section_name)
                        create_section(self, terminal_section_name, 'terminal_section')
                        create_checkbox(self, terminal_section_name)
                        for terminalKey, terminalValue in value.items():
                            
                            if terminalKey == 'payment_terminal':
                                payment_terminal_section_name = f'Payment Terminal {i}{terminalId}'
                                print('     '+payment_terminal_section_name)
                                create_section(self, payment_terminal_section_name, 'payment_terminal_section')
                                
                                for k, paymentTerminalID in enumerate(paymentTerminalIDs[:PAYMENT_TERMINAL]):
                                    payment_terminal_name = f'Payment Terminal {i}{terminalId}{paymentTerminalID}'
                                    print('          '+payment_terminal_name)
                                    create_checkbox(self, payment_terminal_name)
                                    
                                    for paymentTerminalKey, paymentTerminalValue in terminalValue.items():
                                        field_name = f'{paymentTerminalKey} {i}{terminalId}{paymentTerminalID}'
                                        print('          '+'\033[92m'+field_name+'\033[0m')

                                        new_label = paymentTerminalKey
                                        if paymentTerminalKey != 'payment_partner':
                                            new_label = replace_pt_with_payment_terminal(paymentTerminalKey)

                                        if paymentTerminalValue['input_type'] == 'textfield':
                                            create_textfield(self, field_name, paymentTerminalValue)
                                            edit_field_label(self, field_name, new_label)
                                        elif paymentTerminalValue['input_type'] == 'select':
                                            create_select(self, field_name, paymentTerminalValue)
                                            edit_field_label(self, field_name, new_label)
                                        elif paymentTerminalValue['input_type'] == 'multiple_checkboxes':
                                            create_multiple_checkboxes(self, field_name, paymentTerminalValue)
                                            edit_field_label(self, field_name, new_label)
                                if (j + 1) == TERMINAL & i != BRANCH :
                                    print("BRANCH NAME CHECKBOX")
                                    create_checkbox(self, 'Branch ' + str((i + 1)))
                            else:
                                field_name = f'{terminalKey} {i}{terminalId}'
                                print('\033[96m'+'     '+field_name+'\033[0m')

                                if terminalValue['input_type'] == 'textfield':
                                    create_textfield(self, field_name, terminalValue)
                                    edit_field_label(self, field_name, terminalKey)
                                elif terminalValue['input_type'] == 'select':
                                    create_select(self, field_name, terminalValue)
                                    edit_field_label(self, field_name, terminalKey)
                else:
                    field_name = f'{key} {i}'
                    print(f"\033[94m{field_name}\033[0m")
                    if value['input_type'] == 'textfield':
                        create_textfield(self, field_name, value)
                        edit_field_label(self, field_name, key)
                    elif value['input_type'] == 'select':
                        create_select(self, field_name, value)
                        edit_field_label(self, field_name, key)


def create_label(self, label):
    if const.SWITCH == False:
        return

    attempts = 0

    while attempts < const.MAX_RETRIES:
        try:
            form_field = self.find_element(By.XPATH, "//div[@class='btn-group']/a[@title='Label']")
            form_field.click()

            self.implicitly_wait(5)

            field_input = self.find_element(By.ID, "field_label")
            field_input.send_keys(format_text(label))

            change_tab(self, "Style")

            change_field_position(self)

            save_btn = self.find_element(By.ID, "save_field_button")
            save_btn.click()

            break

        except Exception as e:
            print(f'\033[91mAn error occurred: {label}. Retrying...\033[0m')
            attempts += 1
            close_edit_field_modal(self)
            time.sleep(2)
    if attempts == const.MAX_RETRIES:
        print(f"Failed to create label {label} after several attempts.")
    
def create_section(self, label, css):
    if const.SWITCH == False:
        return
    
    attempts = 0
    
    while attempts < const.MAX_RETRIES:
        try:
            self.implicitly_wait(5)
            form_field = self.find_element(By.XPATH, "//div[@class='btn-group']/a[@title='Add a new section']")
            form_field.click()

            self.implicitly_wait(5)

            field_input = self.find_element(By.ID, "section_label")
            field_input.clear()
            field_input.send_keys(label)

            visible_checkbox = self.find_element(By.ID, "visible_checkbox")
            visible_checkbox.click()

            change_field_position(self)

            style_css = self.find_element(By.ID, 'section_style')
            style_css.send_keys(css)

            section_form = self.find_element(By.ID, 'edit_section_form')
            save_btn = section_form.find_element(By.XPATH, "//div[@class='modal-footer']/input[@class='btn btn-primary']")
            save_btn.click()

            break

        except Exception as e:
            print(f'\033[91mAn error occurred: {label}. Retrying...\033[0m')
            attempts += 1
            close_edit_field_modal(self)
            time.sleep(2)
    if attempts == const.MAX_RETRIES:
        print(f"Failed to create section {label} after several attempts.")

def create_checkbox(self, label):
    if const.SWITCH == False:
        return
    
    attempts = 0

    while attempts < const.MAX_RETRIES:
        try:
            form_field = self.find_element(By.XPATH, "//div[@class='btn-group']/a[@title='Checkbox']")
            form_field.click()

            self.implicitly_wait(5)

            field_input = self.find_element(By.ID, "field_label")
            field_input.send_keys(label)

            reload_checkbox = self.find_element(By.ID, 'field_dynamic')
            reload_checkbox.click()

            change_tab(self, "Style")
            change_field_position(self)

            css_field_label = self.find_element(By.ID, 'field_style')
            css_field_label.clear()
            css_field_label.send_keys('checkbox_label')

            css_field_value = self.find_element(By.ID, 'field_style2')
            css_field_value.clear()
            css_field_value.send_keys('checkbox_box')

            separate_cells_checkbox = self.find_element(By.ID, 'field_two_cells')
            separate_cells_checkbox.click()

            save_btn = self.find_element(By.ID, "save_field_button")
            save_btn.click()

            break

        except Exception as e:
            print(f'\033[91mAn error occurred: {label}. Retrying...\033[0m')
            attempts += 1
            close_edit_field_modal(self)
            time.sleep(2)

    if attempts == const.MAX_RETRIES:
        print(f"Failed to create checkbox {label} after several attempts.")

def create_textfield(self, label, options):
    if const.SWITCH == False:
        return

    attempts = 0

    while attempts < const.MAX_RETRIES:
        try:
            form_field = self.find_element(By.XPATH, "//div[@class='btn-group']/a[@title='Textfield']")
            form_field.click()

            self.implicitly_wait(5)

            field_input = self.find_element(By.ID, "field_label")
            field_input.send_keys(format_text(label))

            #PROPERTIES
            if options['required']:
                required_checkbox = self.find_element(By.ID, 'field_required')
                required_checkbox.click()
            if options['disabled']:
                disabled_checkbox = self.find_element(By.ID, 'field_disabled')
                disabled_checkbox.click()
            if options['reload']:
                reload_checkbox = self.find_element(By.ID, 'field_dynamic')
                reload_checkbox.click()
            if options['optional_hint']:
                form_input = self.find_element(By.ID, 'field_description')
                form_input.clear()
                form_input.send_keys(options['optional_hint'])

            #STYLE
            change_tab(self, "Style")
            change_field_position(self)

            css_field_label = self.find_element(By.ID, 'field_style')
            css_field_label.clear()
            css_field_value = self.find_element(By.ID, 'field_style2')
            css_field_value.clear()

            if options['label_size']:
                form_input = self.find_element(By.ID, 'field_title_size')
                form_input.clear()
                form_input.send_keys(options['label_size'])
            if options['input_size']:
                form_input = self.find_element(By.ID, 'field_field_size')
                form_input.clear()
                form_input.send_keys(options['input_size'])
            if options['separate_cells']:
                form_checkbox = self.find_element(By.ID, 'field_two_cells')
                form_checkbox.click()
            else:
                form_checkbox = self.find_element(By.ID, 'field_two_cells')
                if form_checkbox.is_selected():
                    form_checkbox.click()
            if options['label_above_input_field']:
                form_checkbox = self.find_element(By.ID, 'field_on_top')
                form_checkbox.click()
            if options['group_with_next']:
                form_checkbox = self.find_element(By.ID, 'field_group_cells')
                form_checkbox.click()

            #SAVE
            save_btn = self.find_element(By.ID, "save_field_button")
            save_btn.click()

            break

        except Exception as e:
            print(f'\033[91mAn error occurred: {label}. Retrying...\033[0m')
            attempts += 1
            close_edit_field_modal(self)
            time.sleep(2)
            
    if attempts == const.MAX_RETRIES:
        print(f"Failed to create {options['input_type']} {label} after several attempts.")

def create_select(self, label, options):
    if const.SWITCH == False:
        return
    
    attempts = 0

    while attempts < const.MAX_RETRIES:
        try:
            form_field = self.find_element(By.XPATH, "//div[@class='btn-group']/a[@title='Select']")
            form_field.click()

            self.implicitly_wait(5)

            field_input = self.find_element(By.ID, "field_label")
            field_input.send_keys(format_text(label))

            #ACTIONS
            actions = ActionChains(self)

            #PROPERTIES
            field_values = self.find_element(By.ID, 'field_values')
            actions.click(field_values)
            for value in options['values']:
                actions.send_keys(value)
                actions.send_keys(Keys.ENTER)

            actions.perform()

            if options['show_please_select_no_default']:
                form_checkbox = self.find_element(By.ID, 'no_default')
                form_checkbox.click()
            if options['required']:
                form_checkbox = self.find_element(By.ID, 'field_required')
                form_checkbox.click()
            if options['disabled']:
                form_checkbox = self.find_element(By.ID, 'field_disabled')
                form_checkbox.click()
            if options['reload']:
                form_checkbox = self.find_element(By.ID, 'field_dynamic')
                form_checkbox.click()

            #STYLE
            change_tab(self, "Style")
            change_field_position(self)

            css_field_label = self.find_element(By.ID, 'field_style')
            css_field_label.clear()
            css_field_value = self.find_element(By.ID, 'field_style2')
            css_field_value.clear()

            if options['label_size']:
                form_input = self.find_element(By.ID, 'field_title_size')
                form_input.clear()
                form_input.send_keys(options['label_size'])
            if options['input_size']:
                form_input = self.find_element(By.ID, 'field_field_size')
                form_input.clear()
                form_input.send_keys(options['input_size'])
            if options['separate_cells']:
                form_checkbox = self.find_element(By.ID, 'field_two_cells')
                form_checkbox.click()
            else:
                form_checkbox = self.find_element(By.ID, 'field_two_cells')
                if form_checkbox.is_selected():
                    form_checkbox.click()

            if options['label_above_input_field']:
                form_checkbox = self.find_element(By.ID, 'field_on_top')
                form_checkbox.click()
            if options['group_with_next']:
                form_checkbox = self.find_element(By.ID, 'field_group_cells')
                form_checkbox.click()

            #SAVE
            save_btn = self.find_element(By.ID, "save_field_button")
            save_btn.click()
            self.implicitly_wait(5)
            save_btn = self.find_element(By.ID, "save_field_button")
            save_btn.click()

            break

        except Exception as e:
            print(f'\033[91mAn error occurred: {label}. Retrying...\033[0m')
            attempts += 1
            close_edit_field_modal(self)
            time.sleep(2)
            
    if attempts == const.MAX_RETRIES:
        print(f"Failed to create {options['input_type']} {label} after several attempts.")

def create_multiple_checkboxes(self, label, options):
    if const.SWITCH == False:
        return
    
    attempts = 0
    
    while attempts < const.MAX_RETRIES:
        try:
            form_field = self.find_element(By.XPATH, "//div[@class='btn-group']/a[@title='Checkbox']")
            form_field.click()

            self.implicitly_wait(5)

            field_type = self.find_element(By.XPATH, "//select[@id='field_type_select']")
            field_type.click()
            field_type_option = self.find_element(By.XPATH, "//select[@id='field_type_select']/option[@value='22']")
            field_type_option.click()

            field_input = self.find_element(By.ID, "field_label")
            field_input.send_keys(format_text(label))

            #ACTIONS
            actions = ActionChains(self)

            #PROPERTIES
            field_values = self.find_element(By.ID, 'field_values')
            actions.click(field_values)
            for value in options['values']:
                actions.send_keys(value)
                actions.send_keys(Keys.ENTER)

            actions.perform()

            if options['required']:
                form_checkbox = self.find_element(By.ID, 'field_required')
                form_checkbox.click()
            if options['disabled']:
                form_checkbox = self.find_element(By.ID, 'field_disabled')
                form_checkbox.click()
            if options['reload']:
                form_checkbox = self.find_element(By.ID, 'field_dynamic')
                form_checkbox.click()

            #STYLE
            change_tab(self, "Style")
            change_field_position(self)

            css_field_label = self.find_element(By.ID, 'field_style')
            css_field_label.clear()
            css_field_value = self.find_element(By.ID, 'field_style2')
            css_field_value.clear()
            if options['label_size']:
                form_input = self.find_element(By.ID, 'field_title_size')
                form_input.clear()
                form_input.send_keys(options['label_size'])
            if options['input_size']:
                form_input = self.find_element(By.ID, 'field_field_size')
                form_input.clear()
                form_input.send_keys(options['input_size'])
            if options['separate_cells']:
                form_checkbox = self.find_element(By.ID, 'field_two_cells')
                form_checkbox.click()
            if options['label_above_input_field']:
                form_checkbox = self.find_element(By.ID, 'field_on_top')
                form_checkbox.click()
            if options['group_with_next']:
                form_checkbox = self.find_element(By.ID, 'field_group_cells')
                form_checkbox.click()

            save_btn = self.find_element(By.ID, "save_field_button")
            save_btn.click()

            break

        except Exception as e:
            print(f'\033[91mAn error occurred: {label}. Retrying...\033[0m')
            attempts += 1
            close_edit_field_modal(self)
            time.sleep(2)
            
    if attempts == const.MAX_RETRIES:
        print(f"Failed to create {options['input_type']} {label} after several attempts.")

def edit_field_label(self, label, new_label):
    if const.SWITCH == False:
        return

    transform_label = transform_string(label)
    modified_label = transform_label.replace(' ', '_')

    attempts = False

    while attempts == False:
        try:
            self.implicitly_wait(5)
            edit_btn = self.find_element(By.XPATH, f"//label[@for='_115__field_{modified_label}']/a")

            self.execute_script("arguments[0].scrollIntoView({ block: 'center' });", edit_btn)

            edit_btn.click()

            self.implicitly_wait(5)

            field_input = self.find_element(By.ID, "field_label")
            field_input.clear()
            field_input.send_keys(format_text(new_label))

            save_btn = self.find_element(By.ID, "save_field_button")
            save_btn.click()

            attempts = True

            break

        except Exception as e:
            print(f'\033[93mAn error occurred: {modified_label}. Retrying...\033[0m')
            time.sleep(3)
            
    if attempts == const.MAX_RETRIES:
        print(f"\033[91mFailed to edit {label} after several attempts.\033[0m")

def read_json():
    with open(const.JSON_PATH, 'r') as ob_obj:
        data = json.load(ob_obj)
    
    return data

def format_text(label):
    label = label.replace('_', ' ')
    label = label.title()
    
    return label

def transform_string(input_string):
    parts = input_string.rsplit(' ', 1)
    
    if len(parts) == 2:
        parts[1] = parts[1].lower()
    
    return ' '.join(parts)

def replace_pt_with_payment_terminal(labels):
    return labels.replace("pt", "payment_terminal")

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
    close_button = self.find_element(By.XPATH, "//form[@name='edit_field_form']//button[@class='close']")
    close_button.click()
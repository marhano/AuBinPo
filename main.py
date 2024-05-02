from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import tkinter as tk
from tkinter import messagebox
import re

def handle_login():
    # Open the webpage
    driver.get("http://binpo.paybps.ovpn/intranet/panels/helpdesk_edit_rules.php")
    driver.implicitly_wait(0.5)

    username = driver.find_element(By.ID, "frmuser")
    username.clear()
    username.send_keys(entry_username.get())

    password = driver.find_element(By.ID, "frmpass")
    password.clear()
    password.send_keys(entry_password.get())

    submit = driver.find_element(By.ID, "submit")
    submit.click()
    driver.implicitly_wait(1)
    
    driver.get("http://binpo.paybps.ovpn/intranet/panels/helpdesk_edit_rules.php?id=104")

    # REMOVE LOGIN GUI
    label_username.destroy()
    entry_username.destroy()
    label_password.destroy()
    entry_password.destroy()
    button_login.destroy()
    remember_me_checkbox.destroy()

    create_or_update_rules_gui()

def create_or_update_rules_gui():
    global rules_gui_created

    if not rules_gui_created:
        create_rules_gui()
        rules_gui_created = True
    else:
        update_rules_gui()

def create_rules_gui():
    global entry_num_rules, entry_ref_id, entry_ref_name
    # RULES GUI
    tk.Label(frame_main, text="Number of Rules: ").pack()
    entry_num_rules = tk.Entry(frame_main)
    entry_num_rules.pack()

    tk.Label(frame_main, text="Ref ID: ").pack()
    entry_ref_id = tk.Entry(frame_main)
    entry_ref_id.pack()

    # TRIGGER RULE CREATTION
    button_process_rules = tk.Button(frame_main, text="Process Rules", command=handle_process_rules)
    button_process_rules.pack()

def clear_rules_gui():
    clear_entry_if_not_empty(entry_num_rules)
    clear_entry_if_not_empty(entry_ref_id)

def clear_entry_if_not_empty(entry_widget):
    if has_content(entry_widget):
        entry_widget.delete(0, tk.END)
        
def has_content(entry_widget):
    content = entry_widget.get()
    return bool(content)

def update_rules_gui():
    clear_rules_gui()

def handle_process_rules():
    for reference_number in reference_number_arr:
        try:

            numeric_part = re.search(r'\d+', entry_ref_id.get()).group()
            ref_name = "Ref#" + numeric_part
            rule_ref_name = ref_name + "__" + reference_number

            if check_if_existing(rule_ref_name):
                continue

            add_new_condition_set = driver.find_element(By.NAME, "add_rule_link")
            add_new_condition_set.click()

            driver.implicitly_wait(1)

            
            rule_name = driver.find_element(By.ID, "rule_name")
            rule_name.send_keys(rule_ref_name)

            # CHECKBOXES
            driver.find_element(By.ID, "for_fields_rights").click()
            driver.find_element(By.ID, "for_workflow").click()
            driver.find_element(By.ID, "for_sla").click()

            # REFERENCE NUMBER ID
            xpath_expression =  f"//input[@value='{entry_ref_id.get()}']"
            checkbox_ref = driver.find_element(By.XPATH, xpath_expression)
            checkbox_ref.click()
            parent_element = checkbox_ref.find_element(By.XPATH, "./ancestor::tr")
            print(parent_element)
            parent_element.find_element(By.XPATH, ".//input[contains(@id,'equal_checkbox')]").click()

            parent_element.find_element(By.XPATH, ".//input[contains(@id,'input_equal')]").send_keys(reference_number)

            # FOR TRIGGER
            driver.find_element(By.ID, "for_trigger").click()

            # SAVE
            driver.find_element(By.NAME, "add_rule").click()

        except NoSuchElementException:
            messagebox.showerror("Error", "Reference ID not found!")
            driver.get("http://binpo.paybps.ovpn/intranet/panels/helpdesk_edit_rules.php?id=104")
            break

    choice = messagebox.askyesno("Confirmation", "Do you want to enter more rules?")
    if not choice:
        driver.quit()
    
    clear_rules_gui()

def check_if_existing(rule_ref_name):
    print(rule_ref_name)
    order_number = driver.find_elements(By.XPATH, f"//a[contains(text(), '{rule_ref_name}')]")
    if order_number:
        return True
    else:
        return False    

def handle_remember_me():
    if remember_me_var.get() == 1:
        with open("credentials.txt", "w") as file:
            file.write(f"{entry_username.get()}:{entry_password.get()}")
    else:
        with open("credentials.txt", "w") as file:
            file.write("")

def populate_login_form():
    try:
        with open("credentials.txt", "r") as file:
            saved_credentials = file.readline().strip().split(":")
            if len(saved_credentials) == 2:
                entry_username.insert(0, saved_credentials[0])
                entry_password.insert(0, saved_credentials[1])
                remember_me_var.set(1)
    except FileNotFoundError:
        pass



driver = webdriver.Chrome()
reference_number_arr = ["LCD-A0001A", "LCD-A0001B", "LCD-A0001C", "LCD-A0001D", "LCD-A0002A", "LCD-A0002B", "LCD-A0002C", "LCD-A0003B", "LCD-A0004B", "LCD-A0004E", "LCD-A0004D", "LCD-A0005B", "LCD-A0005D", "LCD-B0001C", "LCD-B0002A", "LCD-B0002C", "LCD-B0003A", "LCD-B0004F", "LCD-B0004E", "LCD-B0005C", "LCD-C0001A", "LCD-C0001F", "LCD-C0001C", "LCD-C0001G", "LCD-C0001D", "LCD-C0002A", "LCD-C0002F", "LCD-C0002C", "LCD-C0002G", "LCD-C0002D", "LCD-C0003F", "LCD-C0004F", "LCD-C0004D", "LCD-C0005A", "LCD-C0005G", "LCD-C0005D", "LCD-C0006F", "LCD-C0006C", "LCD-C0006D"]

entry_num_rules = None
entry_ref_id = None
entry_ref_name = None

rules_gui_created = False
stop_flag = False


root = tk.Tk()
gui_thread = Thread(target=root.mainloop)
gui_thread.start()
root.title("Au-BinPo")
root.resizable(False, False)

frame_main = tk.Frame(root, padx=48, pady=32)
frame_main.pack()

label_username = tk.Label(frame_main, text="Username: ")
label_username.pack()
entry_username = tk.Entry(frame_main)
entry_username.pack()

label_password = tk.Label(frame_main, text="Password: ")
label_password.pack()
entry_password = tk.Entry(frame_main, show="*")
entry_password.pack()

remember_me_var = tk.IntVar()
remember_me_checkbox = tk.Checkbutton(frame_main, text="Remember Me", variable=remember_me_var, command=handle_remember_me)
remember_me_checkbox.pack()

populate_login_form()

button_login = tk.Button(frame_main, text="Login", command=handle_login)
button_login.pack()

root.mainloop()
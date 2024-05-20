import tkinter as tk
from tkinter import ttk
import json
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def handle_login():
    global label_username, entry_username, label_password, entry_username, remember_me_var, remember_me_checkbox, button_login
    # Open the webpage
    driver.get("http://binpo.paybps.ovpn/login?&page=%2Fmain%2F")
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
    
    driver.get("http://binpo.paybps.ovpn/intranet/panels/helpdesk_admin.php")

    # REMOVE LOGIN GUI
    label_username.destroy()                                                                                           
    entry_username.destroy()
    label_password.destroy()
    entry_password.destroy()
    button_login.destroy()
    remember_me_checkbox.destroy()

    display_form_selection()

def display_login_form():
    global label_username, entry_username, label_password, entry_password, remember_me_var, remember_me_checkbox, button_login

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

def handle_template_add():
    return

def populate_template():
    data = [{
        "name": "John",
        "age": 30,
        "city": "New York"
    }]
    with open("templates.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

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

def handle_remember_me():
    if remember_me_var.get() == 1:
        with open("credentials.txt", "w") as file:
            file.write(f"{entry_username.get()}:{entry_password.get()}")
    else:
        with open("credentials.txt", "w") as file:
            file.write("")

def populate_login_form():
    global entry_username, entry_password, remember_me_var
    try:
        with open("credentials.txt", "r") as file:
            saved_credentials = file.readline().strip().split(":")
            if len(saved_credentials) == 2:
                entry_username.insert(0, saved_credentials[0])
                entry_password.insert(0, saved_credentials[1])
                remember_me_var.set(1)
    except FileNotFoundError:
        pass

def display_form_selection():
    cards = driver.find_elements(By.CLASS_NAME, "card")

    form_arr = []

    for card in cards:
        card_content__title = card.find_element(By.CLASS_NAME, "card-content__title")
        form_text = card_content__title.text.strip()
        form_arr.append(form_text)

        href = card_content__title.get_attribute("href")

        link_mapping[form_text] = href

    # INFOCAPTURE SELECTION
    selected_option = tk.StringVar()
    dropdown = ttk.Combobox(frame_main, textvariable=selected_option, values=form_arr)
    dropdown.pack()
    dropdown.bind("<<ComboboxSelected>>", handle_form_selection)

    button_edit_form = tk.Button(frame_main, text="Edit Form", command=handle_edit_form)
    button_edit_form.pack()

    button_field_condition_sets = tk.Button(frame_main, text="Field condition sets", command=handle_field_condition_sets)
    button_field_condition_sets.pack()

    button_new_template = tk.Button(frame_main, text="New Template", command=handle_new_template)
    button_new_template.pack()

def handle_field_condition_sets():
    driver.find_element(
        By.XPATH, "//div[@class='col-md-2 info-panel admin-info-panel js-info-panel']//a[contains(., 'Field condition sets')]"
        ).click()

def handle_new_template():
    form_toolbar = driver.find_element(By.CLASS_NAME, "btn-toolbar")
    form_field_selections = form_toolbar.find_elements(By.CLASS_NAME, "btn-group")
    for field in form_field_selections:
        a_tag = field.find_element(By.TAG_NAME, "a")
        field_name = a_tag.get_attribute("title")
        if field_name:
            create_form_field_button(field_name, a_tag)


def create_form_field_button(field_name, link):
    if field_name:
        def on_tab_changed(event):
            current_tab_index = notebook.index(notebook.select())

        def on_button_click():
            link.click()
            display_field_modal_inputs()

        def save_template():
            data_list = []
            for tab_frame, tab_name in zip(notebook.winfo_children(), tabs):
                tab_data = []
                for widget in tab_frame.winfo_children():
                    if isinstance(widget, tk.Entry):
                        entry_data = widget.get()
                        tab_data.append(entry_data)
                    elif isinstance(widget, ttk.Combobox):
                        selected_value = widget.get()
                        tab_data.append(selected_value)
                    elif isinstance(widget, tk.Checkbutton):
                        checkbox_state = widget.get()  # Get the value of the associated IntVar
                        tab_data.append(checkbox_state)

                data_list.append({tab_name.lower(): tab_data})


            # SAVE TO JSON
            with open("data.json", "w") as json_file:
                json.dump(data_list, json_file)

        def display_field_modal_inputs():
            global notebook
            
            for widget in created_widgets:
                widget.destroy()
            created_widgets.clear()

            field_form = driver.find_element(By.NAME, "edit_field_form")
            
            notebook = ttk.Notebook(root)
            notebook.pack(fill="both", expand=True)
            created_widgets.append(notebook)

            for tab in tabs:
                tab_frame = ttk.Frame(notebook)
                notebook.add(tab_frame, text=tab)

                properties = field_form.find_element(By.ID, tab.lower())
                form_groups = properties.find_elements(By.XPATH, "div[contains(@class, 'form-group')]")

                for form_group in form_groups:
                    style_attribute = form_group.get_attribute("style")
                    if "display: none;" in style_attribute:
                        continue

                    form_group_label = form_group.find_elements(
                        By.XPATH, "label[contains(@class, 'control-label')]"
                    )

                    form_group_input = form_group.find_elements(
                        By.CLASS_NAME, "form-control"
                    )

                    form_group_checkboxes = form_group.find_elements(
                        By.CLASS_NAME, "checkbox"
                    )

                    if form_group_label:
                        form_group_label_text = form_group_label[0].get_attribute("textContent")
                    
                        Label_field = tk.Label(tab_frame, text=form_group_label_text)
                        Label_field.pack()

                    if form_group_input:
                        if form_group_input[0].tag_name == "input":
                            entry_field = tk.Entry(tab_frame)
                            entry_field.pack()
                        elif form_group_input[0].tag_name == "select":
                            option_elements = form_group_input[0].find_elements(By.TAG_NAME, "option")
                            options = [option.text for option in option_elements]

                            selected_option = tk.StringVar()
                            dropdown_field = ttk.Combobox(tab_frame, textvariable=selected_option, values=options)
                            dropdown_field.pack()
                    
                    if form_group_checkboxes:
                        for form_group_checkbox in form_group_checkboxes:
                            if "display: none;" in form_group_checkbox.get_attribute("style"):
                                continue
                            checkbox_text = form_group_checkbox.get_attribute("innerText").strip()
                            checkbox_var = tk.IntVar()
                            checkbox = tk.Checkbutton(tab_frame, text=checkbox_text, variable=checkbox_var)
                            checkbox.pack()
                            created_widgets.append(checkbox_var)


            notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

            button_save = tk.Button(root, text="Save", command=save_template)
            button_save.pack()
            created_widgets.append(button_save)


        button = tk.Button(frame_main, text=f"{field_name}", command=on_button_click)
        button.pack(side="left", padx=8)
 

def handle_edit_form():
    driver.find_element(
        By.XPATH, "//a[contains(@name, 'edit_fields_link')]"
        ).click()

def handle_form_selection(event):
    selected_text = event.widget.get()
    if selected_text in link_mapping:
        driver.get(link_mapping[selected_text])


driver = webdriver.Chrome()

# LOGIN FORM
entry_username = None 
entry_password = None 
label_username = None 
label_password = None 
button_login = None 
remember_me_var = None 
remember_me_checkbox = None
notebook = None
tabs = ["Properties", "Style", "Constraints"]

created_widgets = []

link_mapping = {}

root = tk.Tk()
root.title("Au-BinPo")
root.resizable(False, False)

frame_main = tk.Frame(root, padx=48, pady=24)
frame_main.pack()

populate_template()

display_login_form()



root.mainloop()
import curses
import subprocess
import os
import json

class AddNewFieldConditionForm():
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def run(self):
        curses.curs_set(1)
        self.stdscr.clear()


        self.stdscr.addstr(0, 0, "Add new field condition")
        rule_name_prompt = "Rule name: "
        self.stdscr.addstr(2, 0, rule_name_prompt)
        field_condition_prompt = "Field Condition(Field Id's separated by comma(,)): "
        self.stdscr.addstr(3, 0, field_condition_prompt)

        self.stdscr.refresh()

        curses.echo()
        rule_name = self.stdscr.getstr(2, len(rule_name_prompt)).decode("utf-8")
        field_condition = self.stdscr.getstr(3, len(field_condition_prompt)).decode("utf-8")
        curses.noecho()

        # field_condition_arr = [field.strip() for field in field_condition.split(',')]

        file_path = 'field_condition.json'
        if not os.path.exists(file_path):
            open(file_path, 'w').close()

        notepad_process = subprocess.Popen(['notepad.exe', file_path])

        notepad_process.wait()

        with open(file_path, 'r') as file:
            try:
                field_condition_arr = json.load(file)
            except json.JSONDecodeError:
                print("The file does not contain valid JSON data.")
                field_condition_arr = None



        return rule_name, field_condition_arr

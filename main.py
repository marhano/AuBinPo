from infographics.infographics import Infographics
import curses
from cursesmenu import CursesMenu
from cursesmenu.items import FunctionItem, SubmenuItem

def display_menu(add_new_condition_func, edit_condition_func):
    menu = CursesMenu('BinBot', 'BinPo infographics automation bot.')
    field_condition_item_menu = CursesMenu("Field condition set")
    field_condition_item = SubmenuItem("Field condition set", field_condition_item_menu, menu=menu)
    field_condition_item__new_condition_set = FunctionItem("Add new condition set", add_new_condition_func)
    field_condition_item__edit_condition_set = FunctionItem("Edit condition set", edit_condition_func)
    field_condition_item_menu.items.append(field_condition_item__new_condition_set)
    field_condition_item_menu.items.append(field_condition_item__edit_condition_set)

    automatic_change_item = FunctionItem("Automatic changes", input, ["Enter some input"])
    field_visibility_item = FunctionItem("Field Visibility", input, ["Enter some input"])
    
    menu.items.append(field_condition_item)
    menu.items.append(automatic_change_item)
    menu.items.append(field_visibility_item)

    menu.show()
    
if __name__ == "__main__":
    with Infographics() as bot:
        bot.login_user(username="binpo.mbcarullo", password="566bXeYDr4")
        display_menu(bot.add_new_condition, bot.edit_condition)

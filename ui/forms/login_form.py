import curses
from ..widgets.radio_widget import RadioWidget

class LoginForm:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.cursor_x = 0
        self.cursor_y = 4   
        self.username = ""
        self.password = ""

    def draw_form(self):
        self.stdscr.clear()

        self.stdscr.addstr(2, 0, "Login")
        self.stdscr.addstr(4, 0, "Username:")
        self.stdscr.addstr(5, 0, "Password:")
        self.stdscr.addstr(4, 0, self.username)
        self.stdscr.addstr(5, 0, "*" * len(self.password))

        self.stdscr.refresh()

    def get_input(self):
        curses.echo()

        self.stdscr.move(self.cursor_y, self.cursor_x)
        self.username = self.stdscr.getstr().decode("utf-8")

        self.stdscr.move(self.cursor_y + 1, self.cursor_x)
        while True:
            key = self.stdscr.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:  
                break
            elif key == curses.KEY_BACKSPACE or key == 127: 
                self.password = self.password[:-1]
            else:
                self.password += chr(key)

            masked_password = '*' * len(self.password)
            self.stdscr.addstr(self.cursor_y + 1, self.cursor_x, masked_password)
        
        radio_widget = RadioWidget(self.stdscr, "Remember me: ", ["Yes", "No"])
        choice = radio_widget.handle_input(6, 5)

        curses.noecho()

    def run(self):
        self.draw_form()
        self.get_input()
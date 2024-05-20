import curses
from ui.forms import LoginForm

def main(stdscr):  
    curses.curs_set(0)

    login_form = LoginForm(stdscr)

    login_form.run()

if __name__ == "__main__":
    curses.wrapper(main)


import curses

class RadioWidget:
    def __init__(self, stdscr, label, choices):
        self.stdscr = stdscr
        self.label = label
        self.choices = choices
        self.selected_index = 0
        self.highlight_color_pair = 1

    def draw(self, y, x):
        self.stdscr.addstr(y, x, f"{self.label}")

        for i, choice in enumerate (self.choices):
            if i == self.selected_index:
                self.stdscr.attron(curses.color_pair(self.highlight_color_pair) | curses.A_BOLD)
                self.stdscr.addstr(choice)
                self.stdscr.attroff(curses.color_pair(self.highlight_color_pair) | curses.A_BOLD)
            else:
                self.stdscr.addstr(choice)

            if i < len(self.choices) - 1:
                self.stdscr.addstr(" ")

    def handle_input(self, y, x):
        while True:
            key = self.stdscr.getch()
            print(key)
            if key == 452:
                self.selected_index = max(0, self.selected_index - 1)
            elif key == 454:
                self.selected_index = min(len(self.choices) - 1, self.selected_index + 1)
            elif key in (curses.KEY_ENTER, 10, 13):
                break

            self.draw(y, x)
            self.stdscr.refresh()

        return self.choices[self]
class Button:
    def __init__(self, stdscr, text, x, y):
        self.stdscr = stdscr
        self.text = text
        self.x = x
        self.y = y

    def render(self):
        pass

    def handle_input(self, key):
        pass
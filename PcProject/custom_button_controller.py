class CustomButtonController:
    def __init__(self, button, command):
        self.button = button
        self.command = command
        self.button.clicked.connect(self.print_command)

    def print_command(self):
        print(self.command)
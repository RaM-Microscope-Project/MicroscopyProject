# class LedButtonController:
#     def __init__(self, button):
#         self.button = button
#         self.is_yellow = False  # To keep track of the current color state
#         self.button.clicked.connect(self.toggle_color)  # Connect the button click to toggle_color method
#
#
#     def toggle_color(self):
#         if self.is_yellow:
#             self.button.setStyleSheet("background-color: #919191")
#         else:
#             self.button.setStyleSheet("background-color: yellow")
#         self.is_yellow = not self.is_yellow  # Toggle the state
#
#
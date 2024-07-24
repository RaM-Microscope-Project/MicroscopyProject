# class CustomButtonController:
#     def __init__(self, arduino):
#         self.arduino = arduino

#     def connect_button_with_message(self, button, message):
#         button.clicked.connect(lambda: self.arduino.send_serial_message(message))

# from PyQt5.QtWidgets import QPushButton
# from PyQt5.QtCore import QEvent, QObject, pyqtSignal

# class HoverButton(QPushButton):
#     hoverEnter = pyqtSignal()  # Signal to be emitted on hover enter
#     hoverLeave = pyqtSignal()  # Signal to be emitted on hover leave

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.setMouseTracking(True)  # Enable mouse tracking to detect hover
#         self.installEventFilter(self)  # Install an event filter to catch hover events

#     def eventFilter(self, obj, event):
#         if obj == self:
#             if event.type() == QEvent.Enter:
#                 self.hoverEnter.emit()  # Emit the hover enter signal
#             elif event.type() == QEvent.Leave:
#                 self.hoverLeave.emit()  # Emit the hover leave signal
#         return super().eventFilter(obj, event)

# class CustomButtonController:
#     def __init__(self, arduino):
#         self.arduino = arduino

#     def connect_button_with_message(self, button, message):
#         # Ensure the button is a HoverButton instance
#         # if not isinstance(button, HoverButton):
#         #     raise ValueError("button must be an instance of HoverButton")

#         # Connect the hoverEnter signal to a lambda function that sends the enter message
#         button.hoverEnter.connect(lambda: self.arduino.send_serial_message(message))
#         # Connect the hoverLeave signal to a lambda function that sends the leave message
#         button.hoverLeave.connect(lambda: self.arduino.send_serial_message(message))

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QEvent, pyqtSignal

class AutoHoverButton(QPushButton):
    hoverEnter = pyqtSignal()  # Signal for hover enter
    hoverLeave = pyqtSignal()  # Signal for hover leave

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.isAlwaysOn = False  # Toggle state

    def mousePressEvent(self, event):
        self.isAlwaysOn = not self.isAlwaysOn  # Toggle the state on click
        # if self.isAlwaysOn:
        #     self.hoverEnter.emit()  # Optionally, turn on immediately on click
        super().mousePressEvent(event)

    def eventFilter(self, obj, event):
        if obj == self and not self.isAlwaysOn:  # Check if not in always-on mode
            if event.type() == QEvent.Enter:
                self.hoverEnter.emit()
            elif event.type() == QEvent.Leave:
                self.hoverLeave.emit()
        return super().eventFilter(obj, event)

    @staticmethod
    def replace_with_auto_hover(button):
        """
        Replace a QPushButton with an AutoHoverButton, copying relevant properties.
        """
        auto_hover_button = AutoHoverButton(button.parent())
        auto_hover_button.setText(button.text())
        auto_hover_button.setGeometry(button.geometry())
        auto_hover_button.setStyleSheet(button.styleSheet())
        auto_hover_button.setObjectName(button.objectName())
        button.deleteLater()  # Remove the original button
        return auto_hover_button
        


    
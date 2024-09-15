from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QEvent, pyqtSignal


class HoverButton(QPushButton):
    """
    Button that toggles its color on hover and click.
    The buttons are grey. They should turn yellow on hover and stay yellow on click.
    When they stay yellow, the hover effect should be disabled. When they are clicked again, they should revert to grey.
    Feature requested by the end user.
    Replaces the classic QPushButton with a custom HoverButton, including the CSS properties.
    Uses signals to handle hover enter and leave events.
    """

    hoverEnter = pyqtSignal()  # Signal for hover enter
    hoverLeave = pyqtSignal()  # Signal for hover leave

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.isAlwaysOn = False  # Flag to keep the button always on, when clicked
        self.hoverEnter.connect(self.onHoverEnter)
        self.hoverLeave.connect(self.onHoverLeave)

    def onHoverEnter(self):
        """
        Change the color to yellow on hover enter.
        """
        if not self.isAlwaysOn:  # Change color only if not in always-on mode
            self.setStyleSheet("background-color: yellow;")

    def onHoverLeave(self):
        """
        Revert the color to grey on hover leave.
        """
        if not self.isAlwaysOn:  # Revert color only if not in always-on mode
            self.setStyleSheet("background-color: grey;")

    def mousePressEvent(self, event):
        """
        Toggle the color on click.
        Clicking has priority over hover.

        :param event: The mouse press event.
        """
        self.isAlwaysOn = not self.isAlwaysOn  # Toggle the state on click
        super().mousePressEvent(event)

    def reset(self):
        """
        Reset the button to its default state.
        """
        self.isAlwaysOn = False
        self.setStyleSheet("background-color: grey;")

    def eventFilter(self, obj, event):
        """
        Handle hover detection.

        :param obj: Ensures that the event is occurring on this specific button instance.
        :param event: The event to detect (mouse entering/leaving the proximity of the button).
        """
        if obj == self and not self.isAlwaysOn:  # Check if not in always-on mode
            if event.type() == QEvent.Enter:
                self.hoverEnter.emit() # Emit the hover enter signal
            elif event.type() == QEvent.Leave:
                self.hoverLeave.emit() # Emit the hover leave signal
        return super().eventFilter(obj, event)

    @staticmethod
    def replace_with_auto_hover(button):
        """
        Replace a QPushButton with an AutoHoverButton, copying relevant properties.
        Necessary to replace the buttons, without changing the graphical_user_interface.py file.

        :param button: QPushButton to replace
        """
        auto_hover_button = HoverButton(button.parent())
        auto_hover_button.setText(button.text())
        auto_hover_button.setGeometry(button.geometry())
        auto_hover_button.setStyleSheet(button.styleSheet())
        auto_hover_button.setObjectName(button.objectName())
        button.deleteLater()  # Remove the original button
        return auto_hover_button

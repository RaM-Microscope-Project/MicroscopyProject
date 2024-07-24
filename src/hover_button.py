from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QEvent, pyqtSignal

class HoverButton(QPushButton):
    hoverEnter = pyqtSignal()  # Signal for hover enter
    hoverLeave = pyqtSignal()  # Signal for hover leave

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.isAlwaysOn = False  # Toggle state
        self.hoverEnter.connect(self.onHoverEnter)
        self.hoverLeave.connect(self.onHoverLeave)

    def onHoverEnter(self):
        if not self.isAlwaysOn:  # Change color only if not in always-on mode
            self.setStyleSheet("background-color: yellow;")

    def onHoverLeave(self):
        if not self.isAlwaysOn:  # Revert color only if not in always-on mode
            self.setStyleSheet("background-color: grey;")

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
        auto_hover_button = HoverButton(button.parent())
        auto_hover_button.setText(button.text())
        auto_hover_button.setGeometry(button.geometry())
        auto_hover_button.setStyleSheet(button.styleSheet())
        auto_hover_button.setObjectName(button.objectName())
        button.deleteLater()  # Remove the original button
        return auto_hover_button
        


    
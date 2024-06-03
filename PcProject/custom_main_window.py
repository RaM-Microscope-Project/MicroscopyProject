from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets

from PcProject.graphical_user_interface import Ui_MainWindow


class CustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.startPos = None
        self.isResizing = False
        self.isMoving = False  # Add this flag to track if the window is being moved

        """
        All the widgets meed to have mouse tracking enabled to detect the edges for resizing
        """
        self.setMouseTracking(True)  # Enable mouse tracking
        self.ui.centralwidget.setMouseTracking(True)  # Enable mouse tracking
        self.ui.mainBodyContainer.setMouseTracking(True)  # Enable mouse tracking
        self.ui.headerContainer.setMouseTracking(True)  # Enable mouse tracking
        self.ui.controlsContainer.setMouseTracking(True)  # Enable mouse tracking
        self.ui.stageControlContainer.setMouseTracking(True)  # Enable mouse tracking
        ## ---------------------

        # Set the window to be frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # self = main window
        self.resizingEdges = 5 # Number of pixels for detecting edges for resizing

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.isOnEdge(event.pos()):
                self.isResizing = True
                self.resizeStartPos = event.globalPos()
                self.resizeStartRect = self.frameGeometry()
            elif self.childAt(event.pos()) == self.ui.headerContainer:
                self.isMoving = True
                self.startPos = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        x = event.x()
        width = self.width()
        print(x)
        # # Change the cursor based on the position
        # if x < width / 2:
        #     self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
        # else:
        #     self.setCursor(QCursor(QtCore.Qt.WaitCursor))
        if self.isResizing:
            self.resizeWindow(event)
        elif self.isMoving:
            self.moveWindow(event)
        else:
            self.updateCursorShape(event.pos())

    def mouseReleaseEvent(self, event):
        self.isResizing = False
        self.isMoving = False  # Reset the moving flag
        # self.setCursor(QtCore.Qt.ArrowCursor)

    def moveWindow(self, event):
        if self.startPos:
            self.move(event.globalPos() - self.startPos)

    def isOnEdge(self, pos):
        rect = self.rect()
        left = pos.x() <= self.resizingEdges
        right = pos.x() >= rect.width() - self.resizingEdges
        top = pos.y() <= self.resizingEdges
        bottom = pos.y() >= rect.height() - self.resizingEdges

        self.edgeFlags = (left, right, top, bottom)

        return any(self.edgeFlags)

    def resizeWindow(self, event):
        if self.isResizing:
            delta = event.globalPos() - self.resizeStartPos
            newRect = QtCore.QRect(self.resizeStartRect)

            if self.edgeFlags[0]:  # Left edge
                newRect.setLeft(newRect.left() + delta.x())
            if self.edgeFlags[1]:  # Right edge
                newRect.setRight(newRect.right() + delta.x())
            if self.edgeFlags[2]:  # Top edge
                newRect.setTop(newRect.top() + delta.y())
            if self.edgeFlags[3]:  # Bottom edge
                newRect.setBottom(newRect.bottom() + delta.y())
            self.setGeometry(newRect)

    def updateCursorShape(self, pos):
        rect = self.rect()
        left = pos.x() <= self.resizingEdges
        right = pos.x() >= rect.width() - self.resizingEdges
        top = pos.y() <= self.resizingEdges
        bottom = pos.y() >= rect.height() - self.resizingEdges

        if left and top or right and bottom:
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
            print("corner")
        elif right and top or left and bottom:
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
            print("corner")
        elif left or right:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            print("horizontal")
        elif top or bottom:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            print("vertical")
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)



import resources_rc

if __name__ == "__main__":
    import sys

    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # sys.exit(app.exec_())

    app = QtWidgets.QApplication(sys.argv)
    window = CustomMainWindow()
    window.show()
    sys.exit(app.exec_())
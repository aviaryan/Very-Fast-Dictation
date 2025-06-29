import sys
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt, QMetaObject
from PySide6.QtGui import QIcon


class Notification:
    """A simple notification widget that can be shown and hidden."""

    def __init__(self):
        """Initializes the notification widget and the QApplication."""
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)

        icon_path = "images/icon.png"
        self.app.setWindowIcon(QIcon(icon_path))

        self.widget = self._create_widget()

    def _create_widget(self):
        """Creates and configures the notification QLabel."""
        widget = QLabel("Recording... (Press Ctrl to end)")
        widget.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.ToolTip
        )
        widget.setStyleSheet(
            "background-color: black; color: white; padding: 10px; border-radius: 5px;"
        )
        widget.adjustSize()

        # Position the widget at the center of the primary screen
        screen = self.app.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            widget.move(
                (screen_geometry.width() - widget.width()) // 2,
                (screen_geometry.height() - widget.height()) // 2,
            )
        return widget

    def show(self):
        """Shows the notification widget in a thread-safe way."""
        QMetaObject.invokeMethod(self.widget, "show", Qt.QueuedConnection)

    def hide(self):
        """Hides the notification widget in a thread-safe way."""
        QMetaObject.invokeMethod(self.widget, "hide", Qt.QueuedConnection)

    def run(self):
        """Starts the Qt application event loop."""
        sys.exit(self.app.exec())

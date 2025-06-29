import sys
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt, QMetaObject
from PySide6.QtGui import QIcon, QPixmap

if sys.platform == "darwin":
    try:
        import AppKit
        from Foundation import NSData
    except ImportError:
        print(
            "pyobjc-framework-Cocoa not installed. "
            "Install it with 'pip install pyobjc-framework-Cocoa' to set the dock icon."
        )


class Notification:
    """A simple notification widget that can be shown and hidden."""

    def __init__(self):
        """Initializes the notification widget and the QApplication."""
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication(sys.argv)
        
        self._set_app_identity()
        self.widget = self._create_widget()

    def _set_app_identity(self):
        """Sets the application name and icon."""
        self.app.setApplicationName("VeryFastDictation")
        icon_path = "images/icon.png"

        self.app.setWindowIcon(QIcon(icon_path))

        if sys.platform == "darwin" and "AppKit" in sys.modules:
            # Make the app a proper UI app in the dock
            ns_app = AppKit.NSApplication.sharedApplication()
            ns_app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)

            # Set app name in the menu bar and icon in the Dock
            bundle = AppKit.NSBundle.mainBundle()
            if bundle:
                info = bundle.infoDictionary()
                info["CFBundleName"] = "VeryFastDictation"

            with open(icon_path, "rb") as f:
                icon_data = f.read()
            data = NSData.dataWithBytes_length_(icon_data, len(icon_data))
            image = AppKit.NSImage.alloc().initWithData_(data)
            ns_app.setApplicationIconImage_(image)

    def _create_widget(self):
        """Creates and configures the notification QLabel."""
        widget = QLabel("Recording...")
        widget.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.ToolTip
        )
        widget.setStyleSheet(
            "background-color: black; color: white; padding: 10px; border-radius: 5px;"
        )
        widget.adjustSize()

        # Position the widget at the top-right corner of the primary screen
        screen = self.app.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            widget.move(
                screen_geometry.width() - widget.width() - 20,
                40  # 40 pixels from the top
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

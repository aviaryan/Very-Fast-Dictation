import sys
import subprocess
import pyperclip
from pynput import keyboard


def paste_text(text):
    """Pastes the given text by copying it to clipboard and simulating a paste command."""
    pyperclip.copy(text)

    if sys.platform == "darwin":
        # Try AppleScript first; if blocked by permissions, fall back to pynput.
        # osascript is the only path that reliably reports a permission denial
        # (pynput silently does nothing when Accessibility is not granted), so
        # we use its result to detect a blocked paste and warn the user.
        permission_blocked = False
        try:
            result = subprocess.run(
                [
                    "osascript",
                    "-e",
                    'tell application "System Events" to keystroke "v" using command down',
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                # 1002 / "not allowed to send keystrokes" => missing Accessibility permission
                stderr = (result.stderr or "").lower()
                if "1002" in stderr or "not allowed" in stderr or "assistive" in stderr:
                    permission_blocked = True
        except Exception:
            permission_blocked = True

        if permission_blocked:
            print(
                "\n⚠️  Paste may be blocked on macOS: the app does not have "
                "Accessibility permission, so it can't simulate Cmd+V.\n"
                "    The transcribed text has been copied to your clipboard — "
                "press Cmd+V to paste it manually.\n"
                "    To enable automatic paste, grant Accessibility permission to "
                "your terminal (or the Python binary) in\n"
                "    System Settings > Privacy & Security > Accessibility, then restart the app.\n"
            )
            # Still attempt pynput in case permission was granted to a different
            # process that can drive the keystroke.
            try:
                controller = keyboard.Controller()
                with controller.pressed(keyboard.Key.cmd):
                    controller.press("v")
                    controller.release("v")
            except Exception:
                pass
    else:
        # For other OSes, use pynput
        modifier = keyboard.Key.ctrl
        controller = keyboard.Controller()
        with controller.pressed(modifier):
            controller.press("v")
            controller.release("v")

    print("Pasted: " + text)

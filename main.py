import time
import sounddevice as sd
import soundfile as sf
from pynput import keyboard
import numpy as np
import threading
from modules.stt import transcribe
from modules.ui import Notification
import pyperclip
import sys
import subprocess
import signal

# --- Configuration ---
DOUBLE_PRESS_INTERVAL = 0.3  # Seconds
SAMPLE_RATE = 44100  # Hertz
CHANNELS = 1  # Mono
OUTPUT_FILENAME_TEMPLATE = "recording.wav"
FRAMES_PER_BUFFER = 1024

# --- State ---
last_key_press_time = 0
is_recording = False
audio_frames = []
listener_thread = None
notification = None
keyboard_listener = None
shutdown_requested = False
shutdown_in_progress = False


def get_timestamp_str():
    return time.strftime("%Y%m%d_%H%M%S")


def signal_handler(sig, frame):
    """Handles Ctrl+C (SIGINT) signal for graceful shutdown."""
    global \
        shutdown_requested, \
        is_recording, \
        keyboard_listener, \
        notification, \
        shutdown_in_progress

    # Prevent double execution
    if shutdown_in_progress:
        return
    shutdown_in_progress = True

    print("\nShutting down...")
    shutdown_requested = True

    # Stop recording if active
    if is_recording:
        stop_recording()

    # Stop keyboard listener
    if keyboard_listener:
        keyboard_listener.stop()

    # Quit Qt application if it exists
    if notification:
        notification.quit()

    sys.exit(0)


def on_press(key):
    global last_key_press_time, is_recording, audio_frames

    try:
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            current_time = time.time()
            time_since_last_press = current_time - last_key_press_time
            last_key_press_time = current_time

            if is_recording:
                stop_recording()
            elif time_since_last_press < DOUBLE_PRESS_INTERVAL:
                start_recording()

    except Exception as e:
        print(f"An error occurred: {e}")


def record_audio():
    global audio_frames
    audio_frames = []
    with sd.InputStream(
        samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="float32"
    ) as stream:
        print("Recording started...")
        while is_recording:
            frames, overflowed = stream.read(FRAMES_PER_BUFFER)
            if overflowed:
                print("Warning: input overflowed")
            audio_frames.append(frames)


def start_recording():
    global is_recording, listener_thread
    if is_recording:
        return
    print("Double-press detected. Starting recording.")
    if notification:
        notification.show()
    is_recording = True
    listener_thread = threading.Thread(target=record_audio)
    listener_thread.start()


def stop_recording():
    global is_recording, listener_thread
    if not is_recording:
        return

    print("Stopping recording...")
    if notification:
        notification.hide()
    is_recording = False
    if listener_thread:
        listener_thread.join()  # Wait for recording thread to finish

    if audio_frames:
        filename = OUTPUT_FILENAME_TEMPLATE
        recording = np.concatenate(audio_frames, axis=0)
        sf.write(filename, recording, SAMPLE_RATE)
        print(f"Recording saved to {filename}")
        transcript = transcribe(filename)
        if transcript:
            paste_text(transcript)
    else:
        print("No audio was recorded.")


def paste_text(text):
    """Pastes the given text by copying it to clipboard and simulating a paste command."""
    pyperclip.copy(text)

    if sys.platform == "darwin":
        # Try AppleScript first; if blocked by permissions, fall back to pynput
        success = False
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
            success = result.returncode == 0
        except Exception:
            success = False

        if not success:
            try:
                controller = keyboard.Controller()
                with controller.pressed(keyboard.Key.cmd):
                    controller.press("v")
                    controller.release("v")
                success = True
            except Exception:
                success = False

        if not success:
            print(
                "Paste failed on macOS. Grant Accessibility permission to Terminal/Python in System Settings > Privacy & Security > Accessibility."
            )
    else:
        # For other OSes, use pynput
        modifier = keyboard.Key.ctrl
        controller = keyboard.Controller()
        with controller.pressed(modifier):
            controller.press("v")
            controller.release("v")

    print("Pasted: " + text)


def check_shutdown_requested():
    """Callback function for Qt to check if shutdown was requested."""
    return shutdown_requested


def main():
    global notification, keyboard_listener

    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    notification = Notification(shutdown_callback=check_shutdown_requested)

    print("Application started.")
    print("Press Ctrl twice quickly to start recording.")
    print("Press Ctrl again to stop.")
    print("Press Ctrl+C in the terminal to quit.")

    # Start keyboard listener in a separate thread
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

    try:
        # Run Qt event loop in main thread - this is the proper way
        notification.app.exec()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)


if __name__ == "__main__":
    main()

import time
import sounddevice as sd
import soundfile as sf
from pynput import keyboard
import numpy as np
import threading
from modules.stt import transcribe
from modules.ui import Notification
from modules.clipboard import paste_text
import sys
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
is_stopping = False
state_lock = threading.Lock()
frame_lock = threading.Lock()


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
    global last_key_press_time

    try:
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            current_time = time.time()
            time_since_last_press = current_time - last_key_press_time
            last_key_press_time = current_time

            if is_recording:
                request_stop_recording()
            elif time_since_last_press < DOUBLE_PRESS_INTERVAL:
                start_recording()

    except Exception as e:
        print(f"An error occurred: {e}")


def record_audio():
    global audio_frames, is_recording

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="float32"
        ) as stream:
            print("Recording started...")
            while True:
                with state_lock:
                    should_continue = is_recording
                if not should_continue:
                    break

                frames, overflowed = stream.read(FRAMES_PER_BUFFER)
                if overflowed:
                    print("Warning: input overflowed")
                with frame_lock:
                    audio_frames.append(frames.copy())
    except Exception as e:
        with state_lock:
            is_recording = False
        if notification:
            notification.hide()
        print(f"Recording failed: {e}")


def start_recording():
    global is_recording, listener_thread, audio_frames

    with state_lock:
        if is_recording or is_stopping:
            return
        is_recording = True

    with frame_lock:
        audio_frames = []

    print("Double-press detected. Starting recording.")
    if notification:
        notification.show()
    listener_thread = threading.Thread(target=record_audio, daemon=True)
    listener_thread.start()


def request_stop_recording():
    """Stops recording in a worker so the keyboard listener remains responsive."""
    global is_stopping

    with state_lock:
        if not is_recording or is_stopping:
            return
        is_stopping = True

    threading.Thread(target=stop_recording, daemon=True).start()


def stop_recording():
    global is_recording, is_stopping, listener_thread

    with state_lock:
        if not is_recording:
            is_stopping = False
            return
        is_recording = False

    print("Stopping recording...")
    if notification:
        notification.hide()

    recording_thread = listener_thread
    if recording_thread and recording_thread.is_alive():
        recording_thread.join(timeout=2)

    if recording_thread and recording_thread.is_alive():
        print(
            "Warning: recording thread did not stop promptly; "
            "continuing with captured audio."
        )

    with frame_lock:
        captured_frames = list(audio_frames)

    try:
        if captured_frames:
            filename = OUTPUT_FILENAME_TEMPLATE
            recording = np.concatenate(captured_frames, axis=0)
            sf.write(filename, recording, SAMPLE_RATE)
            print(f"Recording saved to {filename}")
            transcript = transcribe(filename)
            if transcript:
                paste_text(transcript)
        else:
            print("No audio was recorded.")
    except Exception as e:
        print(f"Failed to process recording: {e}")
    finally:
        with state_lock:
            is_stopping = False


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

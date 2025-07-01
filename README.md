# Very Fast Dictation (M-Series Macs) 🎙️

A blazing fast, real-time, system-wide dictation tool for your Mac.

Very Fast Dictation is a minimalist, high-performance, and real-time transcription tool. It's designed for speed and efficiency, allowing you to dictate text from anywhere in your operating system with a simple keyboard shortcut.

## ✨ Features

-   **🚀 Blazing Fast:** Get your speech transcribed in real-time using [Parakeet MLX](https://github.com/senstella/parakeet-mlx).
-   **🌐 System-Wide:** Use it in any application on your desktop.
-   **⌨️ Shortcut Activated:** Just press `Control` twice to start and stop dictating.
-   **🚦 Visual Indicator:** A "Recording..." label appears so you know when it's listening.
-   **📋 Clipboard Integration:** The transcribed text is automatically copied to your clipboard and pasted to the active window.

## 📹 Demo

https://github.com/user-attachments/assets/c1a1f4d8-dc97-40a3-8e49-0b31021e100b

## ⚙️ Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/aviaryan/Very-Fast-Dictation.git
    cd Very-Fast-Dictation
    ```

2.  **Install dependencies:**
    This project uses [uv](https://github.com/astral-sh/uv) for package management. Once you have `uv` installed, run the following command to install the required packages:

    ```sh
    uv sync
    ```
    This will install all necessary dependencies including `parakeet-mlx`, `pynput`, `pyside6` and others.

## ▶️ How to Use

1.  **Run the application:**
    ```sh
    uv run main.py
    ```
    The application will start running in the background.

2.  **Start Dictating:**
    -   Go to any text field in any application.
    -   Press the `Control` key twice rapidly to start recording.
    -   You will see a "Recording..." label appear on your screen at the center.
    -   Begin speaking.
    -   Press the `Control` key once to stop.
    -   The transcribed text will be instantly pasted to your active screen.

## 🛠️ Common Issues

### 📋 Transcribed text isn't pasting

If you are able to record text but it doesn't paste anything once recording is done, make sure to give the following access to the application running this Python script.

Eg - If you are running this script on your `Terminal.app`, go to System Settings -> Privacy & Security -> Accessibility and make sure the toggle is turned on for `Terminal`.

**Tip** - If you don't want to give full accessibility permissions to your Terminal or code editor, install a second terminal app like Warp or iTerm. Use this second-terminal for running this application only. Now, you can safely give accessibility permissions to this terminal app as you will not be using it for anything else.

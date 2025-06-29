<img src="images/icon.png" alt="logo" width="100"/>

# Very Fast Dictation 🎙️

A blazing fast, real-time, system-wide dictation tool for your desktop.

Very Fast Dictation is a minimalist, high-performance, and real-time transcription tool. It's designed for speed and efficiency, allowing you to dictate text from anywhere in your operating system with a simple keyboard shortcut.

## ✨ Features

-   **🚀 Blazing Fast:** Get your speech transcribed in real-time using [Parakeet MLX](https://github.com/senstella/parakeet-mlx).
-   **🌐 System-Wide:** Use it in any application on your desktop.
-   **⌨️ Shortcut Activated:** Just press `Control` twice to start and stop dictating.
-   **🚦 Visual Indicator:** A "Recording..." label appears so you know when it's listening.
-   **📋 Clipboard Integration:** The transcribed text is automatically copied to your clipboard.

## ⚙️ Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/aviaryan/Very-Fast-Dictation.git
    cd Very-Fast-Dictation
    ```

2.  **Install dependencies:**
    This project uses [uv](https://github.com/astral-sh/uv) for package management. Once you have `uv` installed, run the following command to install the required packages:

    ```sh
    uv install
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

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/aviaryan/Very-Fast-Dictation/issues).

## 📄 License

This project is licensed under the MIT License.

from parakeet_mlx import from_pretrained

# since it can take time, we print a message to the user
print("Loading voice recognition model (please wait)...")

model = from_pretrained("mlx-community/parakeet-tdt-0.6b-v2")


def transcribe(audio_file_path):
    result = model.transcribe(audio_file_path)
    return result.text


if __name__ == "__main__":
    result = transcribe("audio_file.wav")
    print(result)

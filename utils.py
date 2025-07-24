import os
import shutil
import whisper

def save_audio(uploaded_file, file_id):
    folder = "audio"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{file_id}.wav")
    with open(path, "wb") as f:
        f.write(uploaded_file.read())
    return path

def transcribe_audio(path):
    model = whisper.load_model("base")  # Use "tiny" for speed, "base" for accuracy
    result = model.transcribe(path)
    return result["text"]

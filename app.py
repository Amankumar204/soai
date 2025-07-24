import streamlit as st
import os
import uuid
from utils import save_audio, transcribe_audio
from gtts import gTTS
import google.generativeai as genai

# ✅ Configure Google Generative AI with your Gemini API key
genai.configure(api_key="AIzaSyDojTildyjbqtkV1bq6CFByPdbuiGWYGCU")

# Load Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-pro"

# App Title
st.title("🎙️ Suno Kahani – Record Your Story")
st.markdown("Tell us a story from your life, a festival memory, or an old tale you remember.")

# --- Story Submission Form ---
with st.form("story_form"):
    title = st.text_input("Story Title")
    description = st.text_area("Short Description")
    audio_file = st.file_uploader("Record or upload your story (MP3/WAV)", type=["mp3", "wav"])
    submit = st.form_submit_button("Submit")

# --- On Form Submit ---
if submit and audio_file:
    file_id = str(uuid.uuid4())
    audio_path = save_audio(audio_file, file_id)
    st.success("✅ Story saved successfully!")

    # Transcribe audio
    with st.spinner("📝 Transcribing your story..."):
        transcript = transcribe_audio(audio_path)

    # Save transcript
    os.makedirs("transcriptions", exist_ok=True)
    with open(f"transcriptions/{file_id}.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    st.markdown("#### 🗣️ Transcription:")
    st.write(transcript)

    # --- AI-Powered Telugu Translation ---
    def ai_translate_to_telugu(text):
        prompt = (
            "Translate the following story into natural, expressive, and casual Telugu for narration. "
            "Just return the translated Telugu story, do not include any English explanations or transliterations:\n\n" + text
        )
        response = model.generate_content(prompt)
        return response.text.strip()

    try:
        with st.spinner("🌐 Translating to Telugu using Gemini AI..."):
            telugu_translation = ai_translate_to_telugu(transcript)

        st.markdown("#### 📝 AI-Powered Telugu Translation:")
        st.write(telugu_translation)

        # --- Text-to-Speech ---
        tts = gTTS(text=telugu_translation, lang='te')
        os.makedirs("tts", exist_ok=True)
        tts_path = f"tts/{file_id}.mp3"
        tts.save(tts_path)

        st.markdown("#### 🔊 Telugu Narration:")
        st.audio(tts_path)

    except Exception as e:
        st.error(f"Translation or narration failed: {str(e)}")

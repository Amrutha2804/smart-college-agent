import streamlit as st
from streamlit_audio_recorder import audio_recorder
from gtts import gTTS
import io
import requests
import speech_recognition as sr
st.title("KIIT Smart College Companion 🎓")


st.write("Record your question (Hindi/Odia/English):")
audio_bytes = audio_recorder(pause_threshold=2.0)

text_query = st.text_input("Or, type your question:")
lang = st.selectbox("Language", ["en", "hi", "or"], index=0)

def stt(audio_data, lang):
    recognizer = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(audio_data)) as s:
        audio = recognizer.record(s)
        return recognizer.recognize_google(audio, language=lang)
    return None

if audio_bytes:
    try:
        text_query = stt(audio_bytes, lang)
        st.info(f"Recognized: {text_query}")
    except Exception as e:
        st.error(f"Speech recognition failed: {e}")

if st.button("Ask") and text_query:
    with st.spinner("Getting answer..."):
        resp = requests.post(
            "http://localhost:8000/api/query",
            json={"question": text_query, "user_id": "demo_user", "lang": lang}
        )
        if resp.ok:
            data = resp.json()
            st.success(data["answer"])
            # TTS output
            tts = gTTS(data["answer"], lang=lang)
            tts_fp = io.BytesIO()
            tts.write_to_fp(tts_fp)
            st.audio(tts_fp.getvalue(), format="audio/mp3")
            if data.get("sources"):
                st.caption("Sources: " + ", ".join(data["sources"]))
        else:
            st.error("API error.")

import streamlit as st
from datetime import datetime
from utils.meet_bot import GoogleMeetBot
from utils.transcription import TranscriptionService
from utils.file_generator import FileGenerator

st.set_page_config(page_title="Google Meet Recorder", page_icon="🎤", layout="wide")
st.title("🎤 Google Meet Recorder")

def initialize_session_state():
    if 'meet_bot' not in st.session_state:
        st.session_state.meet_bot = None
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False
    if 'current_session' not in st.session_state:
        st.session_state.current_session = None

def create_session_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def join_meeting_and_start_recording(meeting_url):
    st.session_state.meet_bot = GoogleMeetBot()
    join_success = st.session_state.meet_bot.join_meeting(meeting_url)
    
    if join_success:
        st.session_state.current_session = create_session_id()
        recording_started = st.session_state.meet_bot.start_recording(st.session_state.current_session)
        
        if recording_started:
            st.session_state.is_recording = True
            st.success("✅ Meeting joined and recording started")
            st.rerun()
        else:
            st.error("Failed to start recording")
    else:
        st.error("Failed to join meeting")

def stop_recording_and_generate_files():
    audio_file_path = st.session_state.meet_bot.stop_recording()
    
    if audio_file_path:
        transcription_service = TranscriptionService()
        transcript_text = transcription_service.transcribe_audio(audio_file_path)
        
        file_generator = FileGenerator()
        text_file_path = file_generator.create_text_file(transcript_text, st.session_state.current_session)
        pdf_file_path = file_generator.create_pdf_file(transcript_text, st.session_state.current_session)
        
        display_results(audio_file_path, transcript_text, text_file_path, pdf_file_path)
        reset_session()

def display_results(audio_file_path, transcript_text, text_file_path, pdf_file_path):
    st.success("✅ Recording completed and transcript generated")
    
    st.audio(audio_file_path, format='audio/wav')
    st.text_area("Generated Transcript:", transcript_text, height=300)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with open(text_file_path, 'r', encoding='utf-8') as text_file:
            st.download_button(
                "📄 Download Text File",
                text_file.read(),
                file_name=f"transcript_{st.session_state.current_session}.txt"
            )
    
    with col2:
        with open(pdf_file_path, 'rb') as pdf_file:
            st.download_button(
                "📑 Download PDF File",
                pdf_file.read(),
                file_name=f"transcript_{st.session_state.current_session}.pdf",
                mime="application/pdf"
            )

def reset_session():
    st.session_state.is_recording = False
    st.session_state.meet_bot = None

def main():
    initialize_session_state()
    
    meeting_url = st.text_input("📹 Enter Google Meet URL:", placeholder="https://meet.google.com/abc-defg-hij")
    
    if meeting_url and not st.session_state.is_recording:
        if st.button("🚀 Join Meeting", type="primary", use_container_width=True):
            with st.spinner("Joining meeting and starting recording..."):
                join_meeting_and_start_recording(meeting_url)
    
    if st.session_state.is_recording:
        st.success("🔴 Recording in progress...")
        
        if st.button("⏹️ Stop Recording & Save", type="secondary", use_container_width=True):
            with st.spinner("Processing recording and generating transcript..."):
                stop_recording_and_generate_files()

if __name__ == "__main__":
    main()

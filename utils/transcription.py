import os
import numpy as np
from datetime import datetime

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import assemblyai as aai
    ASSEMBLYAI_AVAILABLE = True
except ImportError:
    ASSEMBLYAI_AVAILABLE = False

class TranscriptionService:
    def __init__(self):
        self.whisper_model = None
        self.assemblyai_client = None
        
        if WHISPER_AVAILABLE:
            self.whisper_model = whisper.load_model("base")
        
        if ASSEMBLYAI_AVAILABLE:
            api_key = os.getenv('ASSEMBLYAI_API_KEY')
            if api_key:
                aai.settings.api_key = api_key
                self.assemblyai_client = aai.Transcriber()
    
    def transcribe_audio(self, audio_file_path):
        if not os.path.exists(audio_file_path):
            return "Audio file not found"
        
        audio_info = self.get_audio_info(audio_file_path)
        
        if audio_info["too_small"] or audio_info["no_content"]:
            return self.create_error_message(audio_file_path, audio_info)
        
        transcript = None
        service_used = None
        
        if self.assemblyai_client:
            transcript = self.use_assemblyai(audio_file_path)
            if transcript:
                service_used = "AssemblyAI"
        
        if not transcript and self.whisper_model:
            transcript = self.use_whisper(audio_file_path)
            if transcript:
                service_used = "Whisper"
        
        if transcript:
            return self.create_success_message(transcript, audio_file_path, audio_info, service_used)
        else:
            return self.create_failure_message(audio_file_path, audio_info)
    
    def get_audio_info(self, audio_file_path):
        try:
            import soundfile as sf
            file_size = os.path.getsize(audio_file_path)
            audio_data, sample_rate = sf.read(audio_file_path)
            max_volume = np.max(np.abs(audio_data))
            duration = len(audio_data) / sample_rate
            
            return {
                "duration": duration,
                "file_size": file_size,
                "max_volume": max_volume,
                "too_small": file_size < 1000,
                "no_content": max_volume < 0.001
            }
        except:
            return {"duration": 0, "file_size": 0, "max_volume": 0, "too_small": True, "no_content": True}
    
    def use_assemblyai(self, audio_file_path):
        try:
            result = self.assemblyai_client.transcribe(audio_file_path)
            if result.status != aai.TranscriptStatus.error:
                text = result.text.strip()
                return text if len(text) > 10 else None
        except:
            pass
        return None
    
    def use_whisper(self, audio_file_path):
        try:
            result = self.whisper_model.transcribe(audio_file_path, fp16=False)
            text = result["text"].strip()
            return text if len(text) > 10 else None
        except:
            pass
        return None
    
    def create_success_message(self, transcript_text, audio_file_path, audio_info, service_name):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        filename = os.path.basename(audio_file_path)
        
        return f"""MEETING TRANSCRIPT
Generated: {timestamp}
Service: {service_name}
File: {filename}
Duration: {audio_info['duration']:.1f}s

TRANSCRIPT:
{transcript_text}

Transcription completed successfully."""
    
    def create_error_message(self, audio_file_path, audio_info):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        filename = os.path.basename(audio_file_path)
        
        return f"""MEETING TRANSCRIPT - ERROR
Generated: {timestamp}
File: {filename}
Duration: {audio_info['duration']:.1f}s

No speech detected in audio file.
Please record with active speech."""
    
    def create_failure_message(self, audio_file_path, audio_info):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        filename = os.path.basename(audio_file_path)
        
        return f"""MEETING TRANSCRIPT - FAILED
Generated: {timestamp}
File: {filename}
Duration: {audio_info['duration']:.1f}s

Transcription services unavailable or failed.
Check AssemblyAI and Whisper setup."""

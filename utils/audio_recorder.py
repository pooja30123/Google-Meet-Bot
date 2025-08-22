import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import time
import os

class AudioRecorder:
    def __init__(self):
        self.audio_chunks = []
        self.is_recording = False
        self.recording_thread = None
        self.current_session = None
        self.save_location = None
    
    def start_recording(self, session_name, save_directory):
        os.makedirs(save_directory, exist_ok=True)
        
        self.current_session = session_name
        self.save_location = save_directory
        self.audio_chunks = []
        self.is_recording = True
        
        self.recording_thread = threading.Thread(target=self.capture_audio)
        self.recording_thread.start()
        return True
    
    def capture_audio(self):
        try:
            with sd.InputStream(samplerate=44100, channels=2, dtype='float32') as audio_stream:
                while self.is_recording:
                    audio_data, _ = audio_stream.read(1024)
                    self.audio_chunks.append(audio_data.copy())
                    time.sleep(0.001)
        except Exception as error:
            print(f"Audio capture failed: {error}")
    
    def stop_recording(self):
        self.is_recording = False
        
        if self.recording_thread:
            self.recording_thread.join()
        
        if self.audio_chunks:
            complete_audio = np.concatenate(self.audio_chunks, axis=0)
            audio_file_path = f"{self.save_location}/{self.current_session}.wav"
            sf.write(audio_file_path, complete_audio, 44100)
            return audio_file_path
        return None

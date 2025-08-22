# 🎤 Google Meet Bot

**Automate Google Meet attendance, record audio, and generate AI-powered transcriptions**

[![Demo Video](https://img.shields.io/badge/Demo-Watch%20Video-red?style=for-the-badge&logo=youtube)](https://youtu.be/NALaPhlwDks)

## 🚀 Features

✅ **Automatic Meeting Join** - Bot joins Google Meet sessions automatically  
✅ **Real-time Recording** - Captures meeting audio in the background  
✅ **AI Transcription** - Uses OpenAI Whisper (local) and AssemblyAI (cloud)  
✅ **File Generation** - Creates PDF and text transcripts  
✅ **Simple Interface** - Clean Streamlit web UI  



## 🛠 Quick Setup

```
Clone repository
git clone https://github.com/pooja30123/Google-Meet-Bot.git
cd Google-Meet-Bot

Setup virtual environment
python -m venv venv

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

(Optional) Add AssemblyAI API key
echo "ASSEMBLYAI_API_KEY=your-api-key-here" > .env

Run the app
streamlit run app.py
```

## 📁 Project Structure

```
Meet_Bot/
├── 📄 app.py # Main Streamlit application
├── ⚙️ config.py # Configuration settings
├── 📋 requirements.txt # Python dependencies
├── 🔒 .env # Environment variables
├── 📂 assets/
│ ├── 🎵 recordings/ # Audio files
│ └── 📄 transcripts/
│ ├── text/ # Text transcripts
│ └── pdf/ # PDF transcripts
└── 🛠 utils/
├── 🎙️ audio_recorder.py # Audio recording logic
├── 🤖 meet_bot.py # Google Meet automation
├── 📝 transcription.py # AI transcription service
└── 📋 file_generator.py # PDF/text file creation
```


## 🎯 How It Works

1. **Enter Google Meet URL** in the web interface
2. **Click Join Meeting** - Chrome opens and bot joins automatically
3. **Recording starts** - Audio captured in background
4. **Click Stop** - AI processes speech to text
5. **Download files** - Get audio, PDF, and text transcripts

## 🧠 AI Technologies Used

- **OpenAI Whisper** - Local speech recognition
- **AssemblyAI** - Cloud-based transcription service  
- **Selenium WebDriver** - Browser automation
- **Streamlit** - Web interface framework

## 📋 Requirements

- Python 3.8+
- Chrome Browser (version 139+ recommended)
- FFmpeg (for audio processing)
- Microphone access

## 🔧 Troubleshooting

**Chrome Driver Issues:**
- App auto-downloads correct ChromeDriver for Chrome 139
- Ensure you have Google Chrome installed

**Transcription Not Working:**
- Check FFmpeg installation (Windows users)
- Verify microphone permissions
- Ensure clear speech during recording

**Empty Transcripts:**
- Make sure people are actually speaking
- Check audio input levels
- Test with music/voice playing


## 📄 License

MIT License - Feel free to use and modify for educational purposes.

---

⭐ **Star this repository if you found it helpful!**

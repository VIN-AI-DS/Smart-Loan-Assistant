import pyaudio
import wave
import io
import requests
from utils import get_sarvam_api_key

# API configuration
SARVAM_AI_API = get_sarvam_api_key()
api_url = "https://api.sarvam.ai/speech-to-text"
headers = {"api-subscription-key": SARVAM_AI_API}

lang_dict = {
    1: "English",
    2: "Hindi",
    3: "Tamil",
    4: "Telugu",
    5: "Kannada"
}

print("Select Language: ")
for i, j in lang_dict.items():
    print(i, "->", j)

lang_opt = int(input("Enter your choice: "))

if (lang_opt == 1):
    language_code = "en-IN"
elif (lang_opt == 2):
    language_code = "hi-IN"
elif (lang_opt == 3):
    language_code = "ta-IN"
elif (lang_opt == 4):
    language_code = "te-IN"
elif (lang_opt == 5):
    language_code = "kn-IN"

data = {
    "language_code": language_code,  # Language code (e.g., 'hi-IN' for Hindi)
    "model": "saarika:v2",     # Model to use for transcription
    "with_timestamps": False   # Set to True for word-level timestamps
}

# Audio configuration
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Mono audio
RATE = 16000              # Sampling rate (16 kHz)
CHUNK = 1024              # Buffer size (number of frames per chunk)
RECORD_SECONDS = 10       # Duration of the recording (in seconds)

# Initialize PyAudio
audio = pyaudio.PyAudio()

def record_audio_chunk(stream, chunk_duration):
    """
    Record a chunk of audio from the microphone.
    """
    frames = []
    for _ in range(0, int(RATE / CHUNK * chunk_duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    return b"".join(frames)

def transcribe_audio(audio_data):
    """
    Send an audio chunk to the API for transcription.
    """
    # Convert raw audio data to a WAV file in memory
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(audio_data)
    wav_buffer.seek(0)

    # Prepare the file for the API request
    files = {'file': ('audiofile.wav', wav_buffer, 'audio/wav')}

    try:
        # Send the request to the API
        response = requests.post(api_url, headers=headers, files=files, data=data)
        if response.status_code == 200 or response.status_code == 201:
            response_data = response.json()
            transcript = response_data.get("transcript", "")
            return transcript
        else:
            print(f"API request failed with status code: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"Error during API request: {e}")
        return None
    finally:
        wav_buffer.close()

def record_and_transcribe():
    """
    Record audio for a specified duration and transcribe it.
    """
    # Open the microphone stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print(f"Recording for {RECORD_SECONDS} seconds... Speak now!")

    # Record audio
    audio_data = record_audio_chunk(stream, RECORD_SECONDS)

    # Close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Transcribe the recorded audio
    transcript = transcribe_audio(audio_data)
    return transcript

# Record and transcribe audio
transcription = record_and_transcribe()

# Print the transcription
if transcription:
    print(f"Transcription: {transcription}")
else:
    print("Transcription failed.")
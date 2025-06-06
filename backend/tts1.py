import requests
import base64
import wave
from utils import get_sarvam_api_key
from translate2 import native_translation
from stt import language_code

def native_audio(native_lang):
    """A simple financial tips advisor agent that extracts 'context' and 'confidence' 
    from mission controls response and returns a message"""
    SARVAM_AI_API=get_sarvam_api_key()   


    url = "https://api.sarvam.ai/text-to-speech"
    headers = {
        "Content-Type": "application/json",
        "api-subscription-key": SARVAM_AI_API  
    }

    text = ''.join(native_lang)

    chunk_size = 500  
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    # Print the number of chunks
    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        # Prepare the payload for the API request
        payload = {
            "inputs": [chunk],
            "target_language_code": language_code,  # Target language code (Kannada in this case)
            "speaker": "neel",  # Speaker voice
            "model": "bulbul:v1",  # Model to use
            "pitch": 0,  # Pitch adjustment
            "pace": 1.0,  # Speed of speech
            "loudness": 1.0,  # Volume adjustment
            "enable_preprocessing": True,  # Enable text preprocessing
        }

        # Make the API request
        response = requests.post(url, json=payload, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Decode the base64-encoded audio data
            audio = response.json()["audios"][0]
            audio = base64.b64decode(audio)
            with wave.open(f"output{i}.wav", "wb") as wav_file:
                    # Set the parameters for the .wav file
                wav_file.setnchannels(1)  # Mono audio
                wav_file.setsampwidth(2)  # 2 bytes per sample
                wav_file.setframerate(22050)  # Sample rate of 22050 Hz

                    # Write the audio data to the file
                wav_file.writeframes(audio)

            print(f"Audio file {i} saved successfully as 'output{i}.wav'!")
        else:
            print(f"Error for chunk {i}: {response.status_code}")
            print(response.json())
        



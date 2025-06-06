import re
import requests
import os
import time
from utils import get_sarvam_api_key
from stt import transcription
from serp import res_text
from stt import language_code

def native_support(final_res):
    SARVAM_API_KEY = get_sarvam_api_key()

    text = ''.join(final_res)
    full_text = text
    print("full_text:", full_text)
    def split_into_sentences(text):
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return sentences

    sentences_list = split_into_sentences(full_text)

    print("\n=== First 5 Sentences ===")
    for i, sentence in enumerate(sentences_list[:5], 1):
        print(f"{i}. {sentence}")

    API_KEY = SARVAM_API_KEY 

    if not API_KEY:
        raise ValueError("API key is missing! Set SARVAM_API_KEY in environment variables.")

    url = "https://api.sarvam.ai/translate"
    headers = {
        "api-subscription-key": API_KEY,
        "Content-Type": "application/json"
    }

    native_translation = []

    for i, sentence in enumerate(sentences_list, 1):

        payload = {
            "source_language_code": "en-IN",
            "target_language_code": language_code,
            "speaker_gender": "Male",
            "mode": "classic-colloquial",
            "model": "mayura:v1",
            "enable_preprocessing": False,
            "input": sentence
        }
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            translation = response.json().get("translated_text", "Translation not available")
            native_translation.append(translation)
            print(f"{translation}")
        
        else:
            print(f"{i}. {sentence} ➝ [Translation Failed]")

    return native_translation
    time.sleep(0.5)

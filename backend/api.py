import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from translate3 import native_support
from tts import financial_tips_agent
from rag import graph
import importlib

stt_module = importlib.import_module("stt")
transcription = stt_module.transcription

app = Flask(__name__)
CORS(app)  

@app.route('/api/query', methods=['POST'])
def process_query():
    """Process a text query and return a response"""
    data = request.json
    user_query = data.get('query', '')
    language_code = data.get('language', 'en-IN')
    
    if not user_query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        state = {"messages": [{"content": user_query}]}
        result = graph.invoke(state)
        response_text = result["messages"][-1].content

        if language_code != 'en-IN':
            native_response = native_support(response_text)
        else:
            native_response = response_text

        audio_file_path = financial_tips_agent(native_response)
        
        return jsonify({
            'text': response_text,
            'translated_text': native_response if language_code != 'en-IN' else None,
            'audio_url': f'/audio/{os.path.basename(audio_file_path)}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/start-recording', methods=['POST'])
def start_recording():
    """Start recording audio for speech-to-text"""
    data = request.json
    language_code = data.get('language', 'en-IN')
    
    try:
        return jsonify({
            'status': 'recording',
            'message': 'Recording started'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop-recording', methods=['POST'])
def stop_recording():
    """Stop recording and return transcription"""
    try:
        transcript = transcription
        
        return jsonify({
            'status': 'success',
            'transcription': transcript
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    """Convert text to speech"""
    data = request.json
    text = data.get('text', '')
    language_code = data.get('language', 'en-IN')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        audio_file_path = financial_tips_agent(text)
        
        return jsonify({
            'status': 'success',
            'audio_url': f'/audio/{os.path.basename(audio_file_path)}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    return send_from_directory('', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
# Smart Loan Assistant

## Overview
Smart Loan Assistant is a multilingual financial assistant that helps users with loan eligibility checks, financial tips, and loan application guidance. The application supports multiple Indian languages including English, Hindi, Tamil, Telugu, and Kannada, making financial information accessible to a wider audience.

## Features
- **Multilingual Support**: Interact in English, Hindi, Tamil, Telugu, or Kannada
- **Voice & Text Input**: Choose between voice recording or text input
- **Loan Eligibility Check**: Get information about loan eligibility criteria
- **Financial Tips**: Receive personalized financial advice
- **Loan Application Guidance**: Learn about the loan application process
- **Text-to-Speech Output**: Listen to responses in your preferred language

## Architecture

### Backend
- **Language Processing**: Uses Groq LLM for natural language understanding
- **Speech Services**: Integrates Sarvam AI for speech-to-text and text-to-speech
- **RAG (Retrieval Augmented Generation)**: Provides accurate information from PDF documents
- **Intent Classification**: Identifies user intent to route queries to appropriate services
- **Translation Services**: Translates responses to the user's preferred language

### Frontend
- **React-based UI**: Modern, responsive user interface
- **Streamlit Interface**: Alternative interface for quick deployment

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- API keys for:
  - Sarvam AI
  - Groq
  - Serper
  - HuggingFace (optional)

### Backend Setup
1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys (see `.env.example` for format)

4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

## API Documentation

### Backend Endpoints
- `/api/query` - Process user queries
- `/api/speech-to-text` - Convert speech to text
- `/api/text-to-speech` - Convert text to speech
- `/api/translate` - Translate text between languages

## Technologies Used
- **LangChain**: For building LLM applications
- **LangGraph**: For creating agent workflows
- **Groq**: For fast LLM inference
- **Sarvam AI**: For Indian language speech services
- **FAISS**: For vector similarity search
- **PyPDF2**: For PDF text extraction
- **React**: For frontend UI

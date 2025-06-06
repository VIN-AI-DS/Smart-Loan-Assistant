import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8501',
  headers: {
    'Content-Type': 'application/json',
  },
});

const apiService = {
  submitQuery: async (query, language) => {
    try {
      const response = await api.post('/api/query', { query, language });
      return response.data;
    } catch (error) {
      console.error('Error submitting query:', error);
      throw error;
    }
  },

  startRecording: async (language) => {
    try {
      const response = await api.post('/api/start-recording', { language });
      return response.data;
    } catch (error) {
      console.error('Error starting recording:', error);
      throw error;
    }
  },

  stopRecording: async () => {
    try {
      const response = await api.post('/api/stop-recording');
      return response.data;
    } catch (error) {
      console.error('Error stopping recording:', error);
      throw error;
    }
  },

  getAudio: async (text, language) => {
    try {
      const response = await api.post('/api/text-to-speech', { text, language });
      return response.data;
    } catch (error) {
      console.error('Error getting audio:', error);
      throw error;
    }
  },
};

export default apiService;
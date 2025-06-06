import React, { useState, useEffect, useRef } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Paper, 
  TextField, 
  Button, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  Grid,
  CircularProgress,
  IconButton,
  Divider,
  Card,
  CardContent
} from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import axios from 'axios';

const HomePage = () => {
  // State variables
  const [language, setLanguage] = useState('English');
  const [inputMethod, setInputMethod] = useState('text');
  const [query, setQuery] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const audioRef = useRef(null);
  
  // Language options mapping
  const languageOptions = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN"
  };

  // Handle language change
  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };

  // Handle input method change
  const handleInputMethodChange = (method) => {
    setInputMethod(method);
  };

  // Handle text input change
  const handleQueryChange = (event) => {
    setQuery(event.target.value);
  };

  // Handle recording start
  const startRecording = async () => {
    setIsRecording(true);
    try {
      // In a real implementation, this would connect to the backend's voice recording API
      // For now, we'll simulate recording for 10 seconds
      setTimeout(() => {
        stopRecording();
      }, 10000);
    } catch (error) {
      console.error('Error starting recording:', error);
      setIsRecording(false);
    }
  };

  // Handle recording stop
  const stopRecording = async () => {
    setIsRecording(false);
    // In a real implementation, this would send the recorded audio to the backend
    // For now, we'll simulate receiving a transcription
    setQuery('Sample transcription from voice input');
  };

  // Handle form submission
  const handleSubmit = async () => {
    if (!query.trim()) return;
    
    setIsLoading(true);
    try {
      // In a real implementation, this would send the query to the backend
      // For now, we'll simulate a response after a delay
      setTimeout(() => {
        const sampleResponse = {
          text: "This is a sample response to your query about loans. In a real implementation, this would come from the backend API. The response would include information relevant to your query about loan eligibility, financial tips, or loan application guidance.",
          audioUrl: "/sample-audio.wav" // In a real implementation, this would be a URL to the audio file
        };
        setResponse(sampleResponse.text);
        setAudioUrl(sampleResponse.audioUrl);
        setIsLoading(false);
      }, 2000);
    } catch (error) {
      console.error('Error submitting query:', error);
      setIsLoading(false);
    }
  };

  // Play audio response
  const playAudio = () => {
    if (audioRef.current) {
      audioRef.current.play();
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Smart Loan Assistant
        </Typography>
        <Typography variant="h6" align="center" color="text.secondary" paragraph>
          Get information about loans, financial tips, and more in your preferred language
        </Typography>

        <Grid container spacing={4} sx={{ mt: 2 }}>
          {/* Left side - Input section */}
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
              <Typography variant="h5" gutterBottom>
                Ask Your Question
              </Typography>
              
              {/* Language selection */}
              <FormControl fullWidth margin="normal">
                <InputLabel id="language-select-label">Language</InputLabel>
                <Select
                  labelId="language-select-label"
                  id="language-select"
                  value={language}
                  label="Language"
                  onChange={handleLanguageChange}
                >
                  {Object.keys(languageOptions).map((lang) => (
                    <MenuItem key={lang} value={lang}>{lang}</MenuItem>
                  ))}
                </Select>
              </FormControl>

              {/* Input method selection */}
              <Box sx={{ display: 'flex', gap: 2, mt: 2, mb: 3 }}>
                <Button 
                  variant={inputMethod === 'text' ? "contained" : "outlined"}
                  onClick={() => handleInputMethodChange('text')}
                >
                  Text Input
                </Button>
                <Button 
                  variant={inputMethod === 'voice' ? "contained" : "outlined"}
                  onClick={() => handleInputMethodChange('voice')}
                >
                  Voice Input
                </Button>
              </Box>

              {/* Text input */}
              {inputMethod === 'text' && (
                <TextField
                  fullWidth
                  label="Enter your query"
                  multiline
                  rows={4}
                  value={query}
                  onChange={handleQueryChange}
                  variant="outlined"
                  margin="normal"
                />
              )}

              {/* Voice input */}
              {inputMethod === 'voice' && (
                <Box sx={{ textAlign: 'center', my: 2 }}>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body1" gutterBottom>
                      {isRecording ? 'Recording... Speak now!' : 'Click to start recording'}
                    </Typography>
                    <IconButton 
                      color={isRecording ? "secondary" : "primary"}
                      aria-label={isRecording ? "Stop recording" : "Start recording"}
                      size="large"
                      onClick={isRecording ? stopRecording : startRecording}
                      sx={{ 
                        width: 80, 
                        height: 80,
                        border: '2px solid',
                        borderColor: isRecording ? 'secondary.main' : 'primary.main'
                      }}
                    >
                      {isRecording ? <StopIcon fontSize="large" /> : <MicIcon fontSize="large" />}
                    </IconButton>
                  </Box>
                  {query && (
                    <Paper elevation={1} sx={{ p: 2, mt: 2, backgroundColor: '#f5f5f5' }}>
                      <Typography variant="body1">
                        <strong>Transcription:</strong> {query}
                      </Typography>
                    </Paper>
                  )}
                </Box>
              )}

              {/* Submit button */}
              <Button
                fullWidth
                variant="contained"
                color="primary"
                size="large"
                onClick={handleSubmit}
                disabled={!query.trim() || isLoading}
                sx={{ mt: 3 }}
              >
                {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Get Response'}
              </Button>
            </Paper>
          </Grid>

          {/* Right side - Response section */}
          <Grid item xs={12} md={6}>
            <Paper elevation={3} sx={{ p: 3, height: '100%', display: 'flex', flexDirection: 'column' }}>
              <Typography variant="h5" gutterBottom>
                Response
              </Typography>
              
              {isLoading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flex: 1 }}>
                  <CircularProgress />
                  <Typography variant="body1" sx={{ ml: 2 }}>
                    Processing your query...
                  </Typography>
                </Box>
              ) : response ? (
                <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                  <Card variant="outlined" sx={{ mb: 3, flex: 1 }}>
                    <CardContent>
                      <Typography variant="body1" paragraph>
                        {response}
                      </Typography>
                    </CardContent>
                  </Card>
                  
                  {audioUrl && (
                    <Box sx={{ mt: 'auto' }}>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="subtitle1" gutterBottom>
                        Audio Response:
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <IconButton color="primary" onClick={playAudio}>
                          <VolumeUpIcon />
                        </IconButton>
                        <Typography variant="body2">
                          Play audio response
                        </Typography>
                        <audio ref={audioRef} src={audioUrl} style={{ display: 'none' }} />
                      </Box>
                    </Box>
                  )}
                </Box>
              ) : (
                <Box sx={{ 
                  display: 'flex', 
                  justifyContent: 'center', 
                  alignItems: 'center', 
                  flex: 1,
                  color: 'text.secondary',
                  backgroundColor: '#f9f9f9',
                  borderRadius: 1,
                  p: 3
                }}>
                  <Typography variant="body1" align="center">
                    Your response will appear here after you submit a query.
                  </Typography>
                </Box>
              )}
            </Paper>
          </Grid>
        </Grid>

        {/* Sample queries section */}
        <Box sx={{ mt: 6, mb: 4 }}>
          <Typography variant="h5" gutterBottom align="center">
            Sample Queries You Can Ask
          </Typography>
          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6} md={4}>
              <Card variant="outlined" sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h6" color="primary" gutterBottom>
                    Loan Eligibility
                  </Typography>
                  <Typography variant="body2">
                    • Am I eligible for a home loan?<br />
                    • What are the eligibility criteria for a personal loan?<br />
                    • Can I get a car loan with my credit score?
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Card variant="outlined" sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h6" color="primary" gutterBottom>
                    Financial Tips
                  </Typography>
                  <Typography variant="body2">
                    • What are some tips for managing personal finances?<br />
                    • How can I save money on loan interest?<br />
                    • What are the best investment strategies for beginners?
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Card variant="outlined" sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h6" color="primary" gutterBottom>
                    Loan Application
                  </Typography>
                  <Typography variant="body2">
                    • How do I apply for a home loan?<br />
                    • What documents are required for a personal loan application?<br />
                    • Can I apply for a loan online?
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
};

export default HomePage;
import React from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Paper, 
  Grid,
  Card,
  CardContent,
  CardMedia,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import LanguageIcon from '@mui/icons-material/Language';
import RecordVoiceOverIcon from '@mui/icons-material/RecordVoiceOver';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import TipsAndUpdatesIcon from '@mui/icons-material/TipsAndUpdates';
import TranslateIcon from '@mui/icons-material/Translate';

const AboutPage = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          About Smart Loan App
        </Typography>
        
        {/* Introduction Section */}
        <Paper elevation={2} sx={{ p: 4, mb: 4 }}>
          <Typography variant="h5" gutterBottom>
            Our Mission
          </Typography>
          <Typography variant="body1" paragraph>
            Smart Loan App is designed to bridge the language gap in financial services in India. 
            We provide accurate, accessible information about loans and financial advice in multiple 
            Indian languages, making financial services more inclusive for everyone.
          </Typography>
          <Typography variant="body1">
            Our application leverages advanced AI technologies including natural language processing, 
            speech recognition, and machine translation to deliver a seamless multilingual experience 
            for users seeking financial guidance.
          </Typography>
        </Paper>
        
        {/* Key Features Section */}
        <Typography variant="h4" gutterBottom align="center" sx={{ mb: 3 }}>
          Key Features
        </Typography>
        
        <Grid container spacing={3} sx={{ mb: 6 }}>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardMedia
                component="div"
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  height: 140,
                  bgcolor: 'primary.light',
                  color: 'white'
                }}
              >
                <LanguageIcon sx={{ fontSize: 60 }} />
              </CardMedia>
              <CardContent>
                <Typography variant="h5" component="div" gutterBottom>
                  Multilingual Support
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Interact with our assistant in English, Hindi, Tamil, Telugu, or Kannada. 
                  Our system is designed to understand and respond in your preferred language, 
                  making financial information accessible to a wider audience.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardMedia
                component="div"
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  height: 140,
                  bgcolor: 'secondary.light',
                  color: 'white'
                }}
              >
                <RecordVoiceOverIcon sx={{ fontSize: 60 }} />
              </CardMedia>
              <CardContent>
                <Typography variant="h5" component="div" gutterBottom>
                  Voice & Text Input
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Choose between voice recording or text input based on your preference. 
                  Our voice recognition system is trained to understand various accents and 
                  dialects, making it easier for you to interact naturally.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardMedia
                component="div"
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  height: 140,
                  bgcolor: 'success.light',
                  color: 'white'
                }}
              >
                <AccountBalanceIcon sx={{ fontSize: 60 }} />
              </CardMedia>
              <CardContent>
                <Typography variant="h5" component="div" gutterBottom>
                  Accurate Information
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Get reliable information about loan eligibility, application processes, and 
                  financial advice. Our system uses Retrieval Augmented Generation (RAG) to 
                  provide accurate, up-to-date information from trusted sources.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
        
        {/* How It Works Section */}
        <Paper elevation={2} sx={{ p: 4, mb: 6 }}>
          <Typography variant="h4" gutterBottom align="center">
            How It Works
          </Typography>
          
          <Grid container spacing={4} sx={{ mt: 2 }}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Technology Stack
              </Typography>
              <List>
                <ListItem>
                  <ListItemIcon>
                    <TipsAndUpdatesIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="AI-Powered Understanding" 
                    secondary="We use advanced language models to understand your queries and provide relevant responses."
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <TranslateIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Real-time Translation" 
                    secondary="Our system translates responses to your preferred language in real-time."
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <RecordVoiceOverIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Speech Processing" 
                    secondary="Advanced speech-to-text and text-to-speech capabilities for natural interaction."
                  />
                </ListItem>
              </List>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Data Flow
              </Typography>
              <Box sx={{ pl: 2 }}>
                <Typography variant="body1" paragraph>
                  1. <strong>User Input:</strong> You provide your query via text or voice in your preferred language.
                </Typography>
                <Typography variant="body1" paragraph>
                  2. <strong>Intent Classification:</strong> Our system identifies the type of information you're seeking.
                </Typography>
                <Typography variant="body1" paragraph>
                  3. <strong>Information Retrieval:</strong> We fetch accurate information from our knowledge base.
                </Typography>
                <Typography variant="body1" paragraph>
                  4. <strong>Response Generation:</strong> A clear, helpful response is generated based on your query.
                </Typography>
                <Typography variant="body1">
                  5. <strong>Translation & Speech:</strong> The response is translated to your language and converted to speech if needed.
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Paper>
        
        {/* Banks & Financial Institutions Section */}
        <Typography variant="h4" gutterBottom align="center" sx={{ mb: 3 }}>
          Supported Banks & Financial Institutions
        </Typography>
        
        <Grid container spacing={2} sx={{ mb: 6 }}>
          {['HDFC Bank', 'ICICI Bank', 'Axis Bank', 'Kotak Mahindra Bank', 'IndusInd Bank'].map((bank) => (
            <Grid item xs={6} sm={4} md={2.4} key={bank}>
              <Paper 
                elevation={1} 
                sx={{ 
                  p: 2, 
                  textAlign: 'center',
                  height: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}
              >
                <Typography variant="body1">{bank}</Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
        
        {/* Disclaimer Section */}
        <Paper elevation={1} sx={{ p: 3, bgcolor: '#f8f9fa' }}>
          <Typography variant="subtitle1" gutterBottom fontWeight="bold">
            Disclaimer
          </Typography>
          <Typography variant="body2" color="text.secondary">
            The information provided by Smart Loan App is for general informational purposes only. 
            While we strive to keep the information up to date and correct, we make no representations 
            or warranties of any kind, express or implied, about the completeness, accuracy, reliability, 
            suitability, or availability of the information. Any reliance you place on such information 
            is therefore strictly at your own risk.
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default AboutPage;
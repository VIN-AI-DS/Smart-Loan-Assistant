import React from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Grid, 
  Link, 
  Divider 
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <Box 
      component="footer" 
      sx={{ 
        bgcolor: 'primary.main', 
        color: 'white',
        py: 3,
        mt: 'auto'
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Smart Loan App
            </Typography>
            <Typography variant="body2">
              Making financial information accessible in multiple Indian languages.
            </Typography>
          </Grid>
          
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Quick Links
            </Typography>
            <Link 
              component={RouterLink} 
              to="/" 
              color="inherit" 
              sx={{ display: 'block', mb: 1 }}
            >
              Home
            </Link>
            <Link 
              component={RouterLink} 
              to="/about" 
              color="inherit" 
              sx={{ display: 'block', mb: 1 }}
            >
              About
            </Link>
          </Grid>
          
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" gutterBottom>
              Supported Languages
            </Typography>
            <Typography variant="body2" paragraph>
              English • Hindi • Tamil • Telugu • Kannada
            </Typography>
          </Grid>
        </Grid>
        
        <Divider sx={{ my: 2, bgcolor: 'rgba(255,255,255,0.2)' }} />
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap' }}>
          <Typography variant="body2" sx={{ mr: 2 }}>
            © {currentYear} Smart Loan App. All rights reserved.
          </Typography>
          <Box>
            <Link color="inherit" sx={{ mr: 2 }}>
              Privacy Policy
            </Link>
            <Link color="inherit">
              Terms of Service
            </Link>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;
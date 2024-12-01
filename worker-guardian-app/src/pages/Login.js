import React, { useState } from 'react';
import { useAuth } from '../providers/AuthContext';

import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { FormControl, Typography } from '@mui/material';
import { Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [user, setUser] = useState({
    userLogin: '',
    userPassword: ''
  });

  const [errors, setErrors] = useState({
    loginError: false,
    passwordError: false,
    serverAns: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    const newErrors = {
      loginError: !user.userLogin.trim(),
      passwordError: !user.userPassword.trim()
    };
  
    setErrors(newErrors);

    if (!newErrors.loginError && !newErrors.passwordError) {
      login(user.userLogin, user.userPassword, (errorMessage) => { 
        setErrors((prev) => ({ ...prev, serverAns: errorMessage }));
      });
    }
  }

  return (
    <Box sx={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
    }}>
      <Box component="form" onSubmit={handleSubmit} sx={{
        width: '25vw',
        padding: '2rem',
        backgroundColor: 'rgba(10, 44, 61, 0.9)',
        color: 'text.default',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        border: '1px solid white',
        borderRadius: '16px',
        boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.6)'
      }}>
        <Typography sx={{
          color: 'whitesmoke',
          fontWeight: 'bold',
          fontSize: '2rem',
          marginBottom: '5%',
        }}>
          Worker Guardian App
        </Typography>

        <FormControl sx={{ width: '100%' }}>
          <TextField 
            label='Username' 
            variant='standard' 
            required 
            error={errors.loginError} 
            helperText={errors.loginError ? 'Insert username!' : ''}
            value={user.userLogin}
            onChange={(e) => { setUser((prev) => ({ ...prev, userLogin: e.target.value })); }}
          />
          
          <TextField 
            label='Password' 
            variant='standard' 
            required 
            error={errors.passwordError} 
            helperText={errors.passwordError ? 'Insert password!' : ''}
            type='password' 
            value={user.userPassword}
            onChange={(e) => { setUser((prev) => ({ ...prev, userPassword: e.target.value })); }} 
            sx={{ marginTop: '10%' }}
          />
          
          <Button 
            type="submit"
            sx={{
              color: 'whitesmoke',
              backgroundColor: 'black',
              width: '100%',
              marginTop: '10%',
              '&:hover': {
                backgroundColor: 'grey'
              }
            }}
          >
            Login
          </Button>

          {
            errors.serverAns && 
              <Typography align='center' sx={{
                color: 'error.main',
                marginTop: '10%'
              }}>
                {errors.serverAns}
              </Typography>
          }
        </FormControl>
      </Box>
    </Box>
  );
};

export default LoginPage;
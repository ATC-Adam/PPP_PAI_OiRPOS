import React, { useState } from 'react';
import { useAuth } from '../providers/AuthContext';

import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { FormControl, Typography } from '@mui/material';
import { Box } from '@mui/material';

const LoginPage = () => {
  const { login } = useAuth();

  const [user, setUser] = useState({
    userLogin: null,
    userPassword: null
  })

  const [errors, setErrors] = useState({
    loginError: false,
    passwordError: false,
    serverAns: ''
  })

  const handleSubmit = () => {
    const newErrors = {
      loginError: !user.userLogin,
      passwordError: !user.userPassword
    };
  
    setErrors(newErrors);

    if (!newErrors.loginError && !newErrors.passwordError) 
      login(user.userLogin, user.userPassword, (errorMessage) => { 
        setErrors((prev) => ({ ...prev, serverAns: errorMessage }));
      });
  }

  return (
    <>
    <Box sx={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
    }}>
      <Box sx={{
        width: '25vw',
        height: '40vh',
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

        <FormControl sx={{width: '50%'}}>
          <TextField label='Username' 
            variant='standard' 
            required 
            error = { errors.loginError } 
            helperText = { errors.loginError ? 'Insert username!' : '' }
            onChange={(e) => { setUser((prev) => ({ ...prev, userLogin: e.target.value })); }}
          />
            
          <TextField label='Password' 
            variant='standard' 
            required 
            error={errors.passwordError} 
            helperText = { errors.loginError ? 'Insert password!' : '' }
            type='password' 
            onChange={(e) => { setUser((prev) => ({ ...prev, userPassword: e.target.value })); }} 
            sx={{marginTop: '10%'}}
          />
            
          <Button onClick={handleSubmit} 
            sx={{
              color: 'whitesmoke',
              backgroundColor: 'black',
              width: '50%',
              marginTop: '10%',
              marginLeft: '25%'
              }}>
            Login
          </Button>

          {
            errors.serverAns ? 
              <Typography align='center' sx={{
                color: 'error.main',
                marginTop: '10%'
              }}>
                {errors.serverAns}
              </Typography> 
            : 
            <></>
          }
        </FormControl>
      </Box>
    </Box>
    </>
  );
};

export default LoginPage;
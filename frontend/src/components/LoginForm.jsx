import React, { useState } from "react";
import { login, signup, getMe } from "../api/auth";
import { TextField, Button, Typography, Box, Paper, Switch, FormControlLabel } from "@mui/material";
import { t } from "../i18n";
import "./LoginForm.css";

export default function LoginForm({ onLogin, language, theme }) {
  const [isSignup, setIsSignup] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    
    try {
      if (isSignup) {
        // Registration
        await signup({
          username,
          full_name: fullName,
          email,
          password
        });
        setSuccess(t('registrationSuccess', language));
        // Clear fields after successful registration
        setUsername("");
        setPassword("");
        setFullName("");
        setEmail("");
        setIsSignup(false);
      } else {
        // Login
        await login(username, password);
        const user = await getMe();
        onLogin(user);
      }
    } catch (err) {
      if (isSignup) {
        setError(err.response?.data?.detail || t('registrationError', language));
      } else {
        setError(t('invalidCredentials', language));
      }
    }
  };

  const handleModeToggle = () => {
    setIsSignup(!isSignup);
    setError("");
    setSuccess("");
  };

  return (
    <div className={`login-container login-${theme}`}>
      <Box 
        component={Paper} 
        elevation={3} 
        className={`login-card login-card-${theme}`}
      >
        <Typography variant="h5" gutterBottom align="center" className="login-title">
          {isSignup ? t('register', language) : t('login', language)}
        </Typography>
        
        <FormControlLabel
          control={
            <Switch
              checked={isSignup}
              onChange={handleModeToggle}
              color="primary"
            />
          }
          label={isSignup ? t('switchToLogin', language) : t('switchToRegister', language)}
          className="mode-toggle"
        />

        <form onSubmit={handleSubmit} className="login-form">
          {isSignup && (
            <TextField
              label={t('fullName', language)}
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              fullWidth
              margin="normal"
              required={isSignup}
              className={`login-input login-input-${theme}`}
            />
          )}
          
          {isSignup && (
            <TextField
              label={t('email', language)}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              fullWidth
              margin="normal"
              required={isSignup}
              className={`login-input login-input-${theme}`}
            />
          )}

          <TextField
            label={t('username', language)}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            fullWidth
            margin="normal"
            required
            className={`login-input login-input-${theme}`}
          />
          
          <TextField
            label={t('password', language)}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            fullWidth
            margin="normal"
            required
            className={`login-input login-input-${theme}`}
          />
          
          <Button 
            type="submit" 
            variant="contained" 
            fullWidth 
            className={`login-button login-button-${theme}`}
          >
            {isSignup ? t('register', language) : t('enter', language)}
          </Button>
          
          {error && (
            <Typography color="error" className="login-error">
              {error}
            </Typography>
          )}
          
          {success && (
            <Typography color="success.main" className="login-success">
              {success}
            </Typography>
          )}
        </form>
      </Box>
    </div>
  );
}

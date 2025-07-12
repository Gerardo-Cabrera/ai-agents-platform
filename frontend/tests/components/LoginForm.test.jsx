import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import LoginForm from '../../src/components/LoginForm';
import { t } from '../../src/i18n';

// Mock the auth API
jest.mock('../../src/api/auth', () => ({
  login: jest.fn()
}));

const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('LoginForm Component', () => {
  const mockOnLogin = jest.fn();
  const mockProps = {
    onLogin: mockOnLogin,
    language: 'es'
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders login form with all elements', () => {
    renderWithRouter(<LoginForm {...mockProps} />);
    
    // Check for form elements using Spanish labels
    expect(screen.getByLabelText(/usuario/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/contraseña/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { type: 'submit' })).toBeInTheDocument();
  });

  test('handles form submission with valid data', async () => {
    const { login } = require('../../src/api/auth');
    login.mockResolvedValueOnce({ access_token: 'test-token' });

    renderWithRouter(<LoginForm {...mockProps} />);
    
    const usernameInput = screen.getByLabelText(/usuario/i);
    const passwordInput = screen.getByLabelText(/contraseña/i);
    const submitButton = screen.getByRole('button', { type: 'submit' });

    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'testpass' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(login).toHaveBeenCalledWith('testuser', 'testpass');
    });
  });

  test('shows error message on login failure in Spanish', async () => {
    const { login } = require('../../src/api/auth');
    login.mockRejectedValueOnce(new Error('Invalid credentials'));

    renderWithRouter(<LoginForm {...mockProps} />);
    
    const usernameInput = screen.getByLabelText(/usuario/i);
    const passwordInput = screen.getByLabelText(/contraseña/i);
    const submitButton = screen.getByRole('button', { type: 'submit' });

    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'wrongpass' } });
    fireEvent.click(submitButton);

    const errorMessage = t('invalidCredentials', 'es');
    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  test('shows error message on login failure in English', async () => {
    const { login } = require('../../src/api/auth');
    login.mockRejectedValueOnce(new Error('Invalid credentials'));

    const englishProps = { ...mockProps, language: 'en' };
    renderWithRouter(<LoginForm {...englishProps} />);
    
    const usernameInput = screen.getByLabelText(/username/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { type: 'submit' });

    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'wrongpass' } });
    fireEvent.click(submitButton);

    const errorMessage = t('invalidCredentials', 'en');
    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  test('validates required fields', async () => {
    renderWithRouter(<LoginForm {...mockProps} />);
    
    const submitButton = screen.getByRole('button', { type: 'submit' });
    fireEvent.click(submitButton);

    // Check that form elements are still present (no validation errors shown)
    expect(screen.getByLabelText(/usuario/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/contraseña/i)).toBeInTheDocument();
  });

  test('form elements have correct attributes', () => {
    renderWithRouter(<LoginForm {...mockProps} />);
    
    const usernameInput = screen.getByLabelText(/usuario/i);
    const passwordInput = screen.getByLabelText(/contraseña/i);
    
    expect(usernameInput).toHaveAttribute('type', 'text');
    expect(passwordInput).toHaveAttribute('type', 'password');
    expect(usernameInput).toBeRequired();
    expect(passwordInput).toBeRequired();
  });
}); 
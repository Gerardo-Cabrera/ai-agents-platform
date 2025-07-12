import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import NavBar from '../../src/components/NavBar';

const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('NavBar Component', () => {
  const mockProps = {
    language: 'es',
    setLanguage: jest.fn(),
    theme: 'light',
    setTheme: jest.fn(),
    onLogout: jest.fn(),
    user: null // Simulates not authenticated
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders navbar with all elements', () => {
    renderWithRouter(<NavBar {...mockProps} />);
    expect(screen.getByText('Agent IA')).toBeInTheDocument();
    expect(screen.getByLabelText('Idioma')).toBeInTheDocument();
    expect(screen.getByLabelText('Tema')).toBeInTheDocument();
  });

  test('language selector changes language', () => {
    renderWithRouter(<NavBar {...mockProps} />);
    const languageSelector = screen.getByLabelText('Idioma');
    fireEvent.change(languageSelector, { target: { value: 'en' } });
    expect(mockProps.setLanguage).toHaveBeenCalledWith('en');
  });

  test('theme toggle button changes theme', () => {
    renderWithRouter(<NavBar {...mockProps} />);
    const themeButton = screen.getByTitle('Oscuro');
    fireEvent.click(themeButton);
    expect(mockProps.setTheme).toHaveBeenCalled();
  });

  test('shows login link when not authenticated', () => {
    renderWithRouter(<NavBar {...mockProps} />);
    // Should not show logout button when no user is authenticated
    expect(screen.queryByText('Cerrar sesión')).not.toBeInTheDocument();
    expect(screen.queryByText('Logout')).not.toBeInTheDocument();
  });

  test('shows logout button when authenticated', () => {
    const authenticatedProps = { ...mockProps, user: { username: 'test' } };
    renderWithRouter(<NavBar {...authenticatedProps} />);
    // Should show logout button with text based on language
    expect(screen.getByText('Cerrar sesión')).toBeInTheDocument();
    expect(screen.queryByText('Iniciar sesión')).not.toBeInTheDocument();
  });

  test('logout button calls onLogout', () => {
    const authenticatedProps = { ...mockProps, user: { username: 'test' } };
    renderWithRouter(<NavBar {...authenticatedProps} />);
    const logoutButton = screen.getByText('Cerrar sesión');
    fireEvent.click(logoutButton);
    expect(mockProps.onLogout).toHaveBeenCalled();
  });

  test('applies correct theme classes', () => {
    const darkProps = { ...mockProps, theme: 'dark' };
    const { container } = renderWithRouter(<NavBar {...darkProps} />);
    expect(container.firstChild).toHaveClass('navbar-dark');
  });

  test('displays correct language options', () => {
    renderWithRouter(<NavBar {...mockProps} />);
    const languageSelector = screen.getByLabelText('Idioma');
    const options = languageSelector.querySelectorAll('option');
    expect(options).toHaveLength(2);
    expect(options[0]).toHaveValue('es');
    expect(options[1]).toHaveValue('en');
  });

  test('logout button text changes with language', () => {
    const authenticatedProps = { ...mockProps, user: { username: 'test' }, language: 'en' };
    renderWithRouter(<NavBar {...authenticatedProps} />);
    expect(screen.getByText('Logout')).toBeInTheDocument();
    expect(screen.queryByText('Cerrar sesión')).not.toBeInTheDocument();
  });
}); 
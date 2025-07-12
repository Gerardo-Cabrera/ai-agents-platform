import React from 'react';
import { t, getAvailableLanguages } from '../i18n';
import { logout } from '../api/auth';
import './NavBar.css';

export default function NavBar({ language, setLanguage, theme, setTheme, onLogout, user }) {
  const languages = getAvailableLanguages();

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  const handleThemeChange = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  const handleLogout = () => {
    logout();
    if (onLogout) {
      onLogout();
    }
  };

  return (
    <nav className={`navbar navbar-${theme}`}>
      <div className="navbar-container">
        <div className="navbar-brand">
          <h1 className="navbar-title">Agent IA</h1>
        </div>
        
        <div className="navbar-controls">
          {/* Language selector */}
          <div className="control-group">
            <label htmlFor="language-select" className="control-label">
              {t('language', language)}
            </label>
            <select
              id="language-select"
              value={language}
              onChange={handleLanguageChange}
              className={`select-control select-${theme}`}
            >
              {languages.map(lang => (
                <option key={lang.code} value={lang.code}>
                  {lang.name}
                </option>
              ))}
            </select>
          </div>

          {/* Theme selector */}
          <div className="control-group">
            <label htmlFor="theme-toggle" className="control-label">
              {t('theme', language)}
            </label>
            <button
              id="theme-toggle"
              onClick={handleThemeChange}
              className={`theme-toggle theme-toggle-${theme}`}
              title={theme === 'light' ? t('dark', language) : t('light', language)}
            >
              {theme === 'light' ? '🌙' : '☀️'}
            </button>
          </div>

          {/* Logout button - only show when user is authenticated */}
          {user && (
            <div className="control-group">
              <button
                onClick={handleLogout}
                className={`logout-button logout-button-${theme}`}
                title={t('logout', language)}
              >
                {t('logout', language)}
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
} 
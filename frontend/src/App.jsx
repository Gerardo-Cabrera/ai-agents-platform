import React, { useState, useEffect, createContext, useContext } from "react";
import LoginForm from "./components/LoginForm";
import Chat from "./components/Chat";
import NavBar from "./components/NavBar";
import { t } from "./i18n";
import { getMe } from "./api/auth";

// Global state context for scalable state management
const AppContext = createContext();

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};

const AppProvider = ({ children }) => {
  // Force default language to English on first load
  useEffect(() => {
    localStorage.setItem("language", "en");
  }, []);

  const [user, setUser] = useState(null);
  const [language, setLanguage] = useState("en");
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem("theme") || "light";
    return savedTheme;
  });
  const [loadingUser, setLoadingUser] = useState(true);

  // Apply theme to body immediately and on theme change
  useEffect(() => {
    document.body.style.background = theme === 'dark' ? '#222' : '#fff';
    document.body.style.color = theme === 'dark' ? '#fff' : '#222';
    document.body.classList.remove('theme-light', 'theme-dark');
    document.body.classList.add(`theme-${theme}`);
  }, [theme]);

  // Restore user session if token exists
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      getMe().then(
        (u) => {
          setUser(u);
          setLoadingUser(false);
        },
        () => setLoadingUser(false)
      );
    } else {
      setLoadingUser(false);
    }
  }, []);

  // Save preferences in localStorage when they change
  useEffect(() => {
    localStorage.setItem("theme", theme);
  }, [theme]);

  useEffect(() => {
    localStorage.setItem("language", language);
  }, [language]);

  const handleLogout = () => {
    setUser(null);
  };

  const value = {
    user,
    setUser,
    language,
    setLanguage,
    theme,
    setTheme,
    loadingUser,
    handleLogout
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

function App() {
  const { user, setUser, loadingUser, handleLogout, language, setLanguage, theme, setTheme } = useAppContext();

  if (loadingUser) {
    return <div style={{padding: '2rem', textAlign: 'center'}}>{t('loading', language)}...</div>;
  }

  if (!user) {
    return <LoginForm onLogin={setUser} language={language} theme={theme} />;
  }

  return (
    <div>
      <NavBar 
        language={language} 
        setLanguage={setLanguage} 
        theme={theme} 
        setTheme={setTheme}
        onLogout={handleLogout}
        user={user}
      />
      <div className="main-content">
        <h1>{t('welcome', language)}, {user.full_name || user.username}!</h1>
        <Chat language={language} theme={theme} />
      </div>
    </div>
  );
}

// Wrap the main App component with the provider
const AppWithProvider = () => (
  <AppProvider>
    <App />
  </AppProvider>
);

export default AppWithProvider;

import React, { useState } from "react";
import { useWebSocket } from "../api/useWebSocket";
import { t } from "../i18n";
import "./ChatWS.css";

export default function ChatWS({ language, theme }) {
  const token = localStorage.getItem("access_token");
  const { messages, sendMessage, status } = useWebSocket("ws://localhost:8000/ws/chat", token);
  const [input, setInput] = useState("");

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessage(input);
    setInput("");
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'connected':
        return t('connected', language);
      case 'disconnected':
        return t('disconnected', language);
      case 'connecting':
        return t('connecting', language);
      case 'reconnecting':
        return t('reconnecting', language);
      default:
        return status;
    }
  };

  return (
    <div className={`chatws-container chatws-${theme}`}>
      <div className="chatws-header">
        <h2 className="chatws-title">{t('realtimeChat', language)}</h2>
        <div className={`status-indicator status-${status} status-${theme}`}>
          {getStatusText(status)}
        </div>
      </div>
      
      <div className={`messages-container messages-${theme}`}>
        {messages.length === 0 ? (
          <div className="no-messages">
            {t('writeMessage', language)}
          </div>
        ) : (
          messages.map((msg, i) => (
            <div key={i} className={`message-item message-${theme}`}>
              {msg}
            </div>
          ))
        )}
      </div>
      
      <form onSubmit={handleSend} className="chatws-form">
        <div className="input-group">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t('message', language)}
            className={`chatws-input chatws-input-${theme}`}
          />
          <button 
            type="submit" 
            className={`chatws-button chatws-button-${theme}`}
            disabled={!input.trim() || status !== 'connected'}
          >
            {t('send', language)}
          </button>
        </div>
      </form>
    </div>
  );
} 
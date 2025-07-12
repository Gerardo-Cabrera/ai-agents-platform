import React, { useState } from "react";
import { useWebSocket } from "../api/useWebSocket";
import { t } from "../i18n";
import "./DataAnalysisWS.css";

export default function DataAnalysisWS({ language, theme }) {
  const token = localStorage.getItem("access_token");
  const { messages, sendMessage, status } = useWebSocket("ws://localhost:8000/ws/data", token);
  const [query, setQuery] = useState("");

  const handleSend = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    sendMessage(query);
    setQuery("");
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
    <div className={`data-analysis-container data-analysis-${theme}`}>
      <div className="data-analysis-header">
        <h2 className="data-analysis-title">{t('dataAnalysis', language)}</h2>
        <div className={`status-indicator status-${status} status-${theme}`}>
          {getStatusText(status)}
        </div>
      </div>
      
      <form onSubmit={handleSend} className="data-analysis-form">
        <div className="input-group">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={t('analysisQuery', language)}
            className={`data-analysis-input data-analysis-input-${theme}`}
          />
          <button 
            type="submit" 
            className={`data-analysis-button data-analysis-button-${theme}`}
            disabled={!query.trim() || status !== 'connected'}
          >
            {t('sendQuery', language)}
          </button>
        </div>
      </form>
      
      <div className={`results-container results-${theme}`}>
        <h3 className="results-title">{t('response', language)}</h3>
        {messages.length === 0 ? (
          <div className="no-results">
            {t('analysisQuery', language)}
          </div>
        ) : (
          <div className="results-list">
            {messages.map((msg, i) => (
              <div key={i} className={`result-item result-${theme}`}>
                <div className="result-content">{msg}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
} 
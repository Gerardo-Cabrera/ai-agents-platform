import React from "react";
import { useWebSocket } from "../api/useWebSocket";
import { t } from "../i18n";
import "./NotificationsWS.css";

export default function NotificationsWS({ language, theme }) {
  const token = localStorage.getItem("access_token");
  const { messages, status } = useWebSocket("ws://localhost:8000/ws/notifications", token);

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
    <div className={`notifications-container notifications-${theme}`}>
      <div className="notifications-header">
        <h2 className="notifications-title">{t('notifications', language)}</h2>
        <div className={`status-indicator status-${status} status-${theme}`}>
          {getStatusText(status)}
        </div>
      </div>
      
      <div className={`notifications-list notifications-list-${theme}`}>
        {messages.length === 0 ? (
          <div className="no-notifications">
            {t('loading', language)}...
          </div>
        ) : (
          messages.map((msg, i) => (
            <div key={i} className={`notification-item notification-${theme}`}>
              <div className="notification-icon">🔔</div>
              <div className="notification-content">{msg}</div>
              <div className="notification-time">
                {new Date().toLocaleTimeString()}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
} 
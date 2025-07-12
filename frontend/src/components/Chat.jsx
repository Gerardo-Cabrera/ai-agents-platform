import React, { useState, useEffect } from "react";
import api, {
  fetchConversations,
  fetchConversationHistory,
  deleteConversation,
  renameConversation
} from "../api/client";
import { t } from "../i18n";
import "./Chat.css";

// Iconos Material (SVG inline)
const PencilIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19.5 3 21l1.5-4L16.5 3.5z"/></svg>
);
const TrashIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/></svg>
);
const PlusIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
);
const ChatIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
);

export default function Chat({ language, theme }) {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [history, setHistory] = useState([]);
  const [renamingId, setRenamingId] = useState(null);
  const [renameValue, setRenameValue] = useState("");

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    if (selectedId) {
      fetchConversationHistory(selectedId).then(res => {
        setHistory(res.data.messages || []);
      });
    } else {
      setHistory([]);
    }
  }, [selectedId]);

  async function loadConversations() {
    const res = await fetchConversations();
    setConversations(res.data.conversations || []);
    if (!selectedId && res.data.conversations?.length) {
      setSelectedId(res.data.conversations[0].id);
    }
  }

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!message.trim() || isLoading) return;
    setIsLoading(true);
    try {
      const res = await api.post("/chat/message", {
        message: message.trim(),
        conversation_id: selectedId,
        temperature: 0.7
      });
      // If the response is the translation key, show the translation
      const resp = res.data.response;
      console.log('Response from backend:', resp);
      console.log('Current language:', language);
      console.log('Translation result:', t('serviceUnavailable', language));
      
      if (resp === 'serviceUnavailable') {
        setResponse(t('serviceUnavailable', language));
      } else if (typeof resp === 'string' && resp in t('', language, true)) {
        setResponse(t(resp, language));
      } else {
        setResponse(resp);
      }
      setMessage("");
      if (!selectedId && res.data.conversation_id) {
        setSelectedId(res.data.conversation_id);
      }
      await loadConversations();
      fetchConversationHistory(res.data.conversation_id || selectedId).then(res2 => {
        setHistory(res2.data.messages || []);
      });
    } catch (error) {
      console.error('Chat error:', error);
      setResponse(t('errorProcessing', language));
    } finally {
      setIsLoading(false);
    }
  };

  async function handleDelete(id) {
    if (window.confirm(t('deleteConfirm', language) || '¿Eliminar conversación?')) {
      await deleteConversation(id);
      await loadConversations();
      if (selectedId === id) {
        setSelectedId(null);
        setHistory([]);
        setResponse("");
      }
    }
  }

  function handleRename(id, currentTitle) {
    setRenamingId(id);
    setRenameValue(currentTitle);
  }

  async function handleRenameSubmit(id) {
    if (renameValue.trim()) {
      await renameConversation(id, renameValue.trim());
      setRenamingId(null);
      setRenameValue("");
      await loadConversations();
    }
  }

  function handleNewConversation() {
    setSelectedId(null);
    setHistory([]);
    setResponse("");
  }

  function Sidebar() {
    return (
      <aside className={`sidebar sidebar-${theme}`}>
        <div className="sidebar-header">
          <span className="sidebar-title"><ChatIcon /> {t('conversations', language)}</span>
          <button className="sidebar-btn" title={t('newConversation', language)} onClick={handleNewConversation}><PlusIcon /></button>
        </div>
        <ul className="sidebar-list">
          {conversations.map(conv => (
            <li key={conv.id} className={`sidebar-item${conv.id === selectedId ? ' selected' : ''}`}> 
              <button className="sidebar-item-main" onClick={() => setSelectedId(conv.id)}>
                <span className="sidebar-item-icon"><ChatIcon /></span>
                {renamingId === conv.id ? (
                  <input
                    className="sidebar-rename-input"
                    value={renameValue}
                    onChange={e => setRenameValue(e.target.value)}
                    onBlur={() => handleRenameSubmit(conv.id)}
                    onKeyDown={e => e.key === 'Enter' && handleRenameSubmit(conv.id)}
                    autoFocus
                  />
                ) : (
                  <span className="sidebar-item-title">{conv.title}</span>
                )}
              </button>
              <button className="sidebar-btn" title={t('rename', language)} onClick={() => handleRename(conv.id, conv.title)}><PencilIcon /></button>
              <button className="sidebar-btn" title={t('delete', language)} onClick={() => handleDelete(conv.id)}><TrashIcon /></button>
            </li>
          ))}
        </ul>
      </aside>
    );
  }

  function ChatHistory() {
    const hasContent = history.length > 0 || !!response || isLoading;
    return (
      <div className={`chat-history${hasContent ? ' chat-history-has-content' : ''}`}>
        {history.length === 0 && <div className="no-messages">{t('noMessages', language)}</div>}
        {history.map((msg, i) => (
          <div key={i} className={`chat-bubble ${msg.message_type === 'USER' ? 'user' : 'assistant'} chat-bubble-${theme}`}>
            <span className="chat-bubble-content">{
              msg.content === 'serviceUnavailable'
                ? t('serviceUnavailable', language)
                : msg.content
            }</span>
          </div>
        ))}
        {/* Show spinner/indicator if waiting for response */}
        {isLoading && (
          <div className={`chat-bubble assistant chat-bubble-${theme} chat-bubble-latest`}>
            <span className="chat-bubble-content">
              <span className="thinking-indicator">
                <svg width="24" height="24" viewBox="0 0 50 50" style={{verticalAlign:'middle',marginRight:'8px'}}>
                  <circle cx="25" cy="25" r="20" fill="none" stroke="#888" strokeWidth="5" strokeDasharray="31.4 31.4" strokeLinecap="round">
                    <animateTransform attributeName="transform" type="rotate" from="0 25 25" to="360 25 25" dur="1s" repeatCount="indefinite" />
                  </circle>
                </svg>
                {t('thinking', language) || 'Thinking...'}
              </span>
            </span>
          </div>
        )}
        {/* Only show the latest response if it's not already in history */}
        {response && (history.length === 0 || (history[history.length-1]?.content !== response)) && !isLoading && (
          <div className={`chat-bubble assistant chat-bubble-${theme} chat-bubble-latest`}>
            <span className="chat-bubble-content">{
              response === 'serviceUnavailable'
                ? t('serviceUnavailable', language)
                : response
            }</span>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="chat-app">
      <Sidebar />
      <div className={`chat-main chat-main-${theme}`}>
        <div className="chat-header">
          <h2>{t('aiAssistant', language)}</h2>
          <p>{t('aiAssistantDesc', language)}</p>
        </div>
        <ChatHistory />
        <form onSubmit={sendMessage} className="chat-form">
          <div className="input-group">
            <input
              value={message}
              onChange={e => setMessage(e.target.value)}
              placeholder={t('writeMessage', language) + '...'}
              className={`chat-input chat-input-${theme}`}
              disabled={isLoading}
            />
            <button 
              type="submit" 
              className={`chat-button chat-button-${theme}`}
              disabled={!message.trim() || isLoading}
            >
              {isLoading ? t('sending', language) : t('send', language)}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

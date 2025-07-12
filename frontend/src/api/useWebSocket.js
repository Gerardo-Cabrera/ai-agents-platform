import { useEffect, useRef, useState } from "react";

/**
 * Hook para conectar a cualquier WebSocket autenticado con JWT.
 * @param {string} url - URL del WebSocket (ws://...)
 * @param {string} token - JWT de autenticación
 * @returns { messages, sendMessage, status }
 */
export function useWebSocket(url, token) {
  const ws = useRef(null);
  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState("closed");

  useEffect(() => {
    if (!token) return;
    ws.current = new window.WebSocket(`${url}?token=${token}`);
    setStatus("connecting");

    ws.current.onopen = () => setStatus("open");
    ws.current.onclose = () => setStatus("closed");
    ws.current.onerror = () => setStatus("error");
    ws.current.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

    return () => {
      ws.current && ws.current.close();
    };
  }, [url, token]);

  const sendMessage = (msg) => {
    if (ws.current && ws.current.readyState === 1) {
      ws.current.send(msg);
    }
  };

  return { messages, sendMessage, status };
} 
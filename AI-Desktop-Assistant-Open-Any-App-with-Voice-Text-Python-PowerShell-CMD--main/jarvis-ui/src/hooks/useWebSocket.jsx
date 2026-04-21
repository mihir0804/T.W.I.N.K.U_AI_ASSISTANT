import { useEffect, useRef, useCallback, useState } from 'react';

/**
 * Custom hook for WebSocket connection management
 */
const useWebSocket = (url, options = {}) => {
  const { onMessage, reconnectInterval = 3000 } = options;
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);
  const [isConnected, setIsConnected] = useState(false);

  const connect = useCallback(() => {
    try {
      const wsUrl = import.meta.env.VITE_WS_URL || url;
      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        if (import.meta.env.DEV) {
          console.log('✅ WebSocket connected');
        }
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (onMessage) {
            onMessage(data);
          }
        } catch (err) {
          if (import.meta.env.DEV) {
            console.error('WebSocket message parse error:', err);
          }
        }
      };

      ws.onerror = (error) => {
        if (import.meta.env.DEV) {
          console.log('WebSocket error (backend not running, using demo mode):', error);
        }
        setIsConnected(false);
      };

      ws.onclose = () => {
        if (import.meta.env.DEV) {
          console.log('WebSocket closed, will retry...');
        }
        setIsConnected(false);
        reconnectTimeoutRef.current = setTimeout(() => {
          connect();
        }, reconnectInterval);
      };

      wsRef.current = ws;
    } catch (err) {
      if (import.meta.env.DEV) {
        console.log('WebSocket connection failed (demo mode active)');
      }
      setIsConnected(false);
    }
  }, [url, onMessage, reconnectInterval]);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect]);

  return { wsRef, isConnected };
};

export default useWebSocket;

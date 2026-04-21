import { useState, useEffect, useCallback } from 'react';

const useWebSocket = (url, { onMessage, reconnectInterval = 3000 } = {}) => {
  const [isConnected, setIsConnected] = useState(false);
  const [ws, setWs] = useState(null);

  const connect = useCallback(() => {
    const socket = new WebSocket(url);

    socket.onopen = () => {
      console.log('🔗 WebSocket Connected to Twinku Backend');
      setIsConnected(true);
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (onMessage) onMessage(data);
      } catch (e) {
        console.error('Error parsing WebSocket message', e);
      }
    };

    socket.onclose = () => {
      console.log('🔴 WebSocket Disconnected. Reconnecting...');
      setIsConnected(false);
      setTimeout(connect, reconnectInterval);
    };

    socket.onerror = (err) => {
      console.error('WebSocket Error:', err);
      socket.close();
    };

    setWs(socket);

    return socket;
  }, [url, onMessage, reconnectInterval]);

  useEffect(() => {
    const socket = connect();
    return () => {
      if (socket) {
        // Prevent reconnect loop on unmount
        socket.onclose = () => {}; 
        socket.close();
      }
    };
  }, [connect]);

  return { isConnected, ws };
};

export default useWebSocket;

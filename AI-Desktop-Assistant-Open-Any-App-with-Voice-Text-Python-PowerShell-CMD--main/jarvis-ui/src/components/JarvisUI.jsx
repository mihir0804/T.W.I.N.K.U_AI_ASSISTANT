import React, { useEffect, useState, useCallback } from 'react';
import Waveform from './Waveform';
import SVGLayers from './SVGLayers';
import ConversationDisplay from './ConversationDisplay';
import useWebSocket from '../hooks/useWebSocket';

const JarvisUI = () => {
  const [status, setStatus] = useState('idle'); // idle, listening, speaking
  const [audioLevel, setAudioLevel] = useState(0);
  const [transcript, setTranscript] = useState('');
  const [messages, setMessages] = useState([]);

  // WebSocket message handler
  const handleWebSocketMessage = useCallback((data) => {
    if (data.status) {
      setStatus(data.status);
    }

    if (data.audioLevel !== undefined) {
      setAudioLevel(data.audioLevel);
    }

    if (data.transcript) {
      setTranscript(data.transcript);
      
      // Parse and add to conversation
      const text = data.transcript;
      if (text.startsWith('You:') || text.startsWith('Twinku:')) {
        const isUser = text.startsWith('You:');
        const cleanText = text.replace(/^(You:|Twinku:)\s*/, '');
        
        setMessages((prev) => [
          ...prev,
          {
            id: `msg-${Date.now()}`,
            type: isUser ? 'user' : 'twinku',
            text: cleanText,
            time: new Date().toLocaleTimeString(),
          },
        ]);
      }
    }
  }, []);

  const [isMicEnabled, setIsMicEnabled] = useState(true);

  // WebSocket connection
  const { isConnected, ws } = useWebSocket('ws://localhost:8765', {
    onMessage: handleWebSocketMessage,
    reconnectInterval: 3000,
  });

  const toggleMic = () => {
    const newState = !isMicEnabled;
    setIsMicEnabled(newState);
    if (ws && isConnected) {
      try {
        ws.send(JSON.stringify({ action: "toggle_mic", state: newState }));
      } catch (e) {
        console.error("Failed to send message: ", e);
      }
    }
  };

  // Demo mode - cycle through states when backend not connected
  useEffect(() => {
    if (isConnected) {
      return; // Don't run demo mode if connected
    }

    const demoInterval = setInterval(() => {
      setStatus((prevStatus) => {
        if (prevStatus === 'idle') return 'listening';
        if (prevStatus === 'listening') return 'speaking';
        return 'idle';
      });

      // Simulate audio level when speaking
      setAudioLevel((prevLevel) => {
        if (status === 'speaking') {
          return Math.random() * 0.8 + 0.2;
        }
        return prevLevel;
      });
    }, 3000);

    return () => clearInterval(demoInterval);
  }, [isConnected, status]);

  return (
    <div className="jarvis-container">
      {/* Background */}
      <div className="jarvis-background" />

      {/* Main HUD Container */}
      <div className="jarvis-hud">
        {/* SVG Layers */}
        <SVGLayers />

        {/* Central Waveform */}
        <div className="waveform-container">
          <Waveform status={status} audioLevel={audioLevel} />
        </div>

        {/* Status Indicator */}
        <StatusIndicator 
          status={status} 
          isConnected={isConnected} 
          isMicEnabled={isMicEnabled} 
          toggleMic={toggleMic} 
        />

        {/* Transcript Display (old, kept for compatibility) */}
        {transcript && !transcript.includes('You:') && !transcript.includes('Twinku:') && (
          <TranscriptDisplay transcript={transcript} />
        )}
      </div>

      {/* Conversation Display - New Feature */}
      <ConversationDisplay messages={messages} currentStatus={status} />
    </div>
  );
};

const StatusIndicator = ({ status, isConnected, isMicEnabled, toggleMic }) => {
  const statusLabels = {
    idle: 'Idle',
    listening: 'Listening',
    speaking: 'Speaking',
  };

  return (
    <div className="status-indicator-container">
      <div className="status-indicator">
        <div className={`status-dot status-${status}`} />
        <span className="status-text">{statusLabels[status] || 'Unknown'}</span>
        {!isConnected && <span className="demo-badge">DEMO</span>}
      </div>
      <button 
        className={`mic-toggle-btn ${isMicEnabled ? 'mic-on' : 'mic-off'}`} 
        onClick={toggleMic}
        title={isMicEnabled ? "Mute Microphone" : "Unmute Microphone"}
      >
        {isMicEnabled ? '🎤 MIC ON' : '🔇 MIC OFF'}
      </button>
    </div>
  );
};

const TranscriptDisplay = ({ transcript }) => (
  <div className="transcript-display">
    <p>{transcript}</p>
  </div>
);

export default JarvisUI;

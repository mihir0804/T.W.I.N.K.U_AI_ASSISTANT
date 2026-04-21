import React from 'react';

const ConversationDisplay = ({ messages, currentStatus }) => {
  // Status display labels
  const statusLabels = {
    idle: '💤 Sleeping...',
    listening: '👂 Listening...',
    speaking: '🗣️ Speaking...',
  };

  return (
    <div className="conversation-container">
      {/* Current Status Banner */}
      <div className={`status-banner status-banner-${currentStatus}`}>
        <div className="status-pulse" />
        <span className="status-label">
          {statusLabels[currentStatus] || '⚡ Active'}
        </span>
      </div>

      {/* Conversation Messages */}
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="no-messages">
            <p className="hint-text">Say the wake word to start...</p>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`message-item ${msg.type}`}
              >
                <div className="message-avatar">
                  {msg.type === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-bubble">
                  <span className="message-label">
                    {msg.type === 'user' ? 'You' : 'Twinku'}
                  </span>
                  <p className="message-text">{msg.text}</p>
                  <span className="message-time">{msg.time}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ConversationDisplay;

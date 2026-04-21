import React from 'react';

const generateNodeId = (index) => `node-${index}`;

const SVGLayers = () => {
  return (
    <svg
      width="800"
      height="800"
      viewBox="0 0 800 800"
      className="jarvis-svg"
    >
      <defs>
        <radialGradient id="bgGradient" cx="50%" cy="50%">
          <stop offset="0%" stopColor="#0a0020" />
          <stop offset="100%" stopColor="#000000" />
        </radialGradient>

        <linearGradient id="cyanGlow" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#00f5ff" stopOpacity="1" />
          <stop offset="100%" stopColor="#00d4ff" stopOpacity="0.8" />
        </linearGradient>

        <linearGradient id="magentaGlow" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#ff00ff" stopOpacity="1" />
          <stop offset="100%" stopColor="#d000d0" stopOpacity="0.8" />
        </linearGradient>

        <linearGradient id="purpleGlow" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#5a00ff" stopOpacity="1" />
          <stop offset="100%" stopColor="#4500cc" stopOpacity="0.8" />
        </linearGradient>

        <filter id="glow-cyan" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="4" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>

        <filter id="glow-magenta" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="6" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>

        <filter id="glow-soft" x="-100%" y="-100%" width="300%" height="300%">
          <feGaussianBlur stdDeviation="10" result="coloredBlur" />
          <feMerge>
            <feMergeNode in="coloredBlur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      <g className="outer-ring-group">
        <path
          d="M 170,260 C 130,330 120,400 130,470 C 145,540 180,600 240,640 C 310,685 380,695 450,680 C 520,665 580,630 630,570 C 675,515 685,450 675,385 C 665,315 630,250 570,200 C 510,150 430,125 360,130 C 290,135 220,180 170,260 Z"
          fill="none"
          stroke="url(#cyanGlow)"
          strokeWidth="2"
          opacity="0.45"
          className="rotating-ring"
        />
      </g>

      <TickMarks />
      <ConnectionArcs />
      <GlowingNodes />

      <circle
        cx="400"
        cy="400"
        r="220"
        fill="none"
        stroke="url(#magentaGlow)"
        strokeWidth="3"
        opacity="0.8"
        filter="url(#glow-magenta)"
      />

      <LevelIndicators />
      <Title />
    </svg>
  );
};

const TickMarks = () => {
  const tickCount = 120;
  const ticks = [];

  for (let i = 0; i < tickCount; i++) {
    const angle = (i * 3 * Math.PI) / 180;
    const r1 = 265;
    const r2 = i % 10 === 0 ? 285 : i % 5 === 0 ? 280 : 275;
    const x1 = 400 + r1 * Math.cos(angle);
    const y1 = 400 + r1 * Math.sin(angle);
    const x2 = 400 + r2 * Math.cos(angle);
    const y2 = 400 + r2 * Math.sin(angle);

    ticks.push({
      id: `tick-${i}`,
      x1,
      y1,
      x2,
      y2,
      stroke: i % 10 === 0 ? '#00f5ff' : i % 5 === 0 ? '#5a00ff' : '#3a1a5a',
      strokeWidth: i % 10 === 0 ? '2.5' : i % 5 === 0 ? '1.5' : '1',
      opacity: i % 10 === 0 ? '0.9' : i % 5 === 0 ? '0.6' : '0.3',
    });
  }

  return (
    <g className="tick-marks">
      {ticks.map((tick) => (
        <line
          key={tick.id}
          x1={tick.x1}
          y1={tick.y1}
          x2={tick.x2}
          y2={tick.y2}
          stroke={tick.stroke}
          strokeWidth={tick.strokeWidth}
          opacity={tick.opacity}
        />
      ))}
    </g>
  );
};

const ConnectionArcs = () => (
  <g className="connection-arcs">
    <path
      d="M 180,220 Q 400,180 620,220"
      fill="none"
      stroke="url(#cyanGlow)"
      strokeWidth="2.5"
      opacity="0.7"
      filter="url(#glow-cyan)"
    />
    <path
      d="M 180,580 Q 400,620 620,580"
      fill="none"
      stroke="url(#cyanGlow)"
      strokeWidth="2.5"
      opacity="0.7"
      filter="url(#glow-cyan)"
    />
    <path
      d="M 120,320 Q 110,400 120,480"
      fill="none"
      stroke="url(#cyanGlow)"
      strokeWidth="2"
      opacity="0.6"
      filter="url(#glow-cyan)"
    />
    <path
      d="M 680,320 Q 690,400 680,480"
      fill="none"
      stroke="url(#cyanGlow)"
      strokeWidth="2"
      opacity="0.6"
      filter="url(#glow-cyan)"
    />
  </g>
);

const GlowingNodes = () => {
  const nodePositions = [
    { x: 300, y: 140 },
    { x: 400, y: 125 },
    { x: 500, y: 140 },
    { x: 620, y: 220 },
    { x: 670, y: 320 },
    { x: 680, y: 400 },
    { x: 670, y: 480 },
    { x: 620, y: 580 },
    { x: 500, y: 660 },
    { x: 400, y: 675 },
    { x: 300, y: 660 },
    { x: 180, y: 580 },
    { x: 130, y: 480 },
    { x: 120, y: 400 },
    { x: 130, y: 320 },
    { x: 180, y: 220 },
  ];

  return (
    <g className="nodes">
      {nodePositions.map((node, i) => (
        <g key={generateNodeId(i)}>
          <circle
            cx={node.x}
            cy={node.y}
            r="8"
            fill="#00f5ff"
            filter="url(#glow-cyan)"
            opacity="0.9"
            className="pulsing-node"
            style={{
              animationDelay: `${i * 0.1}s`,
            }}
          />
          <circle cx={node.x} cy={node.y} r="4" fill="#ffffff" opacity="0.8" />
        </g>
      ))}
    </g>
  );
};

const LevelIndicators = () => {
  const levels = [
    { id: 'level-0', width: 50 },
    { id: 'level-1', width: 65 },
    { id: 'level-2', width: 45 },
    { id: 'level-3', width: 70 },
    { id: 'level-4', width: 55 },
  ];

  return (
    <g className="level-indicators">
      {levels.map((level, i) => (
        <rect
          key={level.id}
          x="270"
          y={480 + i * 12}
          width={level.width}
          height="6"
          fill="#5a00ff"
          opacity="0.6"
          rx="2"
        />
      ))}
    </g>
  );
};

const Title = () => (
  <>
    <text
      x="400"
      y="120"
      fill="#00f5ff"
      fontSize="52"
      fontFamily="'Orbitron', 'Rajdhani', sans-serif"
      fontWeight="700"
      textAnchor="middle"
      letterSpacing="10"
      filter="url(#glow-cyan)"
      className="main-title"
    >
      TWINKU
    </text>
    <text
      x="400"
      y="170"
      fill="#ff00ff"
      fontSize="52"
      fontFamily="'Orbitron', 'Rajdhani', sans-serif"
      fontWeight="700"
      textAnchor="middle"
      letterSpacing="10"
      filter="url(#glow-magenta)"
      className="main-title"
    >
      AI
    </text>
  </>
);

export default SVGLayers;

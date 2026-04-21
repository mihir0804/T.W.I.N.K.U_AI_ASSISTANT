import React, { useEffect, useRef, useCallback } from 'react';

const Waveform = ({ status, audioLevel }) => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  const timeRef = useRef(0);
  const audioDataRef = useRef(new Array(64).fill(0));
  const smoothDataRef = useRef(new Array(64).fill(0));

  const updateAudioData = useCallback(() => {
    if (status === 'speaking') {
      for (let i = 0; i < audioDataRef.current.length; i++) {
        const randomFactor = Math.random() * 0.3 + 0.7;
        audioDataRef.current[i] = audioLevel * randomFactor * 255;
      }
    } else {
      audioDataRef.current = audioDataRef.current.map((val) => val * 0.9);
    }
  }, [status, audioLevel]);

  const smoothData = useCallback(() => {
    for (let i = 0; i < audioDataRef.current.length; i++) {
      smoothDataRef.current[i] =
        smoothDataRef.current[i] * 0.85 + audioDataRef.current[i] * 0.15;
    }
  }, []);

  const drawBlob = useCallback(
    (ctx, centerX, centerY, baseRadius) => {
      const gradient = ctx.createRadialGradient(
        centerX,
        centerY,
        0,
        centerX,
        centerY,
        baseRadius * 1.5
      );
      gradient.addColorStop(0, 'rgba(90, 0, 255, 0.6)');
      gradient.addColorStop(0.5, 'rgba(255, 0, 255, 0.4)');
      gradient.addColorStop(1, 'rgba(0, 245, 255, 0.2)');

      ctx.fillStyle = gradient;
      ctx.strokeStyle = '#ff00ff';
      ctx.lineWidth = 3;

      ctx.beginPath();
      const points = 64;
      for (let i = 0; i <= points; i++) {
        const angle = (i / points) * Math.PI * 2;
        let offset;
        if (status === 'speaking') {
          const dataIndex = Math.floor((i / points) * smoothDataRef.current.length);
          const value = smoothDataRef.current[dataIndex] / 255;
          offset = (value - 0.5) * 40;
        } else if (status === 'listening') {
          offset = Math.sin(timeRef.current * 2 + angle * 2) * 5;
        } else {
          offset = Math.sin(timeRef.current + angle) * 3;
        }

        const radius = baseRadius + offset;
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }

      ctx.closePath();
      ctx.fill();

      ctx.shadowBlur = 20;
      ctx.shadowColor = status === 'speaking' ? '#ff00ff' : '#5a00ff';
      ctx.stroke();
      ctx.shadowBlur = 0;
    },
    [status]
  );

  const drawInnerCircle = useCallback((ctx, centerX, centerY) => {
    const innerGradient = ctx.createRadialGradient(
      centerX,
      centerY,
      0,
      centerX,
      centerY,
      30
    );
    innerGradient.addColorStop(0, 'rgba(255, 0, 255, 0.8)');
    innerGradient.addColorStop(1, 'rgba(90, 0, 255, 0.4)');

    ctx.fillStyle = innerGradient;
    ctx.beginPath();
    ctx.arc(centerX, centerY, 20, 0, Math.PI * 2);
    ctx.fill();
  }, []);

  const drawBlueSegments = useCallback((ctx, centerX, centerY, baseRadius) => {
    if (status !== 'speaking') return;

    ctx.fillStyle = 'rgba(0, 212, 255, 0.6)';

    ctx.beginPath();
    const segment1Start = Math.PI * 0.7;
    const segment1End = Math.PI * 1.1;
    ctx.arc(centerX, centerY, baseRadius * 0.7, segment1Start, segment1End);
    ctx.lineTo(centerX, centerY);
    ctx.closePath();
    ctx.fill();

    ctx.beginPath();
    const segment2Start = Math.PI * 1.8;
    const segment2End = Math.PI * 2.2;
    ctx.arc(centerX, centerY, baseRadius * 0.7, segment2Start, segment2End);
    ctx.lineTo(centerX, centerY);
    ctx.closePath();
    ctx.fill();
  }, [status]);

  const animate = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const baseRadius = 100;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    timeRef.current += 0.02;
    updateAudioData();
    smoothData();

    drawBlob(ctx, centerX, centerY, baseRadius);
    drawInnerCircle(ctx, centerX, centerY);
    drawBlueSegments(ctx, centerX, centerY, baseRadius);

    animationRef.current = requestAnimationFrame(animate);
  }, [updateAudioData, smoothData, drawBlob, drawInnerCircle, drawBlueSegments]);

  useEffect(() => {
    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [animate]);

  return (
    <canvas
      ref={canvasRef}
      width={400}
      height={400}
      className="waveform-canvas"
    />
  );
};

export default Waveform;

export default async function initVisualizer(canvas, setMicOn) {
  const ctx = canvas.getContext("2d");

  canvas.width = 400;
  canvas.height = 400;

  const cx = 200;
  const cy = 200;
  const baseRadius = 80; // Inner dark circle radius

  let previousData = [];

  const analyser = new (window.AudioContext || window.webkitAudioContext)().createAnalyser();
  analyser.fftSize = 256;

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === "suspended") await audioCtx.resume();
    const source = audioCtx.createMediaStreamSource(stream);
    source.connect(analyser);
    setMicOn(true);
  } catch {
    setMicOn(false);
  }

  const bufferLength = analyser.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);

  function draw() {
    requestAnimationFrame(draw);
    analyser.getByteFrequencyData(dataArray);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    let avg = dataArray.reduce((a, b) => a + b) / bufferLength;

    ctx.beginPath();
    
    // 1. Draw inner boundary (Perfect Circle)
    for (let i = 0; i <= bufferLength; i++) {
      let angle = (i / bufferLength) * Math.PI * 2;
      let x = cx + baseRadius * Math.cos(angle);
      let y = cy + baseRadius * Math.sin(angle);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }

    // 2. Draw outer boundary (Dynamic Waveform, drawn in reverse to close the path)
    for (let i = bufferLength; i >= 0; i--) {
      let index = i === bufferLength ? 0 : i;
      let angle = (index / bufferLength) * Math.PI * 2;

      let prev = previousData[index] || 0;
      let smooth = prev * 0.85 + dataArray[index] * 0.15;
      previousData[index] = smooth;

      let value = smooth / 255;
      let offset = avg < 5 ? Math.sin(Date.now() * 0.002 + index) * 3 : value * 40;
      
      // Add a minimum thickness (8px) so the ring is always visible
      let r = baseRadius + 8 + offset; 

      let x = cx + r * Math.cos(angle);
      let y = cy + r * Math.sin(angle);
      ctx.lineTo(x, y);
    }

    ctx.closePath();

    // Replicate the Pink/Blue gradient from the image
    let grad = ctx.createLinearGradient(100, 100, 300, 300);
    grad.addColorStop(0, "#ff00ff");
    grad.addColorStop(0.5, "#00f5ff");
    grad.addColorStop(1, "#a200ff");

    ctx.fillStyle = grad;

    // Deep glow
    ctx.shadowBlur = 20;
    ctx.shadowColor = "#ff00ff";
    ctx.fill();

    ctx.shadowBlur = 40;
    ctx.globalAlpha = 0.5;
    ctx.fill();
    ctx.globalAlpha = 1;
  }

  draw();
}

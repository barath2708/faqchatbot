import { useEffect, useRef } from "react";

const NODE_COUNT = 70;
const MAX_DIST = 150;

function GraphBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    let w, h, nodes, animId;
    const mouse = { x: -9999, y: -9999 };

    const resize = () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    };

    const initNodes = () => {
      nodes = [];
      for (let i = 0; i < NODE_COUNT; i++) {
        const z = Math.random(); // depth: 0 far, 1 near
        nodes.push({
          x: Math.random() * w,
          y: Math.random() * h,
          z,
          vx: (Math.random() - 0.5) * 0.18 * (0.4 + z),
          vy: (Math.random() - 0.5) * 0.18 * (0.4 + z),
          r: 1.1 + z * 2.2,
          pulse: Math.random() * Math.PI * 2,
        });
      }
    };

    const onMouseMove = (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    };
    const onMouseLeave = () => {
      mouse.x = -9999;
      mouse.y = -9999;
    };

    const step = () => {
      ctx.clearRect(0, 0, w, h);
      const px = (mouse.x - w / 2) * 0.01;
      const py = (mouse.y - h / 2) * 0.01;

      for (const n of nodes) {
        n.x += n.vx;
        n.y += n.vy;
        n.pulse += 0.02;
        if (n.x < -20) n.x = w + 20;
        if (n.x > w + 20) n.x = -20;
        if (n.y < -20) n.y = h + 20;
        if (n.y > h + 20) n.y = -20;
      }

      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const a = nodes[i];
          const b = nodes[j];
          const dx = a.x - b.x;
          const dy = a.y - b.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < MAX_DIST) {
            const alpha = (1 - dist / MAX_DIST) * 0.16 * ((a.z + b.z) / 2 + 0.3);
            ctx.strokeStyle = `rgba(45,212,191,${alpha})`;
            ctx.lineWidth = 0.6;
            ctx.beginPath();
            ctx.moveTo(a.x + px * a.z, a.y + py * a.z);
            ctx.lineTo(b.x + px * b.z, b.y + py * b.z);
            ctx.stroke();
          }
        }
      }

      for (const n of nodes) {
        const glow = 0.5 + Math.sin(n.pulse) * 0.3;
        const alpha = 0.35 + n.z * 0.5;
        ctx.beginPath();
        ctx.arc(n.x + px * n.z, n.y + py * n.z, n.r * (0.85 + glow * 0.3), 0, Math.PI * 2);
        const isOrange = n.z > 0.72;
        ctx.fillStyle = isOrange ? `rgba(255,122,26,${alpha})` : `rgba(45,212,191,${alpha * 0.8})`;
        ctx.fill();
      }

      animId = requestAnimationFrame(step);
    };

    resize();
    initNodes();
    window.addEventListener("resize", resize);
    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseleave", onMouseLeave);
    step();

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", resize);
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseleave", onMouseLeave);
    };
  }, []);

  return (
    <>
      <canvas ref={canvasRef} className="fixed inset-0 w-full h-full z-0" />
      <div
        className="fixed inset-0 z-[1] pointer-events-none"
        style={{
          background:
            "radial-gradient(ellipse 900px 500px at 50% 0%, rgba(255,122,26,0.10), transparent 60%), linear-gradient(180deg, rgba(10,14,18,0.2) 0%, rgba(10,14,18,0.55) 55%, #0a0e12 100%)",
        }}
      />
    </>
  );
}

export default GraphBackground;
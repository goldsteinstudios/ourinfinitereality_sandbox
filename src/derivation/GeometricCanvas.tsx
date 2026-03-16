import { useRef, useEffect, useCallback } from 'react';
import type { GeometricFeature } from '../../types/rsm';

interface GeometricCanvasProps {
  activeStepId: string;
  features: GeometricFeature[];
}

export function GeometricCanvas({ activeStepId, features }: GeometricCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number>(0);
  const timeRef = useRef(0);

  const hasFeature = useCallback(
    (type: string) => features.some((f) => f.type === type),
    [features]
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    const w = rect.width;
    const h = rect.height;

    // Coordinate system: center of canvas, scaled so that range [-0.5, 4.5] maps to visible area
    const scale = Math.min(w, h) / 6;
    const cx = w / 2;
    const cy = h / 2;

    const toScreenX = (x: number) => cx + (x - 2) * scale;
    const toScreenY = (y: number) => cy - (y - 2) * scale;

    function draw() {
      if (!ctx) return;
      timeRef.current += 0.02;
      const t = timeRef.current;

      // Clear
      ctx.clearRect(0, 0, w, h);

      // Background grid (subtle)
      ctx.strokeStyle = 'rgba(255,255,255,0.04)';
      ctx.lineWidth = 0.5;
      for (let i = 0; i <= 4; i++) {
        // Vertical
        ctx.beginPath();
        ctx.moveTo(toScreenX(i), toScreenY(0));
        ctx.lineTo(toScreenX(i), toScreenY(4));
        ctx.stroke();
        // Horizontal
        ctx.beginPath();
        ctx.moveTo(toScreenX(0), toScreenY(i));
        ctx.lineTo(toScreenX(4), toScreenY(i));
        ctx.stroke();
      }

      // Axes
      ctx.strokeStyle = 'rgba(255,255,255,0.15)';
      ctx.lineWidth = 1;
      // x-axis
      ctx.beginPath();
      ctx.moveTo(toScreenX(0), toScreenY(0));
      ctx.lineTo(toScreenX(4.5), toScreenY(0));
      ctx.stroke();
      // y-axis
      ctx.beginPath();
      ctx.moveTo(toScreenX(0), toScreenY(0));
      ctx.lineTo(toScreenX(0), toScreenY(4.5));
      ctx.stroke();

      // Axis labels
      ctx.fillStyle = 'rgba(255,255,255,0.3)';
      ctx.font = '11px monospace';
      ctx.fillText('x', toScreenX(4.3), toScreenY(0) + 15);
      ctx.fillText('y', toScreenX(0) - 15, toScreenY(4.3));

      const showEmpty = hasFeature('empty') && !hasFeature('hyperbola') && !hasFeature('duality');

      // Empty state — just show the void
      if (showEmpty) {
        ctx.fillStyle = 'rgba(255,255,255,0.08)';
        ctx.font = '14px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('P0: indistinguishability', w / 2, h / 2);
        ctx.fillText('(incoherent under the premise)', w / 2, h / 2 + 20);
        ctx.textAlign = 'start';
      }

      // Duality — show two regions
      if (hasFeature('duality') && !hasFeature('hyperbola')) {
        ctx.fillStyle = 'rgba(59, 130, 246, 0.06)';
        ctx.fillRect(toScreenX(2), toScreenY(4.5), toScreenX(4.5) - toScreenX(2), toScreenY(0) - toScreenY(4.5));
        ctx.fillStyle = 'rgba(234, 179, 8, 0.06)';
        ctx.fillRect(toScreenX(0), toScreenY(4.5), toScreenX(2) - toScreenX(0), toScreenY(0) - toScreenY(4.5));
        ctx.fillStyle = 'rgba(59, 130, 246, 0.3)';
        ctx.font = '12px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('x-mode', toScreenX(3), toScreenY(2));
        ctx.fillStyle = 'rgba(234, 179, 8, 0.3)';
        ctx.fillText('y-mode', toScreenX(1), toScreenY(2));
        ctx.textAlign = 'start';
      }

      // Conservation — show xy = 1 annotation
      if (hasFeature('conservation') && !hasFeature('hyperbola')) {
        ctx.fillStyle = 'rgba(52, 211, 153, 0.5)';
        ctx.font = '13px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('xy = 1', w / 2, h / 2 - 10);
        ctx.fillText('(neither mode can vanish)', w / 2, h / 2 + 10);
        ctx.textAlign = 'start';
      }

      // Asymptotes (dashed) — show when gradient or hyperbola present
      if (hasFeature('gradient') || hasFeature('hyperbola') || hasFeature('non_termination')) {
        ctx.strokeStyle = 'rgba(239, 68, 68, 0.25)';
        ctx.lineWidth = 1;
        ctx.setLineDash([4, 4]);
        // x = 0 asymptote (y-axis itself, shown red)
        ctx.beginPath();
        ctx.moveTo(toScreenX(0.01), toScreenY(0));
        ctx.lineTo(toScreenX(0.01), toScreenY(4.5));
        ctx.stroke();
        // y = 0 asymptote (x-axis itself, shown red)
        ctx.beginPath();
        ctx.moveTo(toScreenX(0), toScreenY(0.01));
        ctx.lineTo(toScreenX(4.5), toScreenY(0.01));
        ctx.stroke();
        ctx.setLineDash([]);
      }

      // Non-termination arrows at asymptotes
      if (hasFeature('non_termination')) {
        ctx.fillStyle = 'rgba(239, 68, 68, 0.6)';
        ctx.font = '11px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('u → +∞', toScreenX(4), toScreenY(0.15) + 15);
        ctx.fillText('u → −∞', toScreenX(0.15) - 5, toScreenY(4) - 5);
        // Draw arrows
        ctx.strokeStyle = 'rgba(239, 68, 68, 0.5)';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([3, 3]);
        // Arrow toward x-axis (y→0)
        ctx.beginPath();
        ctx.moveTo(toScreenX(3.5), toScreenY(1 / 3.5));
        ctx.lineTo(toScreenX(4.3), toScreenY(1 / 4.3));
        ctx.stroke();
        // Arrow toward y-axis (x→0)
        ctx.beginPath();
        ctx.moveTo(toScreenX(1 / 3.5), toScreenY(3.5));
        ctx.lineTo(toScreenX(1 / 4.3), toScreenY(4.3));
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.textAlign = 'start';
      }

      // Hyperbola xy = 1
      if (hasFeature('hyperbola') || hasFeature('gradient') || hasFeature('conservation')) {
        ctx.strokeStyle = 'rgba(59, 130, 246, 0.9)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        let first = true;
        for (let xv = 0.22; xv <= 4.5; xv += 0.02) {
          const yv = 1 / xv;
          if (yv > 4.5) continue;
          const sx = toScreenX(xv);
          const sy = toScreenY(yv);
          if (first) {
            ctx.moveTo(sx, sy);
            first = false;
          } else {
            ctx.lineTo(sx, sy);
          }
        }
        ctx.stroke();

        // Equation label
        ctx.fillStyle = 'rgba(59, 130, 246, 0.7)';
        ctx.font = '12px monospace';
        ctx.fillText('xy = 1', toScreenX(2.5), toScreenY(1 / 2.5) - 8);
      }

      // Exponential parameterization markers
      if (hasFeature('exponential')) {
        ctx.fillStyle = 'rgba(168, 85, 247, 0.8)';
        ctx.font = '10px monospace';
        for (let u = -1.5; u <= 1.5; u += 0.5) {
          const xv = Math.exp(u);
          const yv = Math.exp(-u);
          if (xv > 4.5 || yv > 4.5) continue;
          const sx = toScreenX(xv);
          const sy = toScreenY(yv);
          ctx.beginPath();
          ctx.arc(sx, sy, 3, 0, Math.PI * 2);
          ctx.fill();
          if (Math.abs(u) < 0.01) {
            ctx.fillText('u=0', sx + 6, sy - 6);
          } else {
            ctx.fillText(`u=${u > 0 ? '+' : ''}${u.toFixed(1)}`, sx + 6, sy - 4);
          }
        }
      }

      // Lorentz overlay
      if (hasFeature('lorentz')) {
        ctx.strokeStyle = 'rgba(234, 179, 8, 0.6)';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([6, 3]);
        ctx.beginPath();
        let first = true;
        for (let u = -2; u <= 2; u += 0.05) {
          const X = Math.cosh(u);
          const T = Math.sinh(u);
          // Map Lorentz coords: X goes right, T goes up, centered at origin
          const sx = toScreenX(X + 1); // offset to not overlap
          const sy = toScreenY(T + 2);
          if (sx < 0 || sx > w || sy < 0 || sy > h) continue;
          if (first) {
            ctx.moveTo(sx, sy);
            first = false;
          } else {
            ctx.lineTo(sx, sy);
          }
        }
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = 'rgba(234, 179, 8, 0.6)';
        ctx.font = '11px monospace';
        ctx.fillText('X²−T²=1', toScreenX(3), toScreenY(3));
      }

      // Balance line x = y
      if (hasFeature('balance_line') || hasFeature('orthogonality')) {
        ctx.strokeStyle = 'rgba(52, 211, 153, 0.7)';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([5, 3]);
        ctx.beginPath();
        ctx.moveTo(toScreenX(0), toScreenY(0));
        ctx.lineTo(toScreenX(4), toScreenY(4));
        ctx.stroke();
        ctx.setLineDash([]);

        // Label
        ctx.fillStyle = 'rgba(52, 211, 153, 0.7)';
        ctx.font = '12px monospace';
        ctx.fillText('x = y', toScreenX(3.2), toScreenY(3.2) - 8);
      }

      // Orthogonality marker at P = (1,1)
      if (hasFeature('orthogonality')) {
        const px = toScreenX(1);
        const py = toScreenY(1);

        // Point P
        ctx.fillStyle = 'rgba(239, 68, 68, 0.9)';
        ctx.beginPath();
        ctx.arc(px, py, 5, 0, Math.PI * 2);
        ctx.fill();

        // Right angle marker
        const msize = 10;
        ctx.strokeStyle = 'rgba(239, 68, 68, 0.7)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        // Along balance line direction (1,1 normalized)
        const bx = msize * Math.cos(Math.PI / 4);
        const by = -msize * Math.sin(Math.PI / 4);
        // Along hyperbola tangent direction (1,-1 normalized)
        const hx = msize * Math.cos(-Math.PI / 4);
        const hy = -msize * Math.sin(-Math.PI / 4);
        ctx.moveTo(px + bx, py + by);
        ctx.lineTo(px + bx + hx, py + by + hy);
        ctx.lineTo(px + hx, py + hy);
        ctx.stroke();

        // Label
        ctx.fillStyle = 'rgba(239, 68, 68, 0.8)';
        ctx.font = '11px monospace';
        ctx.fillText('P=(1,1)', px + 10, py - 10);
        ctx.font = '10px sans-serif';
        ctx.fillText('⊥', px + 12, py + 3);
      }

      // Circle overlay (bridge between branches)
      if (hasFeature('circle') || hasFeature('two_branch')) {
        ctx.strokeStyle = 'rgba(168, 85, 247, 0.6)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(toScreenX(0), toScreenY(0), scale, 0, Math.PI * 2);
        ctx.stroke();

        ctx.fillStyle = 'rgba(168, 85, 247, 0.5)';
        ctx.font = '11px monospace';
        ctx.fillText('x²+y²=1', toScreenX(0.7), toScreenY(0.7) + 15);
      }

      // Sphere indication (2D projection)
      if (hasFeature('sphere') || hasFeature('circle')) {
        ctx.strokeStyle = 'rgba(168, 85, 247, 0.3)';
        ctx.lineWidth = 1;
        ctx.setLineDash([3, 3]);
        // Draw an ellipse suggesting 3D sphere
        ctx.beginPath();
        ctx.ellipse(toScreenX(0), toScreenY(0), scale, scale * 0.4, 0, 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      // Frame recursion visualization
      if (hasFeature('frame_recursion')) {
        // Nested smaller hyperbola
        ctx.strokeStyle = 'rgba(59, 130, 246, 0.4)';
        ctx.lineWidth = 1;
        const s = 0.5; // scale factor for inner frame
        ctx.beginPath();
        let first = true;
        for (let xv = 0.3; xv <= 3; xv += 0.03) {
          const yv = s / xv;
          if (yv > 3) continue;
          const sx = toScreenX(1 + (xv - 1) * s);
          const sy = toScreenY(1 + (yv - 1) * s);
          if (first) {
            ctx.moveTo(sx, sy);
            first = false;
          } else {
            ctx.lineTo(sx, sy);
          }
        }
        ctx.stroke();

        // Arrow from P to nested frame
        ctx.strokeStyle = 'rgba(52, 211, 153, 0.5)';
        ctx.lineWidth = 1;
        ctx.setLineDash([3, 3]);
        ctx.beginPath();
        ctx.moveTo(toScreenX(1), toScreenY(1));
        ctx.lineTo(toScreenX(1), toScreenY(1.2));
        ctx.stroke();
        ctx.setLineDash([]);

        ctx.fillStyle = 'rgba(52, 211, 153, 0.5)';
        ctx.font = '10px sans-serif';
        ctx.fillText('Rₙ → Rₙ₊₁', toScreenX(1.2), toScreenY(1.3));
      }

      // Oscillation animation
      if (hasFeature('oscillation')) {
        const u = Math.sin(t * 2) * 1.2;
        const xv = Math.exp(u);
        const yv = Math.exp(-u);
        if (xv <= 4.5 && yv <= 4.5) {
          const sx = toScreenX(xv);
          const sy = toScreenY(yv);

          // Glowing dot
          const gradient = ctx.createRadialGradient(sx, sy, 0, sx, sy, 12);
          gradient.addColorStop(0, 'rgba(59, 130, 246, 0.8)');
          gradient.addColorStop(1, 'rgba(59, 130, 246, 0)');
          ctx.fillStyle = gradient;
          ctx.beginPath();
          ctx.arc(sx, sy, 12, 0, Math.PI * 2);
          ctx.fill();

          // Core dot
          ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
          ctx.beginPath();
          ctx.arc(sx, sy, 3, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      animationRef.current = requestAnimationFrame(draw);
    }

    draw();

    return () => {
      cancelAnimationFrame(animationRef.current);
    };
  }, [activeStepId, features, hasFeature]);

  return (
    <canvas
      ref={canvasRef}
      className="w-full h-full rounded-lg bg-gray-900/50"
      style={{ minHeight: 300 }}
    />
  );
}

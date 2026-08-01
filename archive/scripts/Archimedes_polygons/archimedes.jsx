import { useState, useEffect, useRef } from "react";

const COLORS = {
  bg: "#111111",
  circle: "#e0e0e0",
  polygon: "#6ba3d6",
  polygonFill: "rgba(107, 163, 214, 0.08)",
  outer: "#d6856b",
  outerFill: "rgba(214, 133, 107, 0.06)",
  center: "#555555",
  text: "#cccccc",
  textMuted: "#777777",
  textDim: "#555555",
  accent: "#e0e0e0",
  pi: "#8bc48a",
};

function getPolygonPoints(n, radius, cx, cy) {
  const points = [];
  for (let i = 0; i < n; i++) {
    const angle = (2 * Math.PI * i) / n - Math.PI / 2;
    points.push({
      x: cx + radius * Math.cos(angle),
      y: cy + radius * Math.sin(angle),
    });
  }
  return points;
}

function getOuterPolygonPoints(n, radius, cx, cy) {
  const outerRadius = radius / Math.cos(Math.PI / n);
  const points = [];
  for (let i = 0; i < n; i++) {
    const angle = (2 * Math.PI * i) / n - Math.PI / 2;
    points.push({
      x: cx + outerRadius * Math.cos(angle),
      y: cy + outerRadius * Math.sin(angle),
    });
  }
  return points;
}

function polygonPerimeter(n, radius) {
  return 2 * n * radius * Math.sin(Math.PI / n);
}

function outerPolygonPerimeter(n, radius) {
  return 2 * n * radius * Math.tan(Math.PI / n);
}

function pointsToPath(points) {
  return points.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`).join(" ") + " Z";
}

export default function ArchimedesAnimation() {
  const [sides, setSides] = useState(3);
  const [isPlaying, setIsPlaying] = useState(false);
  const [showOuter, setShowOuter] = useState(true);
  const [history, setHistory] = useState([]);
  const timerRef = useRef(null);

  const radius = 140;
  const cx = 200;
  const cy = 200;
  const diameter = 2 * radius;

  const innerPerim = polygonPerimeter(sides, radius);
  const outerPerim = outerPolygonPerimeter(sides, radius);
  const innerRatio = innerPerim / diameter;
  const outerRatio = outerPerim / diameter;

  const innerPoints = getPolygonPoints(sides, radius, cx, cy);
  const outerPoints = getOuterPolygonPoints(sides, radius, cx, cy);

  useEffect(() => {
    if (sides >= 3) {
      setHistory((prev) => {
        const exists = prev.find((h) => h.sides === sides);
        if (exists) return prev;
        return [
          ...prev,
          {
            sides,
            lower: innerRatio,
            upper: outerRatio,
          },
        ].slice(-12);
      });
    }
  }, [sides, innerRatio, outerRatio]);

  useEffect(() => {
    if (isPlaying) {
      timerRef.current = setInterval(() => {
        setSides((prev) => {
          if (prev >= 96) {
            setIsPlaying(false);
            return prev;
          }
          if (prev < 6) return prev + 1;
          if (prev < 12) return prev + 2;
          if (prev < 24) return prev + 4;
          return prev * 2;
        });
      }, 1200);
    }
    return () => clearInterval(timerRef.current);
  }, [isPlaying]);

  const reset = () => {
    setIsPlaying(false);
    setSides(3);
    setHistory([]);
  };

  const piBarWidth = 280;
  const piPosition = ((Math.PI - 2.5) / (4.5 - 2.5)) * piBarWidth;
  const lowerPos = ((innerRatio - 2.5) / (4.5 - 2.5)) * piBarWidth;
  const upperPos = ((outerRatio - 2.5) / (4.5 - 2.5)) * piBarWidth;

  return (
    <div
      style={{
        background: COLORS.bg,
        minHeight: "100vh",
        padding: "32px 16px",
        fontFamily: "'Crimson Text', 'Georgia', serif",
        color: COLORS.text,
      }}
    >
      <div style={{ maxWidth: 520, margin: "0 auto" }}>
        {/* Title */}
        <div style={{ textAlign: "center", marginBottom: 32 }}>
          <h1
            style={{
              fontSize: 28,
              fontWeight: 400,
              letterSpacing: "0.02em",
              marginBottom: 8,
              color: COLORS.accent,
            }}
          >
            Archimedes' Method
          </h1>
          <p style={{ color: COLORS.textMuted, fontSize: 15, fontStyle: "italic" }}>
            Squeezing π between polygons, one side at a time
          </p>
        </div>

        {/* SVG Canvas */}
        <div
          style={{
            background: "#0a0a0a",
            borderRadius: 8,
            padding: 16,
            marginBottom: 24,
            border: "1px solid #222",
          }}
        >
          <svg viewBox="0 0 400 400" style={{ width: "100%", display: "block" }}>
            {/* Center crosshair */}
            <line x1={cx - 6} y1={cy} x2={cx + 6} y2={cy} stroke={COLORS.center} strokeWidth={0.5} />
            <line x1={cx} y1={cy - 6} x2={cx} y2={cy + 6} stroke={COLORS.center} strokeWidth={0.5} />
            <circle cx={cx} cy={cy} r={2} fill="none" stroke={COLORS.center} strokeWidth={1} />

            {/* Outer polygon */}
            {showOuter && (
              <path
                d={pointsToPath(outerPoints)}
                fill={COLORS.outerFill}
                stroke={COLORS.outer}
                strokeWidth={1.2}
                strokeLinejoin="round"
                style={{ transition: "d 0.6s ease-in-out" }}
              />
            )}

            {/* The circle (truth) */}
            <circle
              cx={cx}
              cy={cy}
              r={radius}
              fill="none"
              stroke={COLORS.circle}
              strokeWidth={2}
              strokeDasharray={sides <= 6 ? "none" : "none"}
            />

            {/* Inner polygon */}
            <path
              d={pointsToPath(innerPoints)}
              fill={COLORS.polygonFill}
              stroke={COLORS.polygon}
              strokeWidth={1.5}
              strokeLinejoin="round"
              style={{ transition: "d 0.6s ease-in-out" }}
            />

            {/* Diameter line */}
            <line
              x1={cx - radius}
              y1={cy}
              x2={cx + radius}
              y2={cy}
              stroke={COLORS.textDim}
              strokeWidth={0.8}
              strokeDasharray="4,6"
            />

            {/* Labels */}
            <text x={cx} y={cy + radius + 25} textAnchor="middle" fontSize={13} fill={COLORS.textMuted} fontFamily="Georgia, serif">
              diameter = d
            </text>

            {/* Side count badge */}
            <text x={cx} y={38} textAnchor="middle" fontSize={42} fill={COLORS.accent} fontFamily="Georgia, serif" fontWeight={400}>
              {sides}
            </text>
            <text x={cx} y={55} textAnchor="middle" fontSize={12} fill={COLORS.textDim} fontFamily="Georgia, serif">
              sides
            </text>
          </svg>
        </div>

        {/* Pi squeeze bar */}
        <div
          style={{
            background: "#0a0a0a",
            borderRadius: 8,
            padding: "20px 24px",
            marginBottom: 24,
            border: "1px solid #222",
          }}
        >
          <div style={{ fontSize: 13, color: COLORS.textMuted, marginBottom: 12, textAlign: "center" }}>
            Trapping π between inner and outer perimeters
          </div>

          <div style={{ position: "relative", height: 48, marginBottom: 8 }}>
            {/* Track */}
            <div
              style={{
                position: "absolute",
                top: 22,
                left: 0,
                width: piBarWidth,
                height: 4,
                background: "#222",
                borderRadius: 2,
                margin: "0 auto",
                left: "50%",
                transform: "translateX(-50%)",
              }}
            />

            {/* Squeeze zone */}
            <div
              style={{
                position: "absolute",
                top: 20,
                left: `calc(50% - ${piBarWidth / 2}px + ${Math.min(lowerPos, upperPos)}px)`,
                width: Math.max(2, Math.abs(upperPos - lowerPos)),
                height: 8,
                background: "rgba(139, 196, 138, 0.2)",
                borderRadius: 4,
                transition: "all 0.6s ease-in-out",
              }}
            />

            {/* Pi marker */}
            <div
              style={{
                position: "absolute",
                top: 8,
                left: `calc(50% - ${piBarWidth / 2}px + ${piPosition}px)`,
                transform: "translateX(-50%)",
                textAlign: "center",
              }}
            >
              <div style={{ fontSize: 16, color: COLORS.pi, fontFamily: "Georgia, serif" }}>π</div>
              <div
                style={{
                  width: 2,
                  height: 20,
                  background: COLORS.pi,
                  margin: "0 auto",
                  opacity: 0.6,
                }}
              />
            </div>

            {/* Lower bound marker */}
            <div
              style={{
                position: "absolute",
                top: 16,
                left: `calc(50% - ${piBarWidth / 2}px + ${lowerPos}px)`,
                transform: "translateX(-50%)",
                transition: "left 0.6s ease-in-out",
              }}
            >
              <div
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: COLORS.polygon,
                  margin: "2px auto 0",
                }}
              />
            </div>

            {/* Upper bound marker */}
            {showOuter && (
              <div
                style={{
                  position: "absolute",
                  top: 16,
                  left: `calc(50% - ${piBarWidth / 2}px + ${upperPos}px)`,
                  transform: "translateX(-50%)",
                  transition: "left 0.6s ease-in-out",
                }}
              >
                <div
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: "50%",
                    background: COLORS.outer,
                    margin: "2px auto 0",
                  }}
                />
              </div>
            )}
          </div>

          {/* Numeric bounds */}
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 14, fontFamily: "monospace" }}>
            <span style={{ color: COLORS.polygon }}>{innerRatio.toFixed(6)}</span>
            <span style={{ color: COLORS.pi }}>π = 3.141592...</span>
            <span style={{ color: COLORS.outer }}>{outerRatio.toFixed(6)}</span>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: COLORS.textDim }}>
            <span>inner / d</span>
            <span />
            <span>outer / d</span>
          </div>
        </div>

        {/* Controls */}
        <div style={{ display: "flex", gap: 12, justifyContent: "center", marginBottom: 24 }}>
          <button
            onClick={() => setSides((s) => Math.max(3, s - 1))}
            disabled={sides <= 3 || isPlaying}
            style={{
              background: "transparent",
              border: `1px solid ${sides <= 3 || isPlaying ? "#333" : "#555"}`,
              color: sides <= 3 || isPlaying ? "#333" : COLORS.text,
              borderRadius: 6,
              padding: "8px 16px",
              cursor: sides <= 3 || isPlaying ? "default" : "pointer",
              fontFamily: "Georgia, serif",
              fontSize: 14,
            }}
          >
            − side
          </button>

          <button
            onClick={() => {
              if (sides >= 96) {
                reset();
              } else {
                setIsPlaying(!isPlaying);
              }
            }}
            style={{
              background: isPlaying ? "#333" : "transparent",
              border: `1px solid ${COLORS.textMuted}`,
              color: COLORS.accent,
              borderRadius: 6,
              padding: "8px 24px",
              cursor: "pointer",
              fontFamily: "Georgia, serif",
              fontSize: 14,
              minWidth: 100,
            }}
          >
            {sides >= 96 ? "Reset" : isPlaying ? "Pause" : "Play"}
          </button>

          <button
            onClick={() => setSides((s) => Math.min(96, s + (s < 6 ? 1 : s < 12 ? 2 : s < 24 ? 4 : s)))}
            disabled={sides >= 96 || isPlaying}
            style={{
              background: "transparent",
              border: `1px solid ${sides >= 96 || isPlaying ? "#333" : "#555"}`,
              color: sides >= 96 || isPlaying ? "#333" : COLORS.text,
              borderRadius: 6,
              padding: "8px 16px",
              cursor: sides >= 96 || isPlaying ? "default" : "pointer",
              fontFamily: "Georgia, serif",
              fontSize: 14,
            }}
          >
            + side
          </button>
        </div>

        {/* Toggle outer */}
        <div style={{ textAlign: "center", marginBottom: 28 }}>
          <label
            style={{
              color: COLORS.textMuted,
              fontSize: 13,
              cursor: "pointer",
              userSelect: "none",
            }}
          >
            <input
              type="checkbox"
              checked={showOuter}
              onChange={() => setShowOuter(!showOuter)}
              style={{ marginRight: 8 }}
            />
            Show outer polygon (circumscribed)
          </label>
        </div>

        {/* History table */}
        {history.length > 0 && (
          <div
            style={{
              background: "#0a0a0a",
              borderRadius: 8,
              padding: "16px 20px",
              marginBottom: 28,
              border: "1px solid #222",
            }}
          >
            <div style={{ fontSize: 13, color: COLORS.textMuted, marginBottom: 10 }}>
              The trap tightens:
            </div>
            <div style={{ fontFamily: "monospace", fontSize: 12, lineHeight: 1.8 }}>
              {history.map((h) => (
                <div key={h.sides} style={{ display: "flex", justifyContent: "space-between", opacity: h.sides === sides ? 1 : 0.4 }}>
                  <span style={{ color: COLORS.textMuted, width: 50 }}>{h.sides}-gon</span>
                  <span style={{ color: COLORS.polygon }}>{h.lower.toFixed(6)}</span>
                  <span style={{ color: COLORS.textDim }}>&lt; π &lt;</span>
                  <span style={{ color: COLORS.outer }}>{h.upper.toFixed(6)}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Bottom text */}
        <div
          style={{
            textAlign: "center",
            padding: "0 20px",
            lineHeight: 1.7,
          }}
        >
          <p style={{ color: COLORS.textMuted, fontSize: 15, marginBottom: 16 }}>
            {sides === 3 && "Three sides. The minimum for closure. The gate opens."}
            {sides === 4 && "Four sides. The square. Already closer, but still far from round."}
            {sides === 5 && "Five sides. The polygon begins to curve."}
            {sides === 6 && "Six sides. The hexagon. Inner perimeter crosses 3.0 for the first time."}
            {sides > 6 && sides <= 12 && "More sides. The straight edges mime the curve more closely."}
            {sides > 12 && sides <= 24 && "The polygon is visibly rounding. The bounds squeeze tighter."}
            {sides > 24 && sides < 96 && "From a distance, it looks like a circle. Zoom in — still corners. Still straight edges."}
            {sides >= 96 &&
              "96 sides. Where Archimedes stopped. He had π trapped between 3.1408 and 3.1429. He knew it was there. He knew he'd never reach it. He built 96 bridges and none of them was the river."}
          </p>

          <p style={{ color: COLORS.textDim, fontSize: 13, fontStyle: "italic" }}>
            Each polygon is a name for something that can't be named completely.
            <br />
            Every side added is another digit of precision.
            <br />
            The naming never finishes.
          </p>
        </div>
      </div>
    </div>
  );
}

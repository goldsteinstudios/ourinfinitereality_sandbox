import { useState } from "react";

const PI = Math.PI;

function getData(maxN) {
  const rows = [];
  for (let n = 3; n <= maxN; n++) {
    const inscRatio  = n * Math.sin(PI / n) / PI;   // inscribed perimeter / πd
    const circumRatio = n * Math.tan(PI / n) / PI;  // circumscribed perimeter / πd
    const ratio = inscRatio / circumRatio;           // = cos²(π/n)... actually cos(π/n)
    rows.push({ n, inscRatio, circumRatio, ratio });
  }
  return rows;
}

export default function App() {
  const [maxN, setMaxN] = useState(24);
  const [showInsc,   setShowInsc]   = useState(true);
  const [showCircum, setShowCircum] = useState(true);
  const [showRatio,  setShowRatio]  = useState(true);
  const [hoveredN,   setHoveredN]   = useState(null);

  const data = getData(maxN);

  // Chart dimensions
  const W = 540, H = 320;
  const padL = 52, padR = 20, padT = 20, padB = 48;
  const chartW = W - padL - padR;
  const chartH = H - padT - padB;

  // X: n from 3 to maxN
  const xScale = (n) => padL + ((n - 3) / (maxN - 3)) * chartW;

  // Y: values range roughly 0.6 to 1.1
  const yMin = 0.58, yMax = 1.12;
  const yScale = (v) => padT + chartH - ((v - yMin) / (yMax - yMin)) * chartH;

  // π line at y=1
  const piY = yScale(1);

  // Grid y values
  const yTicks = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1];

  // X ticks
  const xTicks = [3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 96].filter(t => t <= maxN);

  const labeledNs = [3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 96].filter(t => t <= maxN);

  const hData = hoveredN ? data.find(d => d.n === hoveredN) : null;

  return (
    <div style={{
      background: "#faf9f6", minHeight: "100vh",
      fontFamily: "Georgia,'Times New Roman',serif",
      color: "#2a2520", padding: "20px 14px 40px",
    }}>
      <div style={{ textAlign: "center", marginBottom: 16 }}>
        <div style={{ fontSize: 18, fontWeight: 400, letterSpacing: "0.03em" }}>
          Polygon Perimeter Ratios
        </div>
        <div style={{ fontSize: 11, color: "#7a7060", fontStyle: "italic", marginTop: 3 }}>
          inscribed and circumscribed perimeter ÷ circle circumference, as n → ∞
        </div>
      </div>

      {/* Chart */}
      <div style={{ display: "flex", justifyContent: "center", marginBottom: 16 }}>
        <svg viewBox={`0 0 ${W} ${H}`}
          style={{ width: Math.min(W, typeof window !== "undefined" ? window.innerWidth - 28 : W), display: "block" }}>

          {/* Grid lines */}
          {yTicks.map(v => (
            <g key={v}>
              <line x1={padL} y1={yScale(v)} x2={W - padR} y2={yScale(v)}
                stroke="rgba(0,0,0,0.07)" strokeWidth={1} />
              <text x={padL - 6} y={yScale(v) + 4} textAnchor="end"
                fontSize={10} fill="#7a7060" fontFamily="Georgia,serif">
                {v.toFixed(1)}
              </text>
            </g>
          ))}

          {/* π = 1 line (the limit) */}
          <line x1={padL} y1={piY} x2={W - padR} y2={piY}
            stroke="#2a2520" strokeWidth={1.2} strokeDasharray="4,4" opacity={0.5} />
          <text x={W - padR + 2} y={piY + 4} fontSize={11} fill="#2a2520"
            fontFamily="Georgia,serif" fontStyle="italic">π</text>

          {/* X axis */}
          <line x1={padL} y1={padT + chartH} x2={W - padR} y2={padT + chartH}
            stroke="rgba(0,0,0,0.15)" strokeWidth={1} />

          {/* X ticks */}
          {labeledNs.map(t => (
            <g key={t}>
              <line x1={xScale(t)} y1={padT + chartH} x2={xScale(t)} y2={padT + chartH + 5}
                stroke="rgba(0,0,0,0.2)" strokeWidth={1} />
              <text x={xScale(t)} y={padT + chartH + 17} textAnchor="middle"
                fontSize={9.5} fill="#7a7060" fontFamily="Georgia,serif">{t}</text>
            </g>
          ))}

          {/* Axis labels */}
          <text x={padL + chartW / 2} y={H - 4} textAnchor="middle"
            fontSize={11} fill="#7a7060" fontFamily="Georgia,serif" fontStyle="italic">
            number of sides (n)
          </text>
          <text x={14} y={padT + chartH / 2} textAnchor="middle"
            fontSize={11} fill="#7a7060" fontFamily="Georgia,serif" fontStyle="italic"
            transform={`rotate(-90, 14, ${padT + chartH / 2})`}>
            ratio to πd
          </text>

          {/* Circumscribed line */}
          {showCircum && (
            <polyline
              points={data.map(d => `${xScale(d.n)},${yScale(d.circumRatio)}`).join(" ")}
              fill="none" stroke="#cc2233" strokeWidth={1.8} />
          )}

          {/* Inscribed line */}
          {showInsc && (
            <polyline
              points={data.map(d => `${xScale(d.n)},${yScale(d.inscRatio)}`).join(" ")}
              fill="none" stroke="#2255cc" strokeWidth={1.8} />
          )}

          {/* Ratio line (insc/circum) */}
          {showRatio && (
            <polyline
              points={data.map(d => `${xScale(d.n)},${yScale(d.ratio)}`).join(" ")}
              fill="none" stroke="#888" strokeWidth={1.2} strokeDasharray="3,3" />
          )}

          {/* Shaded convergence region */}
          {showInsc && showCircum && (
            <polygon
              points={[
                ...data.map(d => `${xScale(d.n)},${yScale(d.circumRatio)}`),
                ...[...data].reverse().map(d => `${xScale(d.n)},${yScale(d.inscRatio)}`),
              ].join(" ")}
              fill="rgba(150,150,200,0.08)" stroke="none" />
          )}

          {/* Dots on data points — all */}
          {showInsc && data.map(d => (
            <circle key={`i${d.n}`} cx={xScale(d.n)} cy={yScale(d.inscRatio)} r={hoveredN===d.n?5:3}
              fill="#2255cc" opacity={hoveredN&&hoveredN!==d.n?0.3:1}
              style={{cursor:"pointer"}}
              onMouseEnter={()=>setHoveredN(d.n)} onMouseLeave={()=>setHoveredN(null)} />
          ))}
          {showCircum && data.map(d => (
            <circle key={`c${d.n}`} cx={xScale(d.n)} cy={yScale(d.circumRatio)} r={hoveredN===d.n?5:3}
              fill="#cc2233" opacity={hoveredN&&hoveredN!==d.n?0.3:1}
              style={{cursor:"pointer"}}
              onMouseEnter={()=>setHoveredN(d.n)} onMouseLeave={()=>setHoveredN(null)} />
          ))}
          {showRatio && data.map(d => (
            <circle key={`r${d.n}`} cx={xScale(d.n)} cy={yScale(d.ratio)} r={hoveredN===d.n?4:2}
              fill="#888" opacity={hoveredN&&hoveredN!==d.n?0.2:0.7}
              style={{cursor:"pointer"}}
              onMouseEnter={()=>setHoveredN(d.n)} onMouseLeave={()=>setHoveredN(null)} />
          ))}

          {/* Hover tooltip */}
          {hData && (() => {
            const tx = xScale(hData.n);
            const ty = yScale(hData.inscRatio) - 52;
            const clampedX = Math.min(Math.max(tx, padL + 60), W - padR - 60);
            return (
              <g>
                {/* Vertical guide */}
                <line x1={tx} y1={padT} x2={tx} y2={padT+chartH}
                  stroke="rgba(0,0,0,0.12)" strokeWidth={1} strokeDasharray="2,3"/>
                {/* Box */}
                <rect x={clampedX-58} y={Math.max(ty, padT)} width={116} height={68}
                  rx={4} fill="white" stroke="rgba(0,0,0,0.12)" strokeWidth={1}/>
                <text x={clampedX} y={Math.max(ty, padT)+15} textAnchor="middle"
                  fontSize={11} fontWeight="bold" fill="#2a2520" fontFamily="Georgia,serif">
                  n = {hData.n}
                </text>
                <text x={clampedX} y={Math.max(ty, padT)+30} textAnchor="middle"
                  fontSize={10} fill="#2255cc" fontFamily="monospace">
                  insc: {hData.inscRatio.toFixed(6)}
                </text>
                <text x={clampedX} y={Math.max(ty, padT)+44} textAnchor="middle"
                  fontSize={10} fill="#cc2233" fontFamily="monospace">
                  circ: {hData.circumRatio.toFixed(6)}
                </text>
                <text x={clampedX} y={Math.max(ty, padT)+58} textAnchor="middle"
                  fontSize={10} fill="#888" fontFamily="monospace">
                  ratio: {hData.ratio.toFixed(6)}
                </text>
              </g>
            );
          })()}

          {/* Special label: Archimedes n=96 */}
          {maxN >= 96 && (() => {
            const d = data.find(x => x.n === 96);
            if (!d) return null;
            return (
              <text x={xScale(96)} y={yScale(d.inscRatio) - 8}
                textAnchor="middle" fontSize={9} fill="#2255cc" fontFamily="Georgia,serif"
                fontStyle="italic">
                Archimedes
              </text>
            );
          })()}
        </svg>
      </div>

      {/* Controls row */}
      <div style={{ display: "flex", gap: 20, justifyContent: "center", flexWrap: "wrap", marginBottom: 14 }}>
        {[
          { label: "Inscribed (lower bound)", checked: showInsc,   set: setShowInsc,   color: "#2255cc" },
          { label: "Circumscribed (upper bound)", checked: showCircum, set: setShowCircum, color: "#cc2233" },
          { label: "Insc/Circum ratio", checked: showRatio,  set: setShowRatio,  color: "#888" },
        ].map(({ label, checked, set, color }) => (
          <label key={label} style={{ display: "flex", alignItems: "center", gap: 7, cursor: "pointer", userSelect: "none" }}
            onClick={() => set(v => !v)}>
            <div style={{
              width: 13, height: 13, borderRadius: 2, flexShrink: 0,
              border: `1.5px solid ${checked ? color : "#ccc"}`,
              background: checked ? color + "33" : "transparent",
              display: "flex", alignItems: "center", justifyContent: "center",
            }}>
              {checked && <div style={{ width: 5, height: 5, borderRadius: 1, background: color }} />}
            </div>
            <span style={{ fontSize: 12, fontFamily: "Georgia,serif", color: checked ? "#2a2520" : "#c0b0a0" }}>{label}</span>
          </label>
        ))}
      </div>

      {/* Max N slider */}
      <div style={{ display: "flex", alignItems: "center", gap: 12, justifyContent: "center", marginBottom: 20 }}>
        <span style={{ fontSize: 11, color: "#7a7060", fontFamily: "Georgia,serif" }}>n up to:</span>
        <input type="range" min={6} max={96} step={1} value={maxN}
          onChange={e => setMaxN(parseInt(e.target.value))}
          style={{ width: 180 }} />
        <span style={{ fontSize: 13, color: "#2a2520", fontFamily: "monospace", minWidth: 28 }}>{maxN}</span>
      </div>

      {/* Key values table */}
      <div style={{ display: "flex", justifyContent: "center" }}>
        <div style={{
          background: "#fff", border: "1px solid #e0d8cc", borderRadius: 4,
          padding: "12px 18px", maxWidth: 520, width: "100%",
        }}>
          <div style={{ fontSize: 10, color: "#c0b0a0", letterSpacing: "0.09em", textTransform: "uppercase", marginBottom: 8 }}>
            Key values
          </div>
          <table style={{ width: "100%", borderCollapse: "collapse", fontFamily: "monospace", fontSize: 11 }}>
            <thead>
              <tr style={{ borderBottom: "1px solid #e0d8cc" }}>
                {["n", "inscribed/πd", "circumscribed/πd", "ratio", "gap"].map(h => (
                  <td key={h} style={{ padding: "3px 8px", color: "#7a7060", fontFamily: "Georgia,serif", fontSize: 10 }}>{h}</td>
                ))}
              </tr>
            </thead>
            <tbody>
              {[3,4,5,6,8,10,12,16,24,48,96].filter(n=>n<=maxN).map(n => {
                const d = data.find(x => x.n === n);
                if (!d) return null;
                const gap = d.circumRatio - d.inscRatio;
                return (
                  <tr key={n} style={{ borderBottom: "1px solid #f0ece4" }}
                    onMouseEnter={()=>setHoveredN(n)} onMouseLeave={()=>setHoveredN(null)}>
                    <td style={{ padding: "4px 8px", color: "#2a2520", fontWeight: n===hoveredN?"bold":"normal" }}>{n}</td>
                    <td style={{ padding: "4px 8px", color: "#2255cc" }}>{d.inscRatio.toFixed(6)}</td>
                    <td style={{ padding: "4px 8px", color: "#cc2233" }}>{d.circumRatio.toFixed(6)}</td>
                    <td style={{ padding: "4px 8px", color: "#888" }}>{d.ratio.toFixed(6)}</td>
                    <td style={{ padding: "4px 8px", color: "#7a7060" }}>{gap.toFixed(6)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <div style={{ fontSize: 10, color: "#c0b0a0", fontStyle: "italic", marginTop: 8 }}>
            n=96: Archimedes' stopping point. Gap = {(() => { const d = data.find(x=>x.n===96); return d ? (d.circumRatio - d.inscRatio).toFixed(6) : "—"; })()}
          </div>
        </div>
      </div>

      <div style={{ maxWidth: 480, margin: "16px auto 0", textAlign: "center", fontSize: 11, color: "#c0b0a0", fontStyle: "italic", lineHeight: 1.7 }}>
        Both curves converge on 1 (= π/π) from below and above.
        The gap between them is the Archimedean squeeze — always positive, never zero, approaching zero without arriving.
      </div>
    </div>
  );
}

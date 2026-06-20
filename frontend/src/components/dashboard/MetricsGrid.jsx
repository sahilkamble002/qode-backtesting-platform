function fmt(value) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(value ?? 0);
}
function pct(value) { return `${(value ?? 0).toFixed(2)}%`; }

const METRICS = [
  { key: "initial_capital",      label: "Initial Capital",  fmt, signed: false },
  { key: "final_capital",        label: "Final Capital",    fmt, signed: false },
  { key: "total_return_pct",     label: "Total Return",     fmt: pct, signed: true },
  { key: "cagr_pct",             label: "CAGR",             fmt: pct, signed: true },
  { key: "max_drawdown_pct",     label: "Max Drawdown",     fmt: pct, signed: true },
  { key: "volatility_pct",       label: "Volatility",       fmt: pct, signed: false },
  { key: "sharpe_ratio",         label: "Sharpe Ratio",     fmt: v => (v ?? 0).toFixed(2), signed: true },
  { key: "number_of_rebalances", label: "Rebalances",       fmt: v => v ?? 0, signed: false },
];

export function MetricsGrid({ metrics }) {
  if (!metrics) return null;
  return (
    <div className="panel" style={{ overflow: "hidden" }}>
      <div style={{ padding: "12px 20px", borderBottom: "1px solid var(--color-border)" }}>
        <span className="sub-label">Performance Snapshot</span>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)" }}>
        {METRICS.map((m, i) => {
          const val = metrics[m.key];
          const color = !m.signed ? "var(--color-text)"
            : val < 0 ? "var(--color-down)"
            : "var(--color-up)";
          return (
            <div
              key={m.key}
              style={{
                padding: "18px 20px",
                borderRight: (i + 1) % 4 !== 0 ? "1px solid var(--color-border)" : "none",
                borderBottom: i < 4 ? "1px solid var(--color-border)" : "none",
              }}
            >
              <div style={{ fontSize: 11, color: "var(--color-sub)", marginBottom: 8, letterSpacing: "0.01em" }}>{m.label}</div>
              <div className="mono" style={{ fontSize: 17, fontWeight: 600, color }}>{m.fmt(val)}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

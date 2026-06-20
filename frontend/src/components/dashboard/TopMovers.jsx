function fmt(v) {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(v ?? 0);
}
function pct(v) { return `${((v ?? 0) * 100).toFixed(2)}%`; }

function MoverList({ title, records, isWinner }) {
  return (
    <div className="panel" style={{ flex: 1 }}>
      <div style={{ padding: "12px 20px", borderBottom: "1px solid var(--color-border)", display: "flex", alignItems: "center", gap: 8 }}>
        <span style={{ width: 6, height: 6, borderRadius: "50%", background: isWinner ? "var(--color-up)" : "var(--color-down)", flexShrink: 0 }} />
        <span className="sub-label">{title}</span>
      </div>
      <div>
        {records.map((r, i) => (
          <div key={r.symbol} style={{
            display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12,
            padding: "12px 20px",
            borderBottom: i < records.length - 1 ? "1px solid var(--color-border)" : "none",
          }}>
            <div>
              <div className="mono" style={{ fontSize: 13, fontWeight: 600, color: "var(--color-text)" }}>{r.symbol}</div>
              <div style={{ fontSize: 11, color: "var(--color-sub)", marginTop: 2 }}>×{r.times_selected} selected</div>
            </div>
            <div style={{ textAlign: "right" }}>
              <div className="mono" style={{ fontSize: 13, fontWeight: 600, color: r.total_profit_loss < 0 ? "var(--color-down)" : "var(--color-up)" }}>
                {fmt(r.total_profit_loss)}
              </div>
              <div className="mono" style={{ fontSize: 11, color: "var(--color-sub)", marginTop: 2 }}>{pct(r.average_return_pct)}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function TopMovers({ winners, losers }) {
  if (!winners?.length && !losers?.length) return null;
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
      <MoverList title="Top Winners" records={winners ?? []} isWinner />
      <MoverList title="Top Losers" records={losers ?? []} isWinner={false} />
    </div>
  );
}

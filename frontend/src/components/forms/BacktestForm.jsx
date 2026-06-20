const REBALANCE = [
  { label: "Monthly", value: "monthly" },
  { label: "Quarterly", value: "quarterly" },
  { label: "Yearly", value: "yearly" },
];
const WEIGHTING = [
  { label: "Equal Weight", value: "equal" },
  { label: "Market Cap", value: "market_cap" },
  { label: "Metric Weight", value: "metric" },
];
const METRICS = [
  { label: "ROE", value: "roe" },
  { label: "PE", value: "pe" },
  { label: "Market Cap", value: "market_cap" },
  { label: "ROCE", value: "roce" },
  { label: "PAT", value: "pat" },
  { label: "Debt/EQ", value: "debt_to_equity" },
  { label: "Curr. Ratio", value: "current_ratio" },
];

function Field({ label, name, type = "text", value, onChange, min, max, step, placeholder, error }) {
  return (
    <div>
      <label className="f-label" htmlFor={name}>{label}</label>
      <input
        id={name} name={name} type={type}
        value={value} onChange={onChange}
        min={min} max={max} step={step} placeholder={placeholder}
        className={`f-input${error ? " err" : ""}`}
      />
      {error && <div style={{ fontSize: 11, color: "var(--color-down)", marginTop: 4 }}>{error}</div>}
    </div>
  );
}

function Select({ label, name, value, onChange, options }) {
  return (
    <div>
      <label className="f-label" htmlFor={name}>{label}</label>
      <select id={name} name={name} value={value} onChange={onChange} className="f-input" style={{ cursor: "pointer" }}>
        {options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
      </select>
    </div>
  );
}

function Group({ title, children, cols = 2 }) {
  return (
    <div className="panel" style={{ marginBottom: 16 }}>
      <div style={{
        padding: "12px 20px", borderBottom: "1px solid var(--color-border)",
        display: "flex", alignItems: "center", gap: 8,
      }}>
        <span className="sub-label">{title}</span>
      </div>
      <div style={{ padding: "18px 20px", display: "grid", gridTemplateColumns: `repeat(${cols}, 1fr)`, gap: 14 }}>
        {children}
      </div>
    </div>
  );
}

export function BacktestForm({ values, errors, onChange, onMetricToggle, onSubmit, onReset, isSubmitting, formMessage }) {
  return (
    <form onSubmit={onSubmit}>
      <Group title="Date Range & Capital" cols={4}>
        <Field label="Start Date" name="start_date" type="date" value={values.start_date} onChange={onChange} error={errors.start_date} />
        <Field label="End Date" name="end_date" type="date" value={values.end_date} onChange={onChange} error={errors.end_date} />
        <Field label="Initial Capital (₹)" name="initial_capital" type="number" min="1" step="1" value={values.initial_capital} onChange={onChange} error={errors.initial_capital} />
        <Field label="Portfolio Size" name="portfolio_size" type="number" min="1" max="50" step="1" value={values.portfolio_size} onChange={onChange} error={errors.portfolio_size} />
      </Group>

      <Group title="Allocation & Rebalancing" cols={2}>
        <Select label="Rebalance Frequency" name="rebalance_frequency" value={values.rebalance_frequency} onChange={onChange} options={REBALANCE} />
        <Select label="Weighting Method" name="weighting_method" value={values.weighting_method} onChange={onChange} options={WEIGHTING} />
      </Group>

      <Group title="Stock Filters — Optional" cols={4}>
        <Field label="Min ROE" name="min_roe" type="number" step="0.01" value={values.min_roe} onChange={onChange} placeholder="—" error={errors.min_roe} />
        <Field label="Max PE" name="max_pe" type="number" step="0.01" value={values.max_pe} onChange={onChange} placeholder="—" error={errors.max_pe} />
        <Field label="Min Mkt Cap" name="min_market_cap" type="number" step="1" value={values.min_market_cap} onChange={onChange} placeholder="—" error={errors.min_market_cap} />
        <Field label="Max Mkt Cap" name="max_market_cap" type="number" step="1" value={values.max_market_cap} onChange={onChange} placeholder="—" error={errors.max_market_cap} />
      </Group>

      <div className="panel" style={{ marginBottom: 20 }}>
        <div style={{ padding: "12px 20px", borderBottom: "1px solid var(--color-border)" }}>
          <span className="sub-label">Ranking Strategy</span>
        </div>
        <div style={{ padding: "18px 20px" }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 18 }}>
            <Select label="Primary Metric" name="ranking_metric" value={values.ranking_metric} onChange={onChange} options={METRICS} />
            <div>
              <label className="f-label">Direction</label>
              <label style={{
                display: "flex", alignItems: "center", gap: 10,
                background: "var(--color-raised)", border: "1px solid var(--color-border2)",
                borderRadius: 5, padding: "9px 12px", cursor: "pointer",
                fontSize: 13, color: "var(--color-text)",
              }}>
                <input type="checkbox" name="ranking_ascending" checked={values.ranking_ascending} onChange={onChange} />
                {values.ranking_ascending ? "Ascending (low → high)" : "Descending (high → low)"}
              </label>
            </div>
          </div>

          <div style={{ marginBottom: 10 }}>
            <span className="f-label" style={{ marginBottom: 8, display: "block" }}>Composite Metrics — average rank across selected</span>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
              {METRICS.map(m => {
                const on = values.ranking_metrics.includes(m.value);
                return (
                  <button
                    key={m.value}
                    type="button"
                    onClick={() => onMetricToggle(m.value)}
                    style={{
                      padding: "5px 12px",
                      borderRadius: 4,
                      fontSize: 12,
                      fontFamily: "var(--font-mono)",
                      cursor: "pointer",
                      border: on ? "1px solid var(--color-gold)" : "1px solid var(--color-border2)",
                      background: on ? "var(--color-gold-dim)" : "var(--color-raised)",
                      color: on ? "var(--color-gold)" : "var(--color-sub)",
                      transition: "all 0.12s",
                    }}
                  >
                    {m.label}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <button className="btn-run" type="submit" disabled={isSubmitting}>
          {isSubmitting
            ? <span style={{ display: "flex", alignItems: "center", gap: 7 }}>
                <svg style={{ animation: "spin 0.8s linear infinite" }} width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4"/>
                </svg>
                Running…
              </span>
            : "Run Backtest"
          }
        </button>
        <button className="btn-outline" type="button" onClick={onReset}>Reset</button>
        {formMessage && (
          <span style={{ fontSize: 12, color: "var(--color-sub)", fontFamily: "var(--font-mono)" }}>
            {formMessage}
          </span>
        )}
      </div>

      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </form>
  );
}

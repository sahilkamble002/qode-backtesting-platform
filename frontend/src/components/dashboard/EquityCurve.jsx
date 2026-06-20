import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function formatCurrency(value) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value ?? 0);
}

function formatPercent(value) {
  return `${(value ?? 0).toFixed(2)}%`;
}

const tickStyle = { fill: "#8a909a", fontFamily: "IBM Plex Mono, monospace", fontSize: 11 };

const tooltipStyle = {
  background: "#171b20",
  border: "1px solid #262b32",
  borderRadius: "6px",
  fontFamily: "IBM Plex Mono, monospace",
  fontSize: 12,
};

export function EquityCurve({ periods, drawdowns }) {
  if (!periods?.length) {
    return null;
  }

  return (
    <section className="grid gap-6 xl:grid-cols-2">
      <article className="ledger-panel panel-padding">
        <div className="mb-6">
          <p className="eyebrow">Portfolio Trend</p>
          <h2 className="section-heading">Equity Curve</h2>
          <p className="mt-3 text-sm leading-6 text-mute">
            A true line chart of portfolio capital across rebalance dates.
          </p>
        </div>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={periods} margin={{ left: 4, right: 12 }}>
              <CartesianGrid stroke="#1b1f25" vertical={false} />
              <XAxis dataKey="rebalance_date" stroke="#262b32" tick={tickStyle} tickLine={false} />
              <YAxis stroke="#262b32" tick={tickStyle} tickLine={false} tickFormatter={formatCurrency} width={64} />
              <Tooltip contentStyle={tooltipStyle} labelStyle={{ color: "#edeef0" }} formatter={(value) => [formatCurrency(value), "Capital"]} />
              <Line type="monotone" dataKey="capital_end" stroke="#b8863b" strokeWidth={2} dot={{ r: 2.5, fill: "#b8863b", strokeWidth: 0 }} activeDot={{ r: 4 }} name="Capital End" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </article>

      <article className="ledger-panel panel-padding">
        <div className="mb-6">
          <p className="eyebrow">Risk View</p>
          <h2 className="section-heading">Drawdown Curve</h2>
          <p className="mt-3 text-sm leading-6 text-mute">
            Period drawdown from the rolling capital peak for fast downside inspection.
          </p>
        </div>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={drawdowns} margin={{ left: 4, right: 12 }}>
              <CartesianGrid stroke="#1b1f25" vertical={false} />
              <XAxis dataKey="rebalance_date" stroke="#262b32" tick={tickStyle} tickLine={false} />
              <YAxis stroke="#262b32" tick={tickStyle} tickLine={false} tickFormatter={formatPercent} width={56} />
              <Tooltip contentStyle={tooltipStyle} labelStyle={{ color: "#edeef0" }} formatter={(value) => [formatPercent(value), "Drawdown"]} />
              <Line type="monotone" dataKey="drawdown_pct" stroke="#c06b5e" strokeWidth={2} dot={{ r: 2.5, fill: "#c06b5e", strokeWidth: 0 }} activeDot={{ r: 4 }} name="Drawdown %" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </article>
    </section>
  );
}

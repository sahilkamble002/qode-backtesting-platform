function formatCurrency(value) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value ?? 0);
}

function formatPercent(value) {
  return `${(value ?? 0).toFixed(2)}%`;
}

const headers = ["Rebalance", "Period", "Capital Start", "Capital End", "Return", "Drawdown", "Positions"];

export function RebalanceSummary({ periods }) {
  if (!periods?.length) {
    return null;
  }

  return (
    <section className="ledger-panel panel-padding">
      <div className="mb-6 grid gap-4 lg:grid-cols-[minmax(0,1fr)_320px]">
        <div>
          <p className="eyebrow">Rebalance View</p>
          <h2 className="section-heading">Capital Progression</h2>
        </div>
        <p className="text-sm leading-6 text-mute">
          Period-wise summary showing how capital changed across rebalances and
          how many positions were carried in each cycle.
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr>
              {headers.map((label) => (
                <th
                  className="border-b border-line px-3 py-3 font-mono text-[11px] font-medium uppercase tracking-[0.14em] text-mute"
                  key={label}
                >
                  {label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {periods.map((period) => {
              const returnPct = (period.period_return ?? 0) * 100;
              const drawdownPct = (period.drawdown ?? 0) * 100;
              return (
                <tr className="hover:bg-panel-raised" key={period.rebalance_date}>
                  <td className="num border-b border-line-soft px-3 py-3.5 text-paper">{period.rebalance_date}</td>
                  <td className="num border-b border-line-soft px-3 py-3.5 text-mute">
                    {period.period_start} &rarr; {period.period_end}
                  </td>
                  <td className="num border-b border-line-soft px-3 py-3.5 text-paper">{formatCurrency(period.capital_start)}</td>
                  <td className="num border-b border-line-soft px-3 py-3.5 text-paper">{formatCurrency(period.capital_end)}</td>
                  <td className={`num border-b border-line-soft px-3 py-3.5 ${returnPct < 0 ? "value-negative" : "value-positive"}`}>
                    {formatPercent(returnPct)}
                  </td>
                  <td className={`num border-b border-line-soft px-3 py-3.5 ${drawdownPct < 0 ? "value-negative" : "text-mute"}`}>
                    {formatPercent(drawdownPct)}
                  </td>
                  <td className="num border-b border-line-soft px-3 py-3.5 text-mute">{period.positions}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}

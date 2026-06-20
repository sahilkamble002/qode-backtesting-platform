function formatCurrency(value) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value ?? 0);
}

function formatPercent(value) {
  return `${((value ?? 0) * 100).toFixed(2)}%`;
}

const headers = ["Symbol", "Report Date", "Rebalance", "Entry", "Exit", "Weight", "Allocation", "P&L", "Return"];

export function PositionsTable({ records }) {
  if (!records?.length) {
    return null;
  }

  return (
    <section className="ledger-panel panel-padding">
      <div className="mb-6 grid gap-4 lg:grid-cols-[minmax(0,1fr)_320px]">
        <div>
          <p className="eyebrow">Position Details</p>
          <h2 className="section-heading">Selected Stocks</h2>
        </div>
        <p className="text-sm leading-6 text-mute">
          Detailed entries from the backtest output including weights,
          allocation, and realized profit per holding.
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-[980px] text-left text-sm">
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
            {records.map((record, index) => {
              const pnl = record.profit_loss ?? 0;
              const returnPct = record.return_pct ?? 0;
              return (
                <tr className="hover:bg-panel-raised" key={`${record.symbol}-${record.rebalance_date}-${index}`}>
                  <td className="border-b border-line-soft px-3 py-3.5 font-medium text-paper">{record.symbol}</td>
                  <td className="num border-b border-line-soft px-3 py-3.5 text-mute">{record.report_date ?? "N/A"}</td>
                  <td className="num border-b border-line-soft px-3 py-3.5 text-mute">{record.rebalance_date}</td>
                  <td className="num border-b border-line-soft px-3 py-3.5 text-paper">
                    {record.entry_date}
                    <br />
                    <span className="text-xs text-mute">{formatCurrency(record.entry_close)}</span>
                  </td>
                  <td className="num border-b border-line-soft px-3 py-3.5 text-paper">
                    {record.exit_date}
                    <br />
                    <span className="text-xs text-mute">{formatCurrency(record.exit_close)}</span>
                  </td>
                  <td className="num border-b border-line-soft px-3 py-3.5 text-paper">{formatPercent(record.weight)}</td>
                  <td className="num border-b border-line-soft px-3 py-3.5 text-paper">{formatCurrency(record.allocation)}</td>
                  <td className={`num border-b border-line-soft px-3 py-3.5 ${pnl < 0 ? "value-negative" : "value-positive"}`}>
                    {formatCurrency(pnl)}
                  </td>
                  <td className={`num border-b border-line-soft px-3 py-3.5 ${returnPct < 0 ? "value-negative" : "value-positive"}`}>
                    {formatPercent(returnPct)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}

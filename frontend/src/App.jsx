import { useEffect, useState } from "react";
import * as XLSX from "xlsx";

import { EmptyState } from "./components/dashboard/EmptyState";
import { EquityCurve } from "./components/dashboard/EquityCurve";
import { MetricsGrid } from "./components/dashboard/MetricsGrid";
import { PositionsTable } from "./components/dashboard/PositionsTable";
import { RebalanceSummary } from "./components/dashboard/RebalanceSummary";
import { TopMovers } from "./components/dashboard/TopMovers";
import { BacktestForm } from "./components/forms/BacktestForm";
import { AppShell } from "./components/layout/AppShell";
import { fetchHealth, runBacktest } from "./lib/api";
import { backtestDefaults } from "./lib/backtestDefaults";

function formatCurrency(value) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency", currency: "INR", maximumFractionDigits: 0,
  }).format(value ?? 0);
}

function validateForm(values) {
  const e = {};
  if (!values.start_date) e.start_date = "Required";
  if (!values.end_date) e.end_date = "Required";
  if (values.start_date && values.end_date && values.start_date > values.end_date)
    e.end_date = "Must be after start date";
  if (!values.initial_capital || Number(values.initial_capital) <= 0)
    e.initial_capital = "Must be greater than 0";
  if (!values.portfolio_size || Number(values.portfolio_size) <= 0)
    e.portfolio_size = "Must be greater than 0";
  if (Number(values.portfolio_size) > 50)
    e.portfolio_size = "Max 50 allowed";
  ["min_roe","max_pe","min_market_cap","max_market_cap"].forEach(f => {
    if (values[f] !== "" && Number.isNaN(Number(values[f]))) e[f] = "Invalid number";
  });
  if (values.min_market_cap !== "" && values.max_market_cap !== "" &&
    Number(values.min_market_cap) > Number(values.max_market_cap))
    e.max_market_cap = "Max must be > min";
  return e;
}

function downloadBlob(filename, blob) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = filename; a.click();
  URL.revokeObjectURL(url);
}

function statusTone(s) {
  if (s.includes("healthy")) return "bg-gain";
  if (s.includes("unavailable") || s.includes("unexpected")) return "bg-loss";
  return "bg-faint";
}

function PageHeader({ label, title, subtitle, actions }) {
  return (
    <div style={{ marginBottom: 28, display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 16, flexWrap: "wrap" }}>
      <div>
        <div className="label" style={{ marginBottom: 4 }}>{label}</div>
        <h1 style={{ margin: 0, fontSize: 22, fontWeight: 600, color: "var(--color-text)", letterSpacing: "-0.02em", lineHeight: 1.2 }}>
          {title}
        </h1>
        {subtitle && <p style={{ margin: "6px 0 0", fontSize: 13, color: "var(--color-sub)", lineHeight: 1.6 }}>{subtitle}</p>}
      </div>
      {actions && <div style={{ display: "flex", gap: 8, flexShrink: 0 }}>{actions}</div>}
    </div>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState("configure");
  const [formValues, setFormValues] = useState(backtestDefaults);
  const [formErrors, setFormErrors] = useState({});
  const [formMessage, setFormMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [apiError, setApiError] = useState("");
  const [apiResult, setApiResult] = useState(null);

  useEffect(() => {
    let live = true;
    fetchHealth()
      .then(d => live && setBackendStatus(d.status === "ok" ? "Backend healthy" : "Unexpected status"))
      .catch(() => live && setBackendStatus("Backend unavailable"));
    return () => { live = false; };
  }, []);

  function handleChange({ target: { name, type, value, checked } }) {
    setFormValues(c => ({ ...c, [name]: type === "checkbox" ? checked : value }));
    setFormErrors(c => { if (!c[name]) return c; const n = { ...c }; delete n[name]; return n; });
  }

  function handleReset() {
    setFormValues(backtestDefaults);
    setFormErrors({});
    setFormMessage("Reset to defaults.");
    setApiError("");
    setApiResult(null);
  }

  function handleMetricToggle(metric) {
    setFormValues(c => {
      const exists = c.ranking_metrics.includes(metric);
      const ranking_metrics = exists
        ? c.ranking_metrics.filter(m => m !== metric)
        : [...c.ranking_metrics, metric];
      return { ...c, ranking_metrics, ranking_metric: ranking_metrics[0] ?? c.ranking_metric };
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const errs = validateForm(formValues);
    setFormErrors(errs);
    if (Object.keys(errs).length) { setFormMessage("Fix highlighted fields."); return; }
    setIsSubmitting(true);
    setApiError("");
    setFormMessage("Running backtest…");
    try {
      const result = await runBacktest(formValues);
      setApiResult(result);
      setFormMessage("Completed successfully.");
      setActiveTab("overview");
    } catch (err) {
      setApiError(err.message);
      setApiResult(null);
      setFormMessage("Request failed.");
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleCsvExport() {
    if (!apiResult?.records?.length) return;
    const headers = Object.keys(apiResult.records[0]);
    const csv = [headers.join(","), ...apiResult.records.map(r => headers.map(h => JSON.stringify(r[h] ?? "")).join(","))].join("\n");
    downloadBlob("backtest.csv", new Blob([csv], { type: "text/csv;charset=utf-8;" }));
  }

  function handleExcelExport() {
    if (!apiResult?.records?.length) return;
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(apiResult.records), "Positions");
    XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(apiResult.rebalance_summary ?? []), "Rebalances");
    XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet([apiResult.metrics ?? {}]), "Metrics");
    XLSX.writeFile(wb, "backtest.xlsx");
  }

  const hasResults = !!apiResult?.records?.length;
  const ExportActions = () => (
    <>
      <button className="btn-outline" onClick={handleCsvExport}>Export CSV</button>
      <button className="btn-run" onClick={handleExcelExport}>Export Excel</button>
    </>
  );

  return (
    <AppShell
      activeTab={activeTab}
      onTabChange={setActiveTab}
      hasResults={hasResults}
      backendStatus={backendStatus}
      statusTone={statusTone(backendStatus)}
    >
      {activeTab === "configure" && (
        <div style={{ maxWidth: 860 }}>
          <PageHeader
            label="Strategy Setup"
            title="Configure Backtest"
            subtitle="Set your date range, capital, and stock screening rules. Results appear automatically when the run completes."
          />
          <BacktestForm
            values={formValues}
            errors={formErrors}
            onChange={handleChange}
            onMetricToggle={handleMetricToggle}
            onSubmit={handleSubmit}
            onReset={handleReset}
            isSubmitting={isSubmitting}
            formMessage={formMessage}
          />
          {apiError && (
            <div className="panel" style={{ marginTop: 20, padding: "16px 20px", borderColor: "rgba(224,92,92,0.3)" }}>
              <div className="label" style={{ color: "var(--color-down)", marginBottom: 8 }}>Request Failed</div>
              <p className="mono" style={{ margin: 0, fontSize: 12, color: "var(--color-down)", lineHeight: 1.7 }}>{apiError}</p>
            </div>
          )}
        </div>
      )}

      {activeTab === "overview" && (
        <div>
          <PageHeader
            label="Run Summary"
            title="Overview"
            subtitle={hasResults
              ? `${apiResult.total_records} positions · ${formatCurrency(apiResult?.metrics?.initial_capital)} → ${formatCurrency(apiResult?.metrics?.final_capital)}`
              : "No results yet"}
            actions={hasResults ? <ExportActions /> : null}
          />
          {hasResults ? (
            <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
              <MetricsGrid metrics={apiResult?.metrics} />
              <TopMovers winners={apiResult?.top_winners} losers={apiResult?.top_losers} />
            </div>
          ) : (
            <EmptyState title="No results yet" description="Run a backtest from Configure to populate this view." />
          )}
        </div>
      )}

      {activeTab === "analytics" && (
        <div>
          <PageHeader label="Charts & Curves" title="Analytics" subtitle="Equity curve, drawdown profile, and rebalance history." />
          {hasResults ? (
            <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
              <EquityCurve periods={apiResult?.equity_curve} drawdowns={apiResult?.drawdown_curve} />
              <RebalanceSummary periods={apiResult?.rebalance_summary} />
            </div>
          ) : (
            <EmptyState title="No chart data" description="Run a backtest to see equity and drawdown curves." />
          )}
        </div>
      )}

      {activeTab === "positions" && (
        <div>
          <PageHeader
            label="Position-Level Detail"
            title="Positions"
            subtitle="Every holding across all rebalance periods."
            actions={hasResults ? <ExportActions /> : null}
          />
          {hasResults
            ? <PositionsTable records={apiResult?.records} />
            : <EmptyState title="No position data" description="Run a backtest to see individual stock positions." />
          }
        </div>
      )}
    </AppShell>
  );
}

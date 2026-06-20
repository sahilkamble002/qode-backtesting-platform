export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "";

function normalizePayload(payload) {
  return {
    ...payload,
    initial_capital: Number(payload.initial_capital),
    portfolio_size: Number(payload.portfolio_size),
    min_roe: payload.min_roe === "" ? null : Number(payload.min_roe),
    max_pe: payload.max_pe === "" ? null : Number(payload.max_pe),
    min_market_cap:
      payload.min_market_cap === "" ? null : Number(payload.min_market_cap),
    max_market_cap:
      payload.max_market_cap === "" ? null : Number(payload.max_market_cap),
    ranking_metrics: payload.ranking_metrics?.length ? payload.ranking_metrics : null,
  };
}

export async function fetchHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error("Failed to connect to backend health endpoint");
  }

  return response.json();
}

export async function runBacktest(payload) {
  const response = await fetch(`${API_BASE_URL}/backtest`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(normalizePayload(payload)),
  });

  if (!response.ok) {
    let errorMessage = "Backtest request failed";
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorData.message || errorMessage;
    } catch {
      errorMessage = `Error ${response.status}: ${response.statusText}`;
    }
    throw new Error(errorMessage);
  }

  const data = await response.json();
  console.log("Backtest response:", data);
  console.log("Records count:", data.records?.length);
  console.log("Metrics:", data.metrics);
  return data;
}

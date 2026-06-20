import { useState } from "react";

const NAV = [
  {
    id: "configure",
    label: "Configure",
    icon: (
      <svg width="15" height="15" fill="none" stroke="currentColor" strokeWidth="1.6" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
      </svg>
    ),
    always: true,
  },
  {
    id: "overview",
    label: "Overview",
    icon: (
      <svg width="15" height="15" fill="none" stroke="currentColor" strokeWidth="1.6" viewBox="0 0 24 24">
        <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
      </svg>
    ),
  },
  {
    id: "analytics",
    label: "Analytics",
    icon: (
      <svg width="15" height="15" fill="none" stroke="currentColor" strokeWidth="1.6" viewBox="0 0 24 24">
        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
      </svg>
    ),
  },
  {
    id: "positions",
    label: "Positions",
    icon: (
      <svg width="15" height="15" fill="none" stroke="currentColor" strokeWidth="1.6" viewBox="0 0 24 24">
        <path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"/>
      </svg>
    ),
  },
];

export function AppShell({ children, activeTab, onTabChange, hasResults, backendStatus, statusTone }) {
  const [open, setOpen] = useState(false);

  return (
    <div style={{ display: "flex", minHeight: "100dvh", width: "100%" }}>
      {/* Mobile overlay */}
      {open && (
        <div
          onClick={() => setOpen(false)}
          style={{
            position: "fixed", inset: 0, zIndex: 40,
            background: "rgba(0,0,0,0.7)", backdropFilter: "blur(2px)"
          }}
        />
      )}

      {/* Sidebar */}
      <aside
        style={{
          position: "fixed", top: 0, left: 0, zIndex: 50,
          height: "100dvh", width: 280,
          background: "var(--color-surface)",
          borderRight: "1px solid var(--color-border)",
          display: "flex", flexDirection: "column",
          transform: open ? "translateX(0)" : undefined,
          transition: "transform 0.2s",
        }}
        className={`sidebar ${open ? "" : "sidebar-hidden"}`}
      >
        {/* Brand */}
        <div style={{ padding: "28px 24px 20px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 4 }}>
            <div style={{
              width: 28, height: 28, borderRadius: 6,
              background: "var(--color-gold)",
              display: "flex", alignItems: "center", justifyContent: "center",
            }}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0a0b0d" strokeWidth="2.2">
                <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>
              </svg>
            </div>
            <div>
              <div style={{ fontSize: 13, fontWeight: 600, color: "var(--color-text)", lineHeight: 1.2 }}>Qode</div>
              <div style={{ fontSize: 10.5, color: "var(--color-sub)", letterSpacing: "0.04em" }}>Backtesting</div>
            </div>
          </div>
        </div>

        <hr className="divider" style={{ margin: "0 0 16px" }} />

        {/* Status */}
        <div style={{ padding: "0 16px 16px" }}>
          <div style={{
            display: "flex", alignItems: "center", gap: 8,
            background: "var(--color-raised)", borderRadius: 6,
            padding: "8px 12px",
            border: "1px solid var(--color-border)",
          }}>
            <span style={{
              width: 6, height: 6, borderRadius: "50%", flexShrink: 0,
              background: statusTone === "bg-gain" ? "var(--color-up)"
                : statusTone === "bg-loss" ? "var(--color-down)"
                : "var(--color-dim)",
            }} />
            <span className="mono" style={{ fontSize: 11, color: "var(--color-sub)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
              {backendStatus}
            </span>
          </div>
        </div>

        {/* Nav section label */}
        <div style={{ padding: "0 20px 8px" }}>
          <span className="sub-label">Workspace</span>
        </div>

        {/* Nav items */}
        <nav style={{ padding: "0 8px", flex: 1 }}>
          {NAV.map((item) => {
            const disabled = !item.always && !hasResults;
            const active = activeTab === item.id;
            return (
              <button
                key={item.id}
                disabled={disabled}
                onClick={() => { if (!disabled) { onTabChange(item.id); setOpen(false); } }}
                className={`nav-item ${active ? "active" : ""}`}
                style={{ marginBottom: 2 }}
              >
                <span style={{ opacity: active ? 1 : 0.7, flexShrink: 0 }}>{item.icon}</span>
                <span>{item.label}</span>
                {disabled && (
                  <span style={{
                    marginLeft: "auto", fontSize: 9.5,
                    letterSpacing: "0.08em", textTransform: "uppercase",
                    color: "var(--color-dim)", fontFamily: "var(--font-mono)"
                  }}>run first</span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Footer */}
        <div style={{ padding: "16px 20px", borderTop: "1px solid var(--color-border)" }}>
          <div className="sub-label" style={{ marginBottom: 2 }}>Qode Advisors LLP</div>
          <div style={{ fontSize: 11, color: "var(--color-dim)" }}>Internal Research Tool</div>
        </div>
      </aside>

      {/* Content area */}
      <div style={{ flex: 1, marginLeft: 280, display: "flex", flexDirection: "column", minWidth: 0 }}>
        {/* Mobile topbar */}
        <div className="mobile-bar" style={{
          display: "none", alignItems: "center", gap: 12,
          padding: "12px 16px",
          background: "var(--color-surface)",
          borderBottom: "1px solid var(--color-border)",
        }}>
          <button
            onClick={() => setOpen(true)}
            style={{
              background: "var(--color-raised)", border: "1px solid var(--color-border)",
              borderRadius: 5, padding: "6px 8px", color: "var(--color-sub)", cursor: "pointer"
            }}
          >
            <svg width="15" height="15" fill="none" stroke="currentColor" strokeWidth="1.6" viewBox="0 0 24 24">
              <path d="M3 12h18M3 6h18M3 18h18" strokeLinecap="round"/>
            </svg>
          </button>
          <span className="sub-label">{NAV.find(n => n.id === activeTab)?.label}</span>
        </div>

        <main style={{ flex: 1, padding: "36px 40px", maxWidth: 1100, width: "100%" }}>
          {children}
        </main>
      </div>

      <style>{`
        @media (max-width: 900px) {
          .sidebar { transform: translateX(-100%); }
          .sidebar-hidden { transform: translateX(-100%) !important; }
          div[style*="marginLeft: 280"] { margin-left: 0 !important; }
          .mobile-bar { display: flex !important; }
          main { padding: 20px 16px !important; }
        }
        @media (min-width: 901px) {
          .sidebar { transform: translateX(0) !important; }
        }
      `}</style>
    </div>
  );
}

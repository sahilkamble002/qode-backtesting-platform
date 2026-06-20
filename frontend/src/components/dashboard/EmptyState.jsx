export function EmptyState({ title, description }) {
  return (
    <div style={{
      padding: "60px 32px", textAlign: "center",
      border: "1px dashed var(--color-border2)", borderRadius: 8,
    }}>
      <div style={{
        width: 36, height: 36, borderRadius: 8,
        background: "var(--color-raised)", border: "1px solid var(--color-border)",
        margin: "0 auto 14px",
        display: "flex", alignItems: "center", justifyContent: "center",
      }}>
        <svg width="16" height="16" fill="none" stroke="var(--color-dim)" strokeWidth="1.5" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>
        </svg>
      </div>
      <p style={{ margin: "0 0 4px", fontSize: 13.5, fontWeight: 600, color: "var(--color-text)" }}>{title}</p>
      <p style={{ margin: 0, fontSize: 12.5, color: "var(--color-sub)", maxWidth: 320, marginInline: "auto", lineHeight: 1.6 }}>{description}</p>
    </div>
  );
}

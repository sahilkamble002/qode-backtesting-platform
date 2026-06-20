export function SectionCard({ title, description }) {
  return (
    <article className="ledger-panel panel-padding">
      <h2 className="section-heading">{title}</h2>
      <p className="mt-3 text-sm leading-6 text-mute">{description}</p>
    </article>
  );
}

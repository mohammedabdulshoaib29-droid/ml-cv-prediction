import React from 'react';

function SectionCard({ title, subtitle, children, className = '' }) {
  return (
    <section className={`section-card ${className}`.trim()}>
      {title || subtitle ? (
        <div className="section-card__header">
          {title ? <h2 className="section-card__title">{title}</h2> : null}
          {subtitle ? <p className="section-card__subtitle">{subtitle}</p> : null}
        </div>
      ) : null}
      <div className="section-card__body">{children}</div>
    </section>
  );
}

export default SectionCard;
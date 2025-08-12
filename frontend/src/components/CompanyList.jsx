import React from 'react'

export default function CompanyList({ companies = [], onSelect, selected }) {
  const handleKeyDown = (e, company) => {
    if (e.key === 'Enter' || e.key === ' ') {
      onSelect(company)
    }
  }

  return (
    <div className="company-list">
      {companies.map(c => (
        <div
          key={c.symbol}
          className={`item ${selected?.symbol === c.symbol ? 'selected' : ''}`}
          onClick={() => onSelect(c)}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => handleKeyDown(e, c)}
        >
          <div className="sym">{c.symbol.replace('.NS', '')}</div>
          <div className="name">{c.name}</div>
        </div>
      ))}
    </div>
  )
}

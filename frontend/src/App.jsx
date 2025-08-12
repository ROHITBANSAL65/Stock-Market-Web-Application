import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CompanyList from './components/CompanyList';
import ChartArea from './components/ChartArea';

const API_BASE = 'http://localhost:8000'; // Move to .env in real apps

// Loader component (uses CSS class from your styles.css)
function Loader() {
  return <div className="loader" />;
}

export default function App() {
  const [companies, setCompanies] = useState([]);
  const [selected, setSelected] = useState(null);
  const [historical, setHistorical] = useState([]);
  const [loadingCompanies, setLoadingCompanies] = useState(false);
  const [loadingHistorical, setLoadingHistorical] = useState(false);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    setLoadingCompanies(true);
    axios.get(`${API_BASE}/companies`)
      .then(res => {
        setCompanies(res.data);
        setLoadingCompanies(false);
        if (res.data.length > 0) setSelected(res.data[0]);
      })
      .catch(() => {
        setError('Failed to load companies');
        setLoadingCompanies(false);
      });
  }, []);

  useEffect(() => {
    if (!selected) {
      setHistorical([]);
      return;
    }
    setLoadingHistorical(true);
    setError(null);
    axios.get(`${API_BASE}/historical/${encodeURIComponent(selected.symbol)}`)
      .then(res => {
        setHistorical(res.data);
        setLoadingHistorical(false);
      })
      .catch(() => {
        setError('Failed to load historical data');
        setLoadingHistorical(false);
      });
  }, [selected]);

  // Filter companies by search term (case-insensitive)
  const filteredCompanies = companies.filter(c =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.symbol.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="app">
      <aside className="left-panel">
        <h3 style={{ marginTop: 0, marginBottom: 16, fontWeight: 700, color: '#1a237e' }}>Companies</h3>
        <input
          type="search"
          placeholder="Search companies"
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          aria-label="Search companies"
        />
        {loadingCompanies ? (
          <Loader />
        ) : error && !loadingHistorical ? (
          <p style={{ color: 'red', marginTop: 12 }}>{error}</p>
        ) : (
          <CompanyList
            companies={filteredCompanies}
            onSelect={setSelected}
            selected={selected}
          />
        )}
      </aside>

      <main className="main-panel">
        <header>
          <h2 style={{ marginTop: 0, marginBottom: 20, fontWeight: 700, color: '#1a237e' }}>
            {selected ? `${selected.name} (${selected.symbol})` : 'Select a company'}
          </h2>
        </header>

        {/* 52-week stats panel */}
        {selected && selected.stats && (
          <div className="stats" role="region" aria-label="52 Week Statistics">
            <div className="stat-item">
              <div className="label">52-Week High</div>
              <div className="value">{selected.stats.week52High.toFixed(2)}</div>
            </div>
            <div className="stat-item">
              <div className="label">52-Week Low</div>
              <div className="value">{selected.stats.week52Low.toFixed(2)}</div>
            </div>
            <div className="stat-item">
              <div className="label">Avg Volume</div>
              <div className="value">{selected.stats.avgVolume.toLocaleString()}</div>
            </div>
          </div>
        )}

        {loadingHistorical ? (
          <Loader />
        ) : (
          <ChartArea data={historical} />
        )}

        {error && !loadingCompanies && !loadingHistorical && (
          <p style={{ color: 'red', marginTop: 16 }}>{error}</p>
        )}
      </main>
    </div>
  );
}

import React, { useState } from 'react';

function AppNavbar({ currentRoute, navigate, navItems }) {
  const [menuOpen, setMenuOpen] = useState(false);

  const handleNavigate = (route) => {
    navigate(route);
    setMenuOpen(false);
  };

  return (
    <header className="app-navbar">
      <div className="app-navbar__inner">
        <button className="app-navbar__brand" type="button" onClick={() => handleNavigate('/')}>
          <span className="app-navbar__brand-mark">BiFe₂O₃</span>
          <span className="app-navbar__brand-text">ML Prediction System</span>
        </button>

        <button
          type="button"
          className="app-navbar__toggle"
          onClick={() => setMenuOpen((open) => !open)}
          aria-label="Toggle navigation"
        >
          ☰
        </button>

        <nav className={`app-navbar__nav ${menuOpen ? 'app-navbar__nav--open' : ''}`}>
          {Object.entries(navItems).map(([route, label]) => (
            <button
              key={route}
              type="button"
              onClick={() => handleNavigate(route)}
              className={`app-navbar__link ${currentRoute === route ? 'app-navbar__link--active' : ''}`}
            >
              {label}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
}

export default AppNavbar;
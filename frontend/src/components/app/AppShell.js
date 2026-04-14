import React from 'react';
import AppNavbar from './AppNavbar';

function AppShell({ currentRoute, navigate, navItems, children }) {
  return (
    <div className="app-shell">
      <AppNavbar currentRoute={currentRoute} navigate={navigate} navItems={navItems} />
      <main className="app-shell__content">{children}</main>
    </div>
  );
}

export default AppShell;
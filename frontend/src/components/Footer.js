import React from 'react';
import '../styles/Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3>🔬 CV Prediction</h3>
          <p>Advanced ML for Cyclic Voltammetry Analysis</p>
          <p className="copyright">© 2026 CV Prediction. All rights reserved.</p>
        </div>

        <div className="footer-section">
          <h4>Product</h4>
          <ul>
            <li><a href="#overview">Overview</a></li>
            <li><a href="#models">Models</a></li>
            <li><a href="#performance">Performance</a></li>
            <li><a href="#predict">Make Prediction</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Resources</h4>
          <ul>
            <li><button onClick={() => window.alert('Documentation coming soon')} className="link-button">Documentation</button></li>
            <li><button onClick={() => window.alert('API Reference coming soon')} className="link-button">API Reference</button></li>
            <li><button onClick={() => window.alert('Tutorials coming soon')} className="link-button">Tutorials</button></li>
            <li><a href="https://arxiv.org/" target="_blank" rel="noopener noreferrer">Research Papers</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Company</h4>
          <ul>
            <li><button onClick={() => window.alert('About Us coming soon')} className="link-button">About Us</button></li>
            <li><button onClick={() => window.alert('Contact coming soon')} className="link-button">Contact</button></li>
            <li><a href="https://twitter.com/" target="_blank" rel="noopener noreferrer">Twitter</a></li>
            <li><a href="https://github.com/" target="_blank" rel="noopener noreferrer">GitHub</a></li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <p>Built with ❤️ for Materials Scientists & Engineers</p>
      </div>
    </footer>
  );
}

export default Footer;
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
            <li><a href="#">Documentation</a></li>
            <li><a href="#">API Reference</a></li>
            <li><a href="#">Tutorials</a></li>
            <li><a href="#">Research Papers</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Company</h4>
          <ul>
            <li><a href="#">About Us</a></li>
            <li><a href="#">Contact</a></li>
            <li><a href="#">Twitter</a></li>
            <li><a href="#">GitHub</a></li>
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
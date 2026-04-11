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


      </div>

      <div className="footer-bottom">
        <p>Built with ❤️ for Materials Scientists & Engineers</p>
      </div>
    </footer>
  );
}

export default Footer;
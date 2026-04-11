import React from 'react';
import '../styles/ReferencesSection.css';

function ReferencesSection() {
  return (
    <section className="references">
      <div className="references-container">
        <h2>🔗 References & Resources</h2>
        
        <div className="references-grid">
          <div className="reference-card">
            <h3>Research Papers</h3>
            <ul>
              <li><a href="#">CV Analysis with Deep Learning</a></li>
              <li><a href="#">XGBoost for Materials Science</a></li>
              <li><a href="#">Neural Networks in Electrochemistry</a></li>
              <li><a href="#">Ensemble Methods Comparison</a></li>
            </ul>
          </div>

          <div className="reference-card">
            <h3>Tools & Libraries</h3>
            <ul>
              <li><a href="https://scikit-learn.org/">Scikit-learn</a></li>
              <li><a href="https://xgboost.readthedocs.io/">XGBoost</a></li>
              <li><a href="https://www.tensorflow.org/">TensorFlow</a></li>
              <li><a href="https://pandas.pydata.org/">Pandas</a></li>
            </ul>
          </div>

          <div className="reference-card">
            <h3>Code Resources</h3>
            <ul>
              <li><a href="https://github.com/">GitHub Repository</a></li>
              <li><a href="#">API Documentation</a></li>
              <li><a href="#">Model Training Guide</a></li>
              <li><a href="#">Dataset Preparation</a></li>
            </ul>
          </div>

          <div className="reference-card">
            <h3>Materials Database</h3>
            <ul>
              <li><a href="#">Materials Project</a></li>
              <li><a href="#">ICSD Database</a></li>
              <li><a href="#">NIST Materials Data</a></li>
              <li><a href="#">Electrochemistry Database</a></li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}

export default ReferencesSection;
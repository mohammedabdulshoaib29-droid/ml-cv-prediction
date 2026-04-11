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
              <li><a href="https://arxiv.org/" target="_blank" rel="noopener noreferrer">CV Analysis with Deep Learning</a></li>
              <li><a href="https://arxiv.org/" target="_blank" rel="noopener noreferrer">XGBoost for Materials Science</a></li>
              <li><a href="https://arxiv.org/" target="_blank" rel="noopener noreferrer">Neural Networks in Electrochemistry</a></li>
              <li><a href="https://arxiv.org/" target="_blank" rel="noopener noreferrer">Ensemble Methods Comparison</a></li>
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
              <li><a href="https://github.com/" target="_blank" rel="noopener noreferrer">GitHub Repository</a></li>
              <li><button onClick={() => window.alert('API Documentation coming soon')} className="link-button">API Documentation</button></li>
              <li><button onClick={() => window.alert('Model Training Guide coming soon')} className="link-button">Model Training Guide</button></li>
              <li><button onClick={() => window.alert('Dataset Preparation coming soon')} className="link-button">Dataset Preparation</button></li>
            </ul>
          </div>

          <div className="reference-card">
            <h3>Materials Database</h3>
            <ul>
              <li><a href="https://materialsproject.org/" target="_blank" rel="noopener noreferrer">Materials Project</a></li>
              <li><a href="https://icsd.fiz-karlsruhe.de/" target="_blank" rel="noopener noreferrer">ICSD Database</a></li>
              <li><a href="https://www.nist.gov/" target="_blank" rel="noopener noreferrer">NIST Materials Data</a></li>
              <li><a href="https://www.electrochem.org/" target="_blank" rel="noopener noreferrer">Electrochemistry Database</a></li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}

export default ReferencesSection;
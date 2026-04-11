import React from 'react';
import '../styles/ReferencesSection.css';

function ReferencesSection() {
  return (
    <section className="references">
      <div className="references-container">
        <h2>🔗 References & Resources</h2>
        
        <div className="references-grid">
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
              <li><a href="https://github.com/mohammedabdulshoaib29-droid/ml-cv-prediction" target="_blank" rel="noopener noreferrer">GitHub Repository</a></li>
            </ul>
          </div>

        </div>
      </div>
    </section>
  );
}

export default ReferencesSection;
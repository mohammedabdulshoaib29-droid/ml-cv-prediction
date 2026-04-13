import React from 'react';
import {
  ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer
} from 'recharts';

const PredictionPlot = ({ actual, predicted, modelName }) => {
  if (!actual || !predicted || actual.length === 0) {
    return <div className="no-data">No prediction data available</div>;
  }

  // Create scatter data
  const data = actual.slice(0, 100).map((a, idx) => ({
    actual: parseFloat(a.toFixed(4)),
    predicted: parseFloat(predicted[idx].toFixed(4))
  }));

  return (
    <div className="prediction-plot">
      <ResponsiveContainer width="100%" height={400}>
        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="actual" name="Actual Values" />
          <YAxis dataKey="predicted" name="Predicted Values" />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Legend />
          <Scatter
            name={modelName}
            data={data}
            fill="#8884d8"
          />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PredictionPlot;

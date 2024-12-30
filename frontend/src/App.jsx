import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'plotly.js-dist-min';
import './App.css';

function App() {
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [imageError, setImageError] = useState(false);
  const [selectedModel, setSelectedModel] = useState('slaughterhouse');
  const [selectedCondition, setSelectedCondition] = useState(1);

  const fetchResults = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('https://halal-compliance-app-tunnel-95k4pqa2.devinapps.com/api/results');
      if (!response.data || (!response.data.slaughterhouse && !response.data.food_processing)) {
        throw new Error('Invalid or missing data received from server');
      }
      setResults(response.data);
    } catch (error) {
      setError(error.response?.data?.detail || error.message || 'Failed to fetch simulation results');
      console.error('Error fetching results:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResults();
  }, []);

  const handleModelChange = (event) => {
    setSelectedModel(event.target.value);
    setImageError(false);
  };

  const handleConditionChange = (event) => {
    setSelectedCondition(event.target.value);
    setImageError(false);
  };

  const handleImageError = () => {
    setImageError(true);
    console.error('Failed to load visualization image');
  };

  const retryImageLoad = () => {
    setImageError(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Halal Compliance Monitoring System</h1>
      </header>
      
      <div className="controls">
        <select value={selectedModel} onChange={handleModelChange}>
          <option value="slaughterhouse">Slaughterhouse Model</option>
          <option value="food_processing">Food Processing Model</option>
        </select>
        
        {/* Removed dimension selector */}
        
        <select value={selectedCondition} onChange={handleConditionChange}>
          {selectedModel === 'slaughterhouse' ? (
            <>
              <option value="1">Health Check Compliance</option>
              <option value="2">Prayer Recitation</option>
              <option value="3">Jugular Vein Location</option>
              <option value="4">Sharp Knife Usage</option>
              <option value="5">Halal Area Compliance</option>
              <option value="6">Slaughterer Qualification</option>
            </>
          ) : (
            <>
              <option value="1">Storage Temperature</option>
              <option value="2">Cutting Area Compliance</option>
              <option value="3">Cooking Area Compliance</option>
            </>
          )}
        </select>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={fetchResults}>Retry Loading Data</button>
        </div>
      )}

      {loading ? (
        <div className="loading-spinner">Loading simulation data...</div>
      ) : (
        <>
          <div className="visualization-container">
            {imageError ? (
              <div className="error-message">
                <p>Failed to load visualization image. The image might be missing or corrupted.</p>
                <button onClick={retryImageLoad}>Retry Loading Image</button>
              </div>
            ) : (
              <img 
                src={`https://halal-compliance-app-tunnel-95k4pqa2.devinapps.com/api/visualizations/${selectedModel}/2d/condition${selectedCondition}.png`}
                alt={`${selectedModel} condition ${selectedCondition} visualization`}
                className="visualization"
                onError={handleImageError}
                onLoad={() => setImageError(false)}
              />
            )}
          </div>

          {results && !error && (
            <div className="results-container">
              <h2>Simulation Results</h2>
              <pre>{JSON.stringify(results[selectedModel], null, 2)}</pre>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default App;

import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please select an image first!");
    
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://localhost:5000/predict', formData);
      setResult(res.data);
    } catch (err) {
      alert("Error detecting face. Try a clearer portrait.");
    }
    setLoading(false);
  };

  return (
  <div className="app-container">
    <div className="card">
      <h1 className="title">True<span className="lens">Lens</span></h1>
      <p className="subtitle">AI-powered face authenticity detection</p>

      <input
        type="file"
        className="file-input"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button className="button" onClick={handleUpload} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Image"}
      </button>

      {result && (
        <div className="result">
          <span
            className={
              result.verdict === "AI-GENERATED" ? "fake" : "real"
            }
          >
            {result.verdict === "AI-GENERATED"
              ? " AI Generated"
              : " Real Human"}
          </span>
        </div>
      )}
    </div>
  </div>
);
}

export default App;
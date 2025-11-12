import { useState, useEffect } from 'react';
import { getDatasets } from '../services/api';
import { Link } from 'react-router-dom';
import './DatasetList.css';

function DatasetList() {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      const data = await getDatasets();
      setDatasets(data);
    } catch (err) {
      setError('Failed to load datasets');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="dataset-list">
      <h2>Upload History (Last 5 Datasets)</h2>
      {datasets.length === 0 ? (
        <p>No datasets uploaded yet</p>
      ) : (
        <div className="datasets-grid">
          {datasets.map((dataset) => (
            <Link to={`/datasets/${dataset.id}`} key={dataset.id} className="dataset-card">
              <h3>{dataset.name}</h3>
              <p className="date">{new Date(dataset.uploaded_at).toLocaleString()}</p>
              <div className="stats">
                <span>Count: {dataset.total_count}</span>
                <span>Avg Flowrate: {dataset.avg_flowrate.toFixed(2)}</span>
                <span>Avg Pressure: {dataset.avg_pressure.toFixed(2)}</span>
                <span>Avg Temp: {dataset.avg_temperature.toFixed(2)}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

export default DatasetList;

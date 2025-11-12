import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getDatasetDetail, downloadPDF } from '../services/api';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';
import './DatasetDetail.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

function DatasetDetail() {
  const { id } = useParams();
  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDataset();
  }, [id]);

  const fetchDataset = async () => {
    try {
      const data = await getDatasetDetail(id);
      setDataset(data);
    } catch (err) {
      setError('Failed to load dataset details');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    downloadPDF(id, `${dataset.name}_report.pdf`);
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!dataset) return <div className="error">Dataset not found</div>;

  const avgData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Values',
        data: [dataset.avg_flowrate, dataset.avg_pressure, dataset.avg_temperature],
        backgroundColor: ['rgba(54, 162, 235, 0.6)', 'rgba(255, 99, 132, 0.6)', 'rgba(255, 206, 86, 0.6)'],
      },
    ],
  };

  const typeData = {
    labels: Object.keys(dataset.type_distribution),
    datasets: [
      {
        label: 'Equipment Count by Type',
        data: Object.values(dataset.type_distribution),
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
      },
    ],
  };

  return (
    <div className="dataset-detail">
      <div className="header">
        <h2>{dataset.name}</h2>
        <button onClick={handleDownloadPDF} className="pdf-button">Download PDF Report</button>
      </div>
      
      <div className="summary-cards">
        <div className="card">
          <h3>Total Equipment</h3>
          <p className="big-number">{dataset.total_count}</p>
        </div>
        <div className="card">
          <h3>Avg Flowrate</h3>
          <p className="big-number">{dataset.avg_flowrate.toFixed(2)}</p>
        </div>
        <div className="card">
          <h3>Avg Pressure</h3>
          <p className="big-number">{dataset.avg_pressure.toFixed(2)}</p>
        </div>
        <div className="card">
          <h3>Avg Temperature</h3>
          <p className="big-number">{dataset.avg_temperature.toFixed(2)}</p>
        </div>
      </div>

      <div className="charts">
        <div className="chart-container">
          <h3>Average Values by Parameter</h3>
          <Bar data={avgData} />
        </div>
        <div className="chart-container">
          <h3>Equipment Type Distribution</h3>
          <Pie data={typeData} />
        </div>
      </div>

      <div className="equipment-table">
        <h3>Equipment Details</h3>
        <table>
          <thead>
            <tr>
              <th>Equipment Name</th>
              <th>Type</th>
              <th>Flowrate</th>
              <th>Pressure</th>
              <th>Temperature</th>
            </tr>
          </thead>
          <tbody>
            {dataset.csv_data.map((row, index) => (
              <tr key={index}>
                <td>{row['Equipment Name']}</td>
                <td>{row.Type}</td>
                <td>{row.Flowrate}</td>
                <td>{row.Pressure}</td>
                <td>{row.Temperature}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default DatasetDetail;

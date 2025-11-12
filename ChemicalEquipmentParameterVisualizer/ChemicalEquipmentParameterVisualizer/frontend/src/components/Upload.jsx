import { useState } from 'react';
import { uploadCSV } from '../services/api';
import { useNavigate } from 'react-router-dom';
import './Upload.css';

function Upload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file');
      return;
    }

    setUploading(true);
    setMessage('');

    try {
      const result = await uploadCSV(file);
      setMessage('File uploaded successfully!');
      setTimeout(() => {
        navigate(`/datasets/${result.id}`);
      }, 1000);
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.error || error.message}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Equipment Data CSV</h2>
      <div className="upload-box">
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          disabled={uploading}
        />
        <button onClick={handleUpload} disabled={uploading || !file}>
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      </div>
      {message && <p className={message.startsWith('Error') ? 'error-message' : 'success-message'}>{message}</p>}
      
      <div className="upload-info">
        <h3>Required CSV Format:</h3>
        <pre>
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
        </pre>
      </div>
    </div>
  );
}

export default Upload;

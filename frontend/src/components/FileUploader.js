import React, { useState } from 'react';
import '../styles/FileUploader.css';

const FileUploader = ({ onFileSelect, label = "Upload Test Dataset" }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setFileName(file ? file.name : '');
    onFileSelect(file);
  };

  const clearFile = () => {
    setSelectedFile(null);
    setFileName('');
    document.getElementById('test-file-input').value = '';
    onFileSelect(null);
  };

  return (
    <div className="file-uploader-container">
      <h3>{label}</h3>
      <div className="upload-area">
        <input
          id="test-file-input"
          type="file"
          accept=".xlsx,.xls,.csv"
          onChange={handleFileChange}
          className="file-input"
        />
        <label htmlFor="test-file-input" className="upload-label">
          <div className="upload-icon">📁</div>
          <div className="upload-text">
            {fileName ? `Selected: ${fileName}` : 'Click to upload test dataset'}
          </div>
        </label>
      </div>
      {selectedFile && (
        <div className="file-info">
          <p>File: {fileName}</p>
          <p>Size: {(selectedFile.size / 1024).toFixed(2)} KB</p>
          <button onClick={clearFile} className="clear-btn">Remove File</button>
        </div>
      )}
      <p className="format-info">Supported formats: .xlsx, .xls, .csv</p>
    </div>
  );
};

export default FileUploader;

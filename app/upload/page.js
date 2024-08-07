'use client';

import { useState } from 'react';

export default function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [personCount, setPersonCount] = useState(null);
  const [annotatedImage, setAnnotatedImage] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    console.log('File selected:', event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    console.log('Uploading file:', selectedFile);

    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      console.log('Response status:', res.status);

      if (res.ok) {
        const data = await res.json();
        setPersonCount(data.personCount);
        setAnnotatedImage(data.annotatedImage);
        alert('File uploaded successfully');
        console.log('Response:', data);
      } else {
        alert('File upload failed');
        console.error('Upload failed:', res.statusText);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('File upload failed');
    }
  };

  return (
    <div>
      <h1>Upload an Image</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {personCount !== null && (
        <div>
          <h2>People Count: {personCount}</h2>
          {annotatedImage && <img src={annotatedImage} alt="Annotated" />}
        </div>
      )}
    </div>
  );
}

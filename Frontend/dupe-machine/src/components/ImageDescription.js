import React, { useState } from "react";

function ImageDescription() {
  const [description, setDescription] = useState("Upload an image and click analyze.");
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setImagePreview(URL.createObjectURL(file)); // Show preview of uploaded image
    }
  };

  const uploadAndAnalyzeImage = async () => {
    if (!selectedFile) {
      setDescription("Please select an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        setDescription("Error: " + data.error);
      } else {
        setDescription("Description: " + data.description);
      }
    } catch (error) {
      setDescription("Failed to upload image. Error: " + error.message);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px", fontFamily: "Arial, sans-serif" }}>
      <h1>AI Image Description</h1>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <br />
      {imagePreview && <img src={imagePreview} alt="Preview" style={{ maxWidth: "300px", marginTop: "10px" }} />}
      <br />
      <button onClick={uploadAndAnalyzeImage} style={{ padding: "10px 20px", fontSize: "16px", cursor: "pointer", marginTop: "10px" }}>
        Analyze Image
      </button>
      <p style={{ marginTop: "20px", fontSize: "18px" }}>{description}</p>
    </div>
  );
}

export default ImageDescription;

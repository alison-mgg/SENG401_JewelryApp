import React, { useState } from "react";
import "../styling/MainPage.css";
import NavBar from "./NavigationBar.js";
import { Form } from "react-router-dom";

function ImageDescription() {
  const [description, setDescription] = useState("Upload an image and click analyze.");
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [similarProducts, setSimilarProducts] = useState("");  // New state for similar products
  const [isHeartClicked, setIsHeartClicked] = useState(false);
  const [loading, setLoading] = useState(false);  // New state for loading
  const [text, setText] = useState("");
  //const [imageName, setImageName] = useState("");

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setImagePreview(URL.createObjectURL(file)); // Show preview of uploaded image
      uploadAndAnalyzeImage(file); // Automatically trigger analysis after file is selected
      setIsHeartClicked(false);
    }
  };

  const handleHeartClick = async () => {
    setIsHeartClicked(true);
  
    if (!selectedFile) {
      alert("No file selected");
      return;
    }
  
    try {
      const response = await fetch("http://localhost:5000/save-to-database", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: "a", // Replace with actual username
          imagePath: selectedFile, // The renamed filename
          similarProducts: similarProducts, // Include similar products
        }),
      });
  
      const data = await response.json();
  
      if (data.error) {
        console.error("Error saving to database:", data.error);
      } else {
        console.log("Successfully saved to database:", data.message);
      }
    } catch (error) {
      console.error("Failed to save to database:", error.message);
    }
  };

  // const uploadAndAnalyzeImage = async (file) => {
  //   if (!file) {
  //     setDescription("Please select an image first.");
  //     return;
  //   }

  //   setLoading(true);  // Set loading to true when the upload process starts
  //   const formData = new FormData();
  //   formData.append("image", file);

  //   try {
  //     const response = await fetch("http://localhost:5000/upload", {
  //       method: "POST",
  //       body: formData,
  //     });

  //     const data = await response.json();

  //     if (data.error) {
  //       setDescription("Error: " + data.error);
  //     } else {
  //       setDescription("Description: " + data.description);
  //       // Store the renamed filename returned from the backend
  //       setSelectedFile(data.filename); // Assuming the backend returns the renamed filename
  //     }
  //   } catch (error) {
  //     setDescription("Failed to upload image. Error: " + error.message);
  //   } finally {
  //     setLoading(false);  // Set loading to false after the request completes
  //   }
  // };

  const uploadAndAnalyzeImage = async (file) => {
    if (!file) {
        setDescription("Please select an image first.");
        return;
    }

    setLoading(true); // Show loading state
    const formData = new FormData();
    formData.append("image", file);

    try {
        const response = await fetch("http://localhost:5000/upload", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (data.error) {
            setDescription("Error: " + data.error);
        } else {
            setDescription(data.description); // Set the extracted description
            setSelectedFile(data.filename);  // Store the renamed filename from backend
            
            // ✅ Automatically fetch similar products once the description is received
            handleGetSimilarProducts(data.description);
        }
    } catch (error) {
        setDescription("Failed to upload image. Error: " + error.message);
    } finally {
        setLoading(false); // Hide loading state
    }
};

const handleGetSimilarProducts = async (latestDescription) => {  
  if (typeof latestDescription !== "string") {
      console.error(" Invalid description:", latestDescription);
      return;
  }

  setLoading(true);

  try {
      const response = await fetch("http://localhost:5000/similar-products", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({
              description: latestDescription.trim(),  // Ensure it's a valid string
          }),
      });

      const data = await response.json();
      console.log(" Similar Products Response:", data);

      if (data.error) {
          setSimilarProducts("Error: " + data.error);
      } else {
          setSimilarProducts(""); // Reset first
          setTimeout(() => {
              setSimilarProducts("Similar Products: " + data.similar_products);
          }, 50);
      }
  } catch (error) {
      setSimilarProducts("Failed to get similar products. Error: " + error.message);
  } finally {
      setLoading(false);
  }
};

    const handleChange = (e) => {
      setText(e.target.value);
    };
  

  const handleRegenerateClick = () => {
    setLoading(true);  // Set loading to true when regenerating description
    uploadAndAnalyzeImage(selectedFile); // Trigger analysis again for regeneration
    setIsHeartClicked(false);
  };

  return (
    <div className="container">
      <NavBar />
      <h1>Start By Uploading an Image</h1>

      {/* Image selection section */}
      <div className ="upload-container">
      <div className="image-upload-wrapper">
        <div className="image-upload-box">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            id="file-input"
          />
          {imagePreview && <img src={imagePreview} alt="Selected" className="uploaded-image" />}
        </div>   
        {/* Button below the image */}
        <button
          onClick={() => document.getElementById('file-input').click()}
          className="choose-image-button"
        >
          Choose an image
        </button>
        </div>
        <div className="input-txt">
      <textarea
        className="text-input"
        value={text}
        onChange={handleChange}
        placeholder="Enter your text here..."
      />
     {/* Submit text to AI button */}
     <button
          className="submit-text-button"
        >
          Submit Text
        </button>
        </div>
      </div>

      {/* <div className="description-box">
        <h2>Image Description</h2> */}
        
        {/* Only show loading message or description */}
        {/* {loading ? (
          <p>Loading... Please wait.</p>
        ) : (
          <p>{description}</p>
        )} */}

        {/* Regenerate Button in top-right */}
        {/* <button 
          className="regenerate-button"
          onClick={handleRegenerateClick} // Trigger analysis again on button click
        >
          <span className="material-icons">&#8635;</span> {/* Circle with arrow icon */}
        {/* </button>
      </div> */} 

      <button onClick={handleGetSimilarProducts} className="similar-products-button">
        Refresh Results
      </button>

      <div className="similar-products-box">
        <h2>Similar Products</h2>
        <p>{similarProducts}</p>
        
        {/* Heart Icon */}
        <span
          className="heart-icon"
          onClick={handleHeartClick}
          style={{ color: isHeartClicked ? 'red' : '#d2bfc7', cursor: 'pointer' }}
        >
          &#9829; {/* Heart icon */}
        </span>
      </div>
    </div>
  );
}

export default ImageDescription;

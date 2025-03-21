import React, { useState } from "react";
import "../styling/MainPage.css";
import NavBar from "./NavigationBar.js";
import { useAuth } from '../AuthContext';
import { Form } from "react-router-dom";

function ImageDescription() {
  const [description, setDescription] = useState("Upload an image and click analyze.");
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [similarProducts, setSimilarProducts] = useState("");  // New state for similar products
  const [isHeartClicked, setIsHeartClicked] = useState(false);
  const [loading, setLoading] = useState(false);  // New state for loading
  const [text, setText] = useState("");
  const [showLoginMessage, setShowLoginMessage] = useState(false); // State for login message popup
  const [showNoFileMessage, setShowNoFileMessage] = useState(false); // State for no file message popup
  const { isAuthenticated, username } = useAuth(); // Use isAuthenticated and username from AuthContext
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
    if (!isAuthenticated) {
      setShowLoginMessage(true);
      return;
    }
  
    if (!selectedFile) {
      setShowNoFileMessage(true);
      return;
    }
  
    setIsHeartClicked(true);
  
    try {
      const response = await fetch("http://localhost:5000/save-to-database", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          imagePath: selectedFile.name, // Ensure this is the correct filename
          similarProducts: Array.isArray(similarProducts) ? similarProducts.join(", ") : similarProducts, // Convert array to string if necessary
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
      
          // Ensure `data.description` is valid before calling `handleGetSimilarProducts`
          if (typeof data.description === "string" && data.description.trim() !== "") {
              handleGetSimilarProducts(data.description);
          } else {
              console.error("Invalid description received:", data.description);
          }
      }
    } catch (error) {
        setDescription("Failed to upload image. Error: " + error.message);
    } finally {
        setLoading(false); // Hide loading state
    }
};

const handleGetSimilarProducts = async (latestDescription) => {  
  if (typeof latestDescription !== "string") {
      console.error("Invalid description:", latestDescription);
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
              description: latestDescription.trim(),
          }),
      });

      const data = await response.json();
      console.log("Similar Products Response:", data);

      if (data.error) {
          setSimilarProducts(["Error: " + data.error]);
      } else {
          if (data.similar_products) {
              if (typeof data.similar_products === "string") {
                  let parsedProducts = data.similar_products
                      .split("\n")
                      .map(item => item.replace(/^\*\s*/g, "").trim()) // Remove leading * and spaces
                      .filter(item => 
                          !item.startsWith("Brand:") &&
                          !item.startsWith("Model:") &&
                          !item.startsWith("Similar Products") &&
                          !item.startsWith("Note:")
                      ) // Remove unwanted lines
                      .filter(item => item !== ""); // Remove empty lines

                  setSimilarProducts(parsedProducts);
              } else if (Array.isArray(data.similar_products)) {
                  setSimilarProducts(data.similar_products.map(item => item.replace(/^\*\s*/g, "").trim()));
              } else {
                  console.error("Unexpected format:", data.similar_products);
                  setSimilarProducts([]);
              }
          } else {
              setSimilarProducts([]);
          }
      }
  } catch (error) {
      setSimilarProducts(["Failed to get similar products. Error: " + error.message]);
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
  
      {/* Login message popup */}
      {showLoginMessage && (
        <div className="login-message-popup">
          <p>This feature is only available to logged-in users.</p>
          <button onClick={() => setShowLoginMessage(false)}>Close</button>
        </div>
      )}
  
      {/* No file selected message popup */}
      {showNoFileMessage && (
        <div className="login-message-popup">
          <p>Please select an image first.</p>
          <button onClick={() => setShowNoFileMessage(false)}>Close</button>
        </div>
      )}
  
      {/* Image selection section */}
      <div className="upload-container">
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
  
      <button onClick={handleGetSimilarProducts} className="similar-products-button">
        Get Similar Products
      </button>
  
      <div className="similar-products-box">
  <h2>Similar Products</h2>
  
  {similarProducts.length > 0 ? (
    <ul>
      {similarProducts.map((product, index) => (
        <li key={index}>{product}</li>
      ))}
    </ul>
  ) : (
    <p>No similar products found.</p>
  )}
  
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

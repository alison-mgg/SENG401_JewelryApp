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

// Handles the file selection event
const handleFileChange = (event) => {
  const file = event.target.files[0];  // Get the selected file
  if (file) {
    setSelectedFile(file);  // Store the selected file
    setImagePreview(URL.createObjectURL(file));  // Show preview of uploaded image
    uploadAndAnalyzeImage(file);  // Automatically trigger image upload and analysis after file selection
    setIsHeartClicked(false);  // Reset heart click state when a new file is selected
  }
};

// Handles the heart button click event (to save image to the database)
const handleHeartClick = async () => {
  if (!isAuthenticated) {
    setShowLoginMessage(true);  // Show login message if the user is not authenticated
    return;
  }

  if (!selectedFile) {
    setShowNoFileMessage(true);  // Show message if no file has been selected
    return;
  }

  setIsHeartClicked(true);  // Set heart click state to true to prevent multiple submissions

  try {
    // Send POST request to save image data to the database
    const response = await fetch("http://localhost:5000/save-to-database", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,  // Include the username
        imagePath: selectedFile,  // Include the filename of the selected image
        similarProducts: Array.isArray(similarProducts) ? similarProducts.join(", ") : similarProducts,  // Include the similar products as a comma-separated string
      }),
    });

    const data = await response.json();

    if (data.error) {
      console.error("Error saving to database:", data.error);
    } else {
      console.log("Successfully saved to database:", data.message);
    }
  } catch (error) {
    console.error("Failed to save to database:", error.message);  // Handle errors during database save
  }
};

// Function to upload the image and analyze it
const uploadAndAnalyzeImage = async (file) => {
  if (!file) {
    setDescription("Please select an image first.");  // Display message if no file is selected
    return;
  }

  setLoading(true);  // Show loading state while the image is being uploaded
  const formData = new FormData();
  formData.append("image", file);  // Append the selected image to FormData

  try {
    // Send POST request to upload the image and analyze it
    const response = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,  // Send the image file as FormData
    });

    const data = await response.json();

    if (data.error) {
      setDescription("Error: " + data.error);  // Display error message if the analysis fails
    } else {
      setDescription(data.description);  // Set the description from the analysis response
      setSelectedFile(data.filename);  // Store the renamed filename returned from the backend

      // Ensure the description is valid before fetching similar products
      if (typeof data.description === "string" && data.description.trim() !== "") {
        handleGetSimilarProducts(data.description);  // Fetch similar products based on the description
      } else {
        console.error("Invalid description received:", data.description);
      }
    }
  } catch (error) {
    setDescription("Failed to upload image. Error: " + error.message);  // Handle errors during image upload
  } finally {
    setLoading(false);  // Hide loading state after the process is finished
  }
};

// Function to fetch similar products based on the image description
const handleGetSimilarProducts = async (latestDescription) => {  
  if (typeof latestDescription !== "string") {
    console.error("Invalid description:", latestDescription);  // Log error if description is invalid
    return;
  }

  setLoading(true);  // Show loading state while fetching similar products

  try {
    // Send POST request to get similar products based on the description
    const response = await fetch("http://localhost:5000/similar-products", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        description: latestDescription.trim(),  // Send the trimmed description in the request body
      }),
    });

    const data = await response.json();
    console.log("Similar Products Response:", data);

    if (data.error) {
      setSimilarProducts(["Error: " + data.error]);  // Display error if fetching similar products fails
    } else {
      // Parse and display the similar products returned from the server
      if (data.similar_products) {
        if (typeof data.similar_products === "string") {
          let parsedProducts = data.similar_products
            .split("\n")
            .map(item => item.replace(/^\*\s*/g, "").trim())  // Clean up product names
            .filter(item => 
              !item.startsWith("Brand:") &&
              !item.startsWith("Model:") &&
              !item.startsWith("Similar Products") &&
              !item.startsWith("Note:")
            )  // Remove unnecessary lines
            .filter(item => item !== "");  // Remove empty lines

          setSimilarProducts(parsedProducts);  // Set the cleaned list of similar products
        } else if (Array.isArray(data.similar_products)) {
          setSimilarProducts(data.similar_products.map(item => item.replace(/^\*\s*/g, "").trim()));  // Clean up product names if the result is an array
        } else {
          console.error("Unexpected format:", data.similar_products);
          setSimilarProducts([]);
        }
      } else {
        setSimilarProducts([]);  // Handle case where no similar products are returned
      }
    }
  } catch (error) {
    setSimilarProducts(["Failed to get similar products. Error: " + error.message]);  // Handle error while fetching similar products
  } finally {
    setLoading(false);  // Hide loading state after fetching similar products
  }
};


  

  return (
    <div>
      <NavBar />
      <div className="container">
      <h1>Start by uploading an image of a product you wish to find an alternative for </h1>
  
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
  
      <div className="content-wrapper">
        {/* Left Column */}
        <div className="left-column">
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
              <button
                onClick={() => document.getElementById('file-input').click()}
                className="choose-image-button"
              >
                Choose an image
              </button>
              <button onClick={handleGetSimilarProducts} className="similar-products-button">
            Get Similar Products
          </button>
            </div>
          </div>
  
        </div>
  
        {/* Right Column */}
        <div className="right-column">
          <div className="similar-products-box">
            <h2 style={{ color: "#2f1c10"}}>Similar Products</h2>
  
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
              style={{ color: isHeartClicked ? 'red' : '#ccd4c2', cursor: 'pointer' }}
            >
              &#9829; {/* Heart icon */}
            </span>
          </div>
        </div>
      </div>
    </div>
    </div>
  );
  
}

export default ImageDescription;

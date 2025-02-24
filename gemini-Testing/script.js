require("dotenv").config();
const axios = require("axios");
const fs = require("fs");

// Load API key from .env file
const API_KEY = process.env.GEMINI_API_KEY;
const IMAGE_PATH = "TestImage.jpg";

// Read image and convert to Base64
function encodeImageToBase64(imagePath) {
  try {
    const imageBuffer = fs.readFileSync(imagePath);
    return imageBuffer.toString("base64");
  } catch (error) {
    console.error("Error reading image file:", error);
    process.exit(1);
  }
}

// Call Gemini API to analyze the image
async function analyzeImage(base64Image) {
    const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;


  const requestBody = {
    contents: [
      {
        parts: [
          { text: "Describe this image in detail." },
          { inline_data: { mime_type: "image/jpeg", data: base64Image } },
        ],
      },
    ],
  };

  try {
    const response = await axios.post(API_URL, requestBody, {
      headers: { "Content-Type": "application/json" },
    });

    // Extract and print the description
    const description = response.data.candidates?.[0]?.content?.parts?.[0]?.text;
    console.log("\nImage Description:\n", description || "No description provided.");
  } catch (error) {
    console.error("Error analyzing image:", error.response?.data || error.message);
  }
}

// Main function
(async () => {
  const base64Image = encodeImageToBase64(IMAGE_PATH);
  await analyzeImage(base64Image);
})();

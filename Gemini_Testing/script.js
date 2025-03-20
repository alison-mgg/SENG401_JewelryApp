// COMMENTED OUT BC I SWITCHED TO PYTHON, ONCE CONFIRMED, DELETE THIS




//require("dotenv").config();
// const axios = require("axios");
// const fs = require("fs");
// const express = require("express");
// const cors = require("cors");
// const multer = require("multer"); // Middleware to handle file uploads
// const path = require("path");
// const { resourceLimits } = require("worker_threads");

// //For express server (backend node.js framework)
// const app = express();
// const PORT = 5000;

// // Enable CORS to allow frontend (localhost:3000) to make requests
// app.use(cors({
//   origin: "http://localhost:3000",  // Allow requests from this origin
//   methods: "GET,POST",              // Allowed methods
// }));
// app.use(express.json());

// // Load API key from .env file
// const API_KEY = process.env.GEMINI_API_KEY;
// const IMAGE_PATH = "TestImage.jpg";

// // Initiate a json output file
// const OUTPUT_JSON = "output.json";

// const UPLOAD_DIR = "uploads";

// // Ensure upload directory exists
// if (!fs.existsSync(UPLOAD_DIR)) {
//   fs.mkdirSync(UPLOAD_DIR);
// }

// // Set up file storage using multer
// const storage = multer.diskStorage({
//   destination: UPLOAD_DIR,
//   filename: (req, file, cb) => {
//     cb(null, `uploaded_${Date.now()}${path.extname(file.originalname)}`);
//   },
// });

// const upload = multer({ storage });

// // Read image and convert to Base64
// function encodeImageToBase64(imagePath) {
//   try {
//     const imageBuffer = fs.readFileSync(imagePath);
//     return imageBuffer.toString("base64");
//   } catch (error) {
//     console.error("Error reading image file:", error);
//     process.exit(1);
//   }
// }

// // Call Gemini API to analyze the image
// async function analyzeImage(base64Image) {
//     const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;


//   const requestBody = {
//     contents: [
//       {
//         parts: [
//           { text: "Describe this image in detail." },
//           { inline_data: { mime_type: "image/jpeg", data: base64Image } },
//         ],
//       },
//     ],
//   };

//   try {
//     const response = await axios.post(API_URL, requestBody, {
//       headers: { "Content-Type": "application/json" },
//     });

//     console.log("Full AI API Response:", response.data);
//     if (!response.data || !response.data.candidates) {
//       console.error("Error: AI API returned invalid data", response.data);
//       return { error: "Failed to get a valid AI-generated description." };
//     }

//     // Extract and print the description
//     const description = response.data.candidates?.[0]?.content?.parts?.[0]?.text;
//     console.log("\nImage Description:\n", description || "No description provided.");

//     // Create JSON object
//     const result = {
//       image: IMAGE_PATH,
//       description: description,
//       timestamp: new Date().toISOString(),
//     };
//     // Save to output.json
//     fs.writeFileSync(OUTPUT_JSON, JSON.stringify(result, null, 4));
//     console.log(`\nImage description saved to ${OUTPUT_JSON}`);
//     console.log("Returning result:", result);
//     return result;

//   } catch (error) {
//     console.error("Error analyzing image:", error.response?.data || error.message);
//   }
// }


// // Endpoint for image upload & analysis
// app.post("/upload", upload.single("image"), async (req, res) => {
//   try{
//     if (!req.file) {
//       return res.status(400).json({ error: "No image uploaded." });
//     }
//     console.log("File received:", req.file.path);

//     const imagePath = req.file.path;
//     const base64Image = encodeImageToBase64(imagePath);

//     if (!base64Image) {
//       console.error("Error: Failed to process image.");
//       return res.status(500).json({ error: "Failed to process image." });
//     }

//     const result = await analyzeImage(base64Image);
//     console.log("analyzeImage function returned:", result);

//     // Ensure result is valid JSON before sending it
//     if (!result || typeof result !== "object"|| !result.description) {
//       console.error("Error: Invalid response from analyzeImage function", result);
//       return res.status(500).json({ error: "Invalid response from AI analysis." });
//     }

//     res.json(result);

//     // Cleanup: Delete the uploaded image after processing
//     fs.unlinkSync(imagePath);
//     console.log("Deleted uploaded image:", imagePath);
//   } catch (error) {
//     console.error("Error processing upload:", error);
//     res.status(500).json({ error: "Internal server error." });
//   }
// });

// // Endpoint to get latest description
// app.get("/description", (req, res) => {
//   if (fs.existsSync(OUTPUT_JSON)) {
//     const data = fs.readFileSync(OUTPUT_JSON, "utf-8");
//     res.json(JSON.parse(data));
//   } else {
//     res.json({ error: "No data available" });
//   }
// });

// // Start the server
// app.listen(PORT, () => {
//   console.log(`Server running on http://localhost:${PORT}`);
// });
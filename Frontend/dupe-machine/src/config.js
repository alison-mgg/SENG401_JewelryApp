/* Config.js File
 *
 * This file contains the configuration for the frontend application, such as the
 * API URL. Helps to manage the connections to backend hosted on Render, ensuring consistent
 * setup across all components of the application for API calls.
 */


const useLocalApi = false; // Set to true for local, false for remote

const localApiUrl = "http://localhost:5000";
const remoteApiUrl = "https://jewelry-dupe-app.onrender.com";
const corsProxyUrl = "https://cors-anywhere-6vpc.onrender.com";

const config = {
  apiURL: useLocalApi ? localApiUrl : `${corsProxyUrl}/${remoteApiUrl}`,
  corsProxyURL: corsProxyUrl, // Keep this for potential future use
};

export default config;
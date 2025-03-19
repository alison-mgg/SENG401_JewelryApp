/* Config.js File
 *
 * This file contains the configuration for the frontend application, such as the
 * API URL. Helps to manage the connections to backend hosted on Render, ensuring consistent
 * setup across all components of the application for API calls.
 */
// const config = {
//     apiURL: 'https://jewelry-dupe-app.onrender.com', // Updated to Render link
//     // apiURL: 'http://localhost:5000', // Original link
// };
  
//   export default config;

const config = {
    apiURL: 'https://jewelry-dupe-app.onrender.com',
    corsProxyURL: 'https://cors-anywhere-6vpc.onrender.com/'
};

export default config;
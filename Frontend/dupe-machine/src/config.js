/* Config.js File
 *
 * This file contains the configuration for the frontend application, such as the
 * API URL. Helps to manage the connections to backend hosted on Render, ensuring consistent
 * setup across all components of the application for API calls.
 */
const environment = process.env.NODE_ENV; // 'development' or 'production'

const config = {
  apiURL: environment === 'production'
    ? process.env.REACT_APP_BACKEND_URL_PRODUCTION
    : process.env.REACT_APP_BACKEND_URL_LOCAL,
  corsProxyURL: process.env.REACT_APP_CORS_PROXY_URL,
};

// Check if a CORS proxy is being used
if (config.corsProxyURL) {
  config.apiURL = `${config.corsProxyURL}/${config.apiURL}`;
}

export default config;
/* Config.js File
 *
 * This file contains the configuration for the frontend application, such as the
 * API URL and the environment (development or production). Helps to manage
 * the connections to backend hosted on AWS Elastic Beanstalk, ensuring consistent
 * setup across all components of the application for API calls.
 */
const config = {
    apiURL: 'http://jewelry-app-env.eba-r9q3svxm.ca-central-1.elasticbeanstalk.com',
    environment: 'development'  // Change depending on whether development or production
};

export default config;

# SENG401 Jewelry Dupe App
## L01 Group 3, Winter 2025 | March 21, 2025
### Written using Gemini LLM

This repository contains the source code for the SENG 401 project assignment, a jewelry dupe application. The app allows users to upload photos of jewelry and leverages the Gemini LLM to find and suggest similar products. It is built using a **Python Flask backend** and a **MySQL database** for data storage. The application includes user authentication, profile pages to store saved searches, and a **React-based frontend** for a seamless user experience.

## Authors

-   Chantal del Carmen
    -   GitHub: chantal-delcarmen

-   Maryam Al Sayed
    -   GitHub: malsayed03

-   Svara Patel
    -   GitHub: svaraP

-   Zaira Ramji
    -   GitHub: zaira-ra

-   Alison Gartner
    -   GitHub: alison-mgg

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

-   **Jewelry Dupe Search:** Upload a photo of jewelry and receive similar product suggestions powered by the Gemini LLM.
-   **User Authentication:** Secure sign-in and registration functionality.
-   **Profile Page:** Users can view and manage their saved product searches.
-   **Responsive Frontend:** Built with React for a modern and user-friendly interface.
-   **Gemini API Integration:** Seamless integration with the Gemini LLM for image processing and product matching.
-   **MySQL Database:** Utilizes a MySQL database to store user data and product information.
-   **Python Flask Backend:** Powered by a Python Flask backend for API endpoints and server-side logic.

## Getting Started

Follow these instructions to set up and run the application on your local machine.

### Prerequisites

Before you begin, ensure you have the following software installed:

### Prerequisites

Before you begin, ensure you have the following software installed:

-   Python 3.x
-   React (You'll need Node.js and npm or yarn to set up a React development environment)
-   MySQL Server

**Note:** React applications require Node.js and npm (or yarn) for development and build processes.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/alison-mgg/SENG401_JewelryApp](https://github.com/alison-mgg/SENG401_JewelryApp)
    cd SENG401_JewelryApp
    ```

2.  **Create and activate a Python virtual environment:**

    * **For macOS/Linux:**

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

    * **For Windows:**

        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Install backend dependencies:**

    ```bash
    pip install -r Backend/requirements.txt
    ```

    **Note:** Make sure you have the MySQL Python connector installed if it's not already included in your `requirements.txt`. You can install it using:

    ```bash
    pip install mysql-connector-python
    ```

4.  **Install frontend dependencies:**

    ```bash
    cd Frontend/dupe-machine
    npm install
    ```

5.  **Set up the MySQL database:**

    * Create a database named `401_sql_database`.
    * Import the `401_sql_database.sql` file into your MySQL database using a tool like phpMyAdmin or the MySQL command-line client.
    * Configure the database connection details in your `Gemini/.env` file.

      MYSQL_DB=401_sql_database
      MYSQL_HOST=localhost
      MYSQL_PASSWORD=seng401
      MYSQL_USER=seng401

### Running the Application

1.  **Start the Gemini API (Backend):**

    * **Ensure the virtual environment is activated:**

        ```bash
        # If not already activated
        source venv/bin/activate  # macOS/Linux
        # OR
        venv\Scripts\activate      # Windows
        ```

    * **Run the backend:**

        ```bash
        cd Gemini # Navigate to the Gemini directory
        python app.py # For Windows
        # OR
        python3 app.py # For macOS/Linux
        ```

2.  **Start the React Frontend:**

    ```bash
    cd Frontend/dupe-machine
    npm start
    ```

    This will launch the frontend in your default browser at `http://localhost:3000`.

---
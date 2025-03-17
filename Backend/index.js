const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("mysql");
const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());

const db = mysql.createConnection({
  host: "your-rds-endpoint",
  user: "your-username",
  password: "your-password",
  database: "your-database",
});

db.connect((err) => {
  if (err) {
    console.error("Error connecting to the database:", err);
    return;
  }
  console.log("Connected to the RDS database.");
});

app.post("/api/signup", (req, res) => {
  const { username, password } = req.body;
  const query = "INSERT INTO users (username, password) VALUES (?, ?)";
  db.query(query, [username, password], (err, result) => {
    if (err) {
      console.error("Error inserting user into database:", err);
      res.status(500).send("Error signing up");
      return;
    }
    res.status(200).send("User signed up successfully");
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});

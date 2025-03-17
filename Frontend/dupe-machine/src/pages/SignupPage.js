import React, { useState } from "react";
import axios from "axios";
import "../styling/SignupPage.css";

function SignupPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("https://jewelry-dupe-flask-app.onrender.com/api/signup", {
        username,
        password,
      });
      console.log(response.data);
    } catch (error) {
      console.error("There was an error signing up!", error);
    }
  };

  return (
    <div className="signup-container">
      <form onSubmit={handleSignup}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default SignupPage;
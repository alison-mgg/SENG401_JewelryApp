import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../styling/MainPage.css";

import NavBar from "../components/NavBar/NavBar.js";
 main

function MainPage() {
  return (
    <div className="mainpage-container">

      <NavBar />
 main
      <h1 className="page-title">Test: Welcome to The Main Page</h1>
    </div>
  );
}

export default MainPage;
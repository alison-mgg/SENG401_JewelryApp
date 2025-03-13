import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../styling/MainPage.css";
import NavigationBar from "./NavigationBar.js";

function MainPage() {
  return (
    <div className="mainpage-container">
      <NavigationBar />
      <h1 className="page-title">Test: Welcome to The Main Page</h1>
    </div>
  );
}

export default MainPage;
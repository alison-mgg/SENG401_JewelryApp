import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../styling/MainPage.css";

import NavBar from "./NavigationBar.js";
import Upload from "./UploadImageText.js";
import GPT from "./GPTResponce.js"
import Input from "./InputBox.js"

function MainPage() {
  return (
    <div className="mainpage-container">

      <NavBar />
      <div className = "Upload-container">
      <Upload /> 
      </div>
      <div className = "GPT-container">
      <GPT /> 
      </div>
      <div className = "Text-container">
      <Input /> 
      </div>

    </div>
  );
}

export default MainPage;
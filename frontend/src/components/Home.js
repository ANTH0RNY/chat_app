// home.js
import React from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const Navigate=useNavigate();

  return (
    <div>
      <h1> welcome to our chat application</h1>
      <button onClick={() => Navigate('/register')}>register</button>
      <button onClick={()=> Navigate('/login')} >login </button>
    </div>
  );
};

export default Home; 

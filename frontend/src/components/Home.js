// home.js
import React from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const Navigate=useNavigate();

  return (
    <div>
      <h1> welcome to our chat application</h1>
      <button onClick={() => Navigate('/login')}>Login</button>
    </div>
  );
};

export default Home; 

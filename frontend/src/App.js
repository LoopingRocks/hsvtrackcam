import React from 'react';
import ReactDOM from "react-dom";

import './App.css';

import NavBar from "./navbar";
import Home from "./home";

function App() {
  return (
    <div>
      <NavBar />
      <Home />
    </div>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);

export default App;

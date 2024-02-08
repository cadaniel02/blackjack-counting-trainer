import "./App.css";
import React, { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import { observer } from "mobx-react";
import SimpleApiComponent from "./test";
import CardGame from "./components/DrawCardPage";

import { render } from "react-dom";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

const App = observer(function App() {
  return (
    <div className="App">
      <header className="App-header">
        <CardGame />
      </header>
    </div>
  );
});

export default App;

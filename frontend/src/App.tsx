import React from 'react';
import './App.css';
import { observer } from 'mobx-react';
import SimpleApiComponent from './test';
import CardGame from './components/DrawCardPage';

const App = observer(function App() {
  return (
    <div className="App">
      <header className="App-header">
        <CardGame /> 
      </header>
    </div>
  );
})

export default App;

import React from 'react';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './components/pages/Home';
import SearchBar from './components/SearchBar';


function App() {
  return (
    <>
    <Router>
      <Navbar />
      <Routes>
        <Route path='/' exact component={Home}/>
      </Routes>
    </Router>
    <SearchBar/>
    </>
  );
}

export default App;

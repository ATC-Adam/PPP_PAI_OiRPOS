import logo from "../logo.svg";
import React from 'react';
import { useAuth } from "../providers/AuthContext";

const Home = () => {
  const { user, logout } = useAuth();

  return (
    <div className="App">
      <header style={{color: 'white'}}>
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://platforma.polsl.pl/rau2/course/view.php?id=195"
          target="_blank"
          rel="noopener noreferrer"
        >
          HolyTrinity WebApp
        </a>
        <h1> {'Hello ' + user.usrFirstName + '!'} </h1>
        
        <button onClick={() => { logout() }}> Wyloguj </button>

      </header>
    </div>
  );
};

export default Home;
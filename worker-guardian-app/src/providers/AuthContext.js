import React, { createContext, useContext, useState } from "react";
import axios from 'axios';

export const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

const emptyUser = {
  usrId: null,
  usrLogin: null,
  usrFirstName: null,
  usrLastName: null
}

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(
    () => JSON.parse(localStorage.getItem("isAuthenticated")) || false
  );
  const [user, setUser] = useState(
    () => JSON.parse(localStorage.getItem("user")) || emptyUser
  );
  
  const login = (username, password, handleError) => {
    const user = {
      login: username,
      password: password
    }
    
    axios.post('/login/', user)
      .then(res => {
        /* TODO: zapisywac w localStorage czy ciasteczko? */
        const userData = {
          usrId: 1,
          usrLogin: username,
          usrFirstName: username,
          usrLastName: username
        }
    
        setIsAuthenticated(true);
        setUser(userData);
    
        localStorage.setItem("isAuthenticated", JSON.stringify(true));
        localStorage.setItem("user", JSON.stringify(userData));
      })
      .catch(err => {
        if(err.status === 500) {
          handleError('Wystąpił nieprzewidziany błąd serwera!');
          return;
        }
        
        handleError(err.response.data.non_field_errors[0]);
      })
  }       

  /* TODO: API CALL */
  const logout = () => {
    setIsAuthenticated(false);
    setUser(emptyUser);

    localStorage.removeItem("isAuthenticated");
    localStorage.removeItem("user");
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );


}
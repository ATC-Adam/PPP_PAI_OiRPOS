import React, { useState } from 'react';
import { useAuth } from "../providers/AuthContext";

const LoginPage = () => {
  const { login } = useAuth();

  const [user, setUser] = useState({
    userLogin: null,
    userPassword: null
  })

  return (
    <div>
      <input type="text" placeholder="Login" onChange={(e) => { setUser((prev) => ({ ...prev, userLogin: e.target.value }))  }} /> <br />
      <input type="text" placeholder="Haslo" onChange={(e) => { setUser((prev) => ({ ...prev, userPassword: e.target.value }))  }} />
      
      <button onClick={() => { user.userLogin && user.userPassword ? login(user.userLogin, user.userPassword) : alert('Wpisz dane!')} }> Zaloguj </button>
    </div>
  );
};

export default LoginPage;
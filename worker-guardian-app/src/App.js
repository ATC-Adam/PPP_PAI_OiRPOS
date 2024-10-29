import "./App.css";

import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { AuthProvider } from "./providers/AuthContext";

import Home from "./pages/Home";
import LoginPage from "./pages/Login";
import ProtectedRoute from "./hooks/ProtectedRoutes";
import PublicRoute from "./hooks/PublicRoutes";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          
          {/* Public routes */}
          <Route path="/" element={<PublicRoute Component={LoginPage} />} />
          <Route path="/login" element={<PublicRoute Component={LoginPage} />} />
          
          {/* Protected routes */}
          <Route path="/home" element={<ProtectedRoute Component={Home} />} />

        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;

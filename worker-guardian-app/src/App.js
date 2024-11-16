import "./App.css";

import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { AuthProvider } from "./providers/AuthContext";

import Home from "./pages/Home";
import LoginPage from "./pages/Login";
import ProtectedRoute from "./hooks/ProtectedRoutes";
import PublicRoute from "./hooks/PublicRoutes";
import { ThemeProvider } from "@mui/material";
import { theme } from "./providers/ThemeProvider";

function App() {
  return (
    <ThemeProvider theme={theme}>
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
    </ThemeProvider>
  );
}

export default App;

import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../providers/AuthContext";

const ProtectedRoute = ({ Component }) => {
  const { isAuthenticated } = useAuth();

  return isAuthenticated ? <Component /> : <Navigate to="/" />;
}

export default ProtectedRoute;
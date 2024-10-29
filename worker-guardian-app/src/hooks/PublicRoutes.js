import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../providers/AuthContext";

const PublicRoute = ({ Component }) => {
  const { isAuthenticated } = useAuth();

  return !isAuthenticated ? <Component /> : <Navigate to="/home" />;
}

export default PublicRoute;


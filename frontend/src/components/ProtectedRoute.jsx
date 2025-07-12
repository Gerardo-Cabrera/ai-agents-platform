import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children, user }) => {
  // Verificar si el usuario está autenticado
  if (!user) {
    // Redirigir al login si no está autenticado
    return <Navigate to="/login" replace />;
  }

  // Si está autenticado, renderizar el contenido protegido
  return children;
};

export default ProtectedRoute;

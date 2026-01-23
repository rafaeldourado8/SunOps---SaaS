import { Navigate, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import useAuthStore from '../store/authStore';

const ProtectedRoute = ({ children }) => {
  const { token, checkTimeout, updateActivity } = useAuthStore();
  const location = useLocation();
  
  useEffect(() => {
    // Atualizar atividade ao mudar de rota
    if (token) {
      updateActivity();
    }
  }, [location, token, updateActivity]);
  
  // Verificar timeout
  if (token && checkTimeout()) {
    return <Navigate to="/login" replace />;
  }
  
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

export default ProtectedRoute;